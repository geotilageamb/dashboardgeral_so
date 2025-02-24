import os
import re
import pandas as pd
from thefuzz import process


class LocalizationData:
    def __init__(self):
        self.root_directory = ('D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/'
                             '02_SO/11_municipiosPAs')
        self.output_directory = ('D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/'
                               '03_equipeGEOTI/08_automacoes/03_SO')
        self.csv_mapping_file = ('D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/'
                               '03_equipeGEOTI/08_automacoes/03_SO/'
                               '03_codsipraPAsMunicipios.csv')

        # Dicionários de exceções carregados do CSV
        self.municipio_exceptions = {}
        self.assentamento_exceptions = {}
        self.load_exceptions()

    def load_exceptions(self):
        try:
            df_exceptions = pd.read_csv(
                os.path.join(self.output_directory, 'exceptions.csv')
            )
            self.municipio_exceptions = dict(zip(
                df_exceptions['municipio_key'],
                df_exceptions['municipio_value']
            ))
            self.assentamento_exceptions = dict(zip(
                df_exceptions['assentamento_key'],
                df_exceptions['assentamento_value']
            ))
        except FileNotFoundError:
            # Usar dicionários padrão se o arquivo não existir
            self.municipio_exceptions = {
                "diamantedoeste": "DIAMANTE DO OESTE",
                "mangueirinha": "MANGUEIRINHA",
            }
            self.assentamento_exceptions = {
                "paanderrodolfohenrique": "ANDER RODOLFO HENRIQUE",
                "pa13denovembro": "13 DE NOVEMBRO",
                "pavitoriadauniaodoparana": "VITÓRIA DA UNIÃO DO PARANÁ",
                "vitoriadauniaodoparana": "VITÓRIA DA UNIÃO DO PARANÁ",
                "e.viva": "ESPERANÇA VIVA",
                "pa12deabril": "12 DE ABRIL",
                "12deabril": "12 DE ABRIL",
                "8dejunho": "8 DE JUNHO",
                "RondonIII": "RONDON III",
                "RandonIII": "RONDON III"
            }


class DataProcessor:
    def __init__(self, localization_data):
        self.loc_data = localization_data
        self.df_mapping = None
        self.assentamento_to_municipio = {}
        self.assentamento_to_codsipra = {}

    def load_mapping(self):
        """Carrega mapeamentos do arquivo CSV."""
        try:
            self.df_mapping = pd.read_csv(self.loc_data.csv_mapping_file)
            self.assentamento_to_municipio = dict(zip(
                self.df_mapping['Assentamento'].str.upper(),
                self.df_mapping['Município'].str.upper()
            ))
            self.assentamento_to_codsipra = dict(zip(
                self.df_mapping['Assentamento'].str.upper(),
                self.df_mapping['Codsipra']
            ))
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Arquivo de mapeamento não encontrado: "
                f"{self.loc_data.csv_mapping_file}"
            )

    def find_pdfs_with_prefix(self, prefix="Docs_"):
        """Encontra arquivos PDF com prefixo específico."""
        pdf_files = []
        for dirpath, _, filenames in os.walk(self.loc_data.root_directory):
            pdf_files.extend([
                os.path.join(dirpath, f) for f in filenames
                if f.startswith(prefix) and f.endswith(".pdf")
            ])
        return pdf_files

    def extract_info(self, file_path):
        """Extrai informações de município e assentamento do caminho do arquivo."""
        file_path_lower = file_path.lower()
        file_name_lower = os.path.basename(file_path).lower()

        municipio = self._extract_municipio(file_path_lower, file_name_lower)
        assentamento = self._extract_assentamento(file_path_lower, file_name_lower)

        return municipio.upper(), assentamento.upper()

    def _extract_municipio(self, file_path_lower, file_name_lower):
        """Extrai e processa nome do município."""
        for key, value in self.loc_data.municipio_exceptions.items():
            if key in file_path_lower or key in file_name_lower:
                return value

        municipio_match = re.search(
            r'11_municipiospas[\\/](\d+_([^\\/]+))',
            file_path_lower
        )
        return (municipio_match.group(2).replace('_', ' ')
                if municipio_match else '')

    def _extract_assentamento(self, file_path_lower, file_name_lower):
        """Extrai e processa nome do assentamento verificando múltiplas ocorrências."""
        # Verifica primeiro as exceções
        for key, value in self.loc_data.assentamento_exceptions.items():
            if key in file_path_lower or key in file_name_lower:
                return value

        # Lista para armazenar todas as ocorrências encontradas
        assentamento_names = []

        # Procura o padrão PA no formato pasta
        pa_folder_match = re.search(r'\\(\d+_pa([^\\/]+))', file_path_lower)
        if pa_folder_match:
            assentamento = pa_folder_match.group(2).replace('_', ' ')
            if assentamento.startswith("pa"):
                assentamento = assentamento[2:]
            assentamento_names.append(assentamento)

        # Procura outras ocorrências do nome do PA no caminho
        # Primeiro tenta encontrar padrões como "PANomePA" ou "PA NomePA"
        pa_matches = re.finditer(r'pa([a-zA-Z0-9]+)', file_path_lower)
        for match in pa_matches:
            assentamento = match.group(1)
            if assentamento not in assentamento_names:
                assentamento_names.append(assentamento)

        # Procura o nome sem o prefixo PA
        if assentamento_names:
            # Pega o primeiro nome encontrado e procura outras ocorrências similares
            base_name = assentamento_names[0]
            # Remove números e caracteres especiais para ter apenas o nome base
            base_name_clean = re.sub(r'[0-9_\s]', '', base_name)
            if len(base_name_clean) > 3:  # Evita matches com strings muito curtas
                other_matches = re.finditer(
                    f'{base_name_clean}[a-zA-Z0-9]*',
                    file_path_lower
                )
                for match in other_matches:
                    found_name = match.group(0)
                    if found_name not in assentamento_names:
                        assentamento_names.append(found_name)

        if not assentamento_names:
            return ''

        # Processa o nome mais longo encontrado (geralmente o mais completo)
        best_name = max(assentamento_names, key=len)
        # Adiciona espaços entre palavras em CamelCase
        processed_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', best_name)
        # Remove underscores e adiciona espaços
        processed_name = processed_name.replace('_', ' ')
        # Remove espaços extras
        processed_name = ' '.join(processed_name.split())

        return processed_name

    @staticmethod
    def find_best_match(name, choices):
        """Encontra a melhor correspondência usando fuzzy matching."""
        if not name:
            return 'Desconhecido'
        match, score, _ = process.extractOne(name, choices)
        return match if score > 80 else 'Desconhecido'

    @staticmethod
    def extract_lote(file_name):
        """Extrai e padroniza o número do lote."""
        lote_match = re.search(r'(L\d{1,3}|Lote\d{1,3}|lote\d{1,3})', file_name)
        if not lote_match:
            return 'Desconhecido'
        lote_number = re.search(r'\d{1,3}', lote_match.group(0)).group(0)
        return f'Lote {lote_number.zfill(3)}'

    def process_files(self):
        """Processa os arquivos e gera o DataFrame final."""
        pdf_files = self.find_pdfs_with_prefix()
        data = []

        for pdf_file in pdf_files:
            municipio, assentamento = self.extract_info(pdf_file)

            best_municipio = (
                municipio if municipio in self.loc_data.municipio_exceptions.values()
                else self.find_best_match(municipio, self.df_mapping['Município'])
            )

            best_assentamento = (
                assentamento if assentamento in self.loc_data.assentamento_exceptions.values()
                else self.find_best_match(assentamento, self.df_mapping['Assentamento'])
            )

            if best_assentamento in self.assentamento_to_municipio:
                best_municipio = self.assentamento_to_municipio[best_assentamento]

            codsipra = self.assentamento_to_codsipra.get(
                best_assentamento,
                'Desconhecido'
            )

            arquivo = os.path.basename(pdf_file)
            lote = self.extract_lote(arquivo)

            data.append([
                pdf_file, best_municipio, best_assentamento,
                codsipra, arquivo, lote
            ])

        return pd.DataFrame(
            data,
            columns=[
                "Caminho Completo", "Município", "Assentamento",
                "Código SIPRA", "Arquivo", "Lote"
            ]
        )


def main():
    """Função principal de execução."""
    try:
        loc_data = LocalizationData()
        processor = DataProcessor(loc_data)
        processor.load_mapping()

        df_result = processor.process_files()

        output_file = os.path.join(
            loc_data.output_directory,
            '03_contDocsRecebidos.xlsx'
        )
        df_result.to_excel(output_file, index=False)
        print(f'Planilha gerada com sucesso: {output_file}')

    except Exception as e:
        print(f'Erro durante a execução: {str(e)}')


if __name__ == "__main__":
    main()
