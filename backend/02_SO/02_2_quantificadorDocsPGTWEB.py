"""Módulo para processamento de arquivos PDF e extração de informações."""

import os
import re
import time
import pandas as pd
from thefuzz import process


class LocalizationData:
    """Classe para armazenar dados de localização e exceções."""

    def __init__(self):
        """Inicializa a classe com caminhos de arquivos e dicionários de exceções."""
        self.csv_mapping_file = ('D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/'
                                '03_equipeGEOTI/08_automacoes/02_SO/'
                                '02_codsipraPAsMunicipios.csv')

        # Dicionários de exceções
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
            "RandonIII": "RONDON III",
            "PASAOJOAOMARIA": "SÃO JOÃO MARIA",
            "PAJOSEDIAS": "JOSÉ DIAS",
        }


def extract_info_from_filename(filename):
    """Extrai informações do nome do arquivo.

    Args:
        filename: Nome do arquivo a ser processado

    Returns:
        Tupla com tipo_documento, assentamento, nome_t1, autenticador e is_second_report

    Raises:
        ValueError: Se o nome do arquivo não estiver no formato esperado
    """
    base_name = os.path.splitext(filename)[0]

    is_second_report = base_name.startswith('2_')
    if is_second_report:
        base_name = base_name[2:]

    parts = base_name.split('_')

    if len(parts) < 4:
        raise ValueError(f"Nome do arquivo '{filename}' não está no formato esperado.")

    tipo_documento = parts[0]
    assentamento = parts[1]
    nome_t1 = parts[2]
    autenticador = parts[3]

    return tipo_documento, assentamento, nome_t1, autenticador, is_second_report


def load_mapping(csv_file):
    """Carrega o arquivo de mapeamento e cria dicionários.

    Args:
        csv_file: Caminho para o arquivo CSV de mapeamento

    Returns:
        Tupla com dataframe de mapeamento e dicionários de mapeamento

    Raises:
        Exception: Se ocorrer erro ao carregar o arquivo
    """
    try:
        df_mapping = pd.read_csv(csv_file, delimiter=',')
        print(f"Arquivo de mapeamento carregado com sucesso. "
              f"Total de registros: {len(df_mapping)}")

        # Criar dicionários de mapeamento
        assentamento_to_municipio = dict(zip(
            df_mapping['Assentamento'].str.upper(),
            df_mapping['Município'].str.upper()
        ))
        assentamento_to_codsipra = dict(zip(
            df_mapping['Assentamento'].str.upper(),
            df_mapping['Codsipra']
        ))

        return df_mapping, assentamento_to_municipio, assentamento_to_codsipra
    except Exception as e:
        print(f"Erro ao carregar arquivo de mapeamento: {e}")
        raise


def find_best_match(name, choices, threshold=80):
    """Encontra a melhor correspondência usando fuzzy matching.

    Args:
        name: Nome a ser procurado
        choices: Lista de opções para comparação
        threshold: Limite mínimo de pontuação para considerar uma correspondência

    Returns:
        Melhor correspondência encontrada ou 'Desconhecido'
    """
    if not name:
        return 'Desconhecido'
    match, score, _ = process.extractOne(name, choices)
    return match if score > threshold else 'Desconhecido'


def preprocess_assentamento(assentamento, assentamento_exceptions):
    """Processa o nome do assentamento usando exceções e regras de formatação.

    Args:
        assentamento: Nome do assentamento a ser processado
        assentamento_exceptions: Dicionário de exceções para nomes de assentamentos

    Returns:
        Nome do assentamento processado
    """
    # Primeiro verifica se o assentamento está nas exceções
    assentamento_lower = assentamento.lower()
    for key, value in assentamento_exceptions.items():
        if key.lower() == assentamento_lower:
            return value.upper()

    # Processa o nome do assentamento
    # Adiciona espaços entre palavras em CamelCase
    processed_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', assentamento)
    # Remove prefixo PA se existir
    if processed_name.upper().startswith("PA"):
        processed_name = processed_name[2:]
    # Remove underscores e adiciona espaços
    processed_name = processed_name.replace('_', ' ')
    # Remove espaços extras
    processed_name = ' '.join(processed_name.split())

    return processed_name.upper()


def extract_assentamento_from_path(file_path, assentamento_exceptions):
    """Extrai o nome do assentamento do caminho do arquivo usando regex.

    Args:
        file_path: Caminho completo do arquivo
        assentamento_exceptions: Dicionário de exceções para nomes de assentamentos

    Returns:
        Nome do assentamento extraído do caminho
    """
    file_path_lower = file_path.lower()

    # Verifica primeiro as exceções
    for key, value in assentamento_exceptions.items():
        if key.lower() in file_path_lower:
            return value.upper()

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

    return processed_name.upper()


def process_pdfs_in_directory(directory_path, output_path, df_mapping, 
                             assentamento_to_municipio, assentamento_to_codsipra, 
                             loc_data):
    """Processa arquivos PDF em um diretório e gera uma planilha com os dados.

    Args:
        directory_path: Caminho do diretório com os arquivos PDF
        output_path: Caminho para salvar a planilha de saída
        df_mapping: DataFrame com mapeamento de assentamentos
        assentamento_to_municipio: Dicionário de mapeamento assentamento->município
        assentamento_to_codsipra: Dicionário de mapeamento assentamento->código SIPRA
        loc_data: Instância da classe LocalizationData com dados de exceções
    """
    tipo_documento_map = {
        'analiseRegularizacao': 'Análise para regularização',
        'relatorioConformidadesRegularizacao': 'Relatório de conformidades para regularização',
        'relatorioConformidadesTitulacao': 'Relatório de conformidades para titulação',
        'solicitacaoDocComplementar': 'Solicitação de documentação complementar'
    }

    valid_prefixes = set(tipo_documento_map.keys())
    data = []

    print(f"\nBuscando arquivos PDF em: {directory_path}")

    for root, _, files in os.walk(directory_path):
        pdf_files = [f for f in files if f.endswith('.pdf')]
        print(f"\nEncontrados {len(pdf_files)} arquivos PDF em: {root}")

        for filename in pdf_files:
            full_path = os.path.join(root, filename)
            check_filename = filename[2:] if filename.startswith('2_') else filename

            if any(check_filename.startswith(prefix) for prefix in valid_prefixes):
                try:
                    print(f"Processando: {filename}")
                    tipo_documento, assentamento_from_filename, nome_t1, autenticador, is_second_report = (
                        extract_info_from_filename(filename)
                    )

                    # Processa o nome do assentamento
                    assentamento_from_filename = preprocess_assentamento(
                        assentamento_from_filename, 
                        loc_data.assentamento_exceptions
                    )

                    # Tenta extrair o assentamento do caminho do arquivo também
                    assentamento_from_path = extract_assentamento_from_path(
                        full_path, 
                        loc_data.assentamento_exceptions
                    )

                    # Usa o nome mais longo entre os dois métodos
                    assentamento = (assentamento_from_path 
                                   if len(assentamento_from_path) > len(assentamento_from_filename) 
                                   else assentamento_from_filename)

                    tipo_documento_full = tipo_documento_map.get(tipo_documento, tipo_documento)
                    if is_second_report:
                        tipo_documento_full += ' (2º Relatório)'

                    objetivo = ''
                    if 'Regularizacao' in tipo_documento:
                        objetivo = 'Regularização'
                    elif 'Titulacao' in tipo_documento:
                        objetivo = 'Titulação'

                    # Encontra a melhor correspondência para o assentamento
                    best_assentamento = find_best_match(
                        assentamento, 
                        df_mapping['Assentamento']
                    )

                    # Obtém o município e código SIPRA do dicionário de mapeamento
                    municipio = assentamento_to_municipio.get(
                        best_assentamento.upper(), 
                        'Desconhecido'
                    )
                    codsipra = assentamento_to_codsipra.get(
                        best_assentamento.upper(), 
                        'Desconhecido'
                    )

                    data.append({
                        'Tipo de documento PGT': tipo_documento_full,
                        'Assentamento': best_assentamento,
                        'Município': municipio,
                        'Código SIPRA': codsipra,
                        'Nome T1': nome_t1,
                        'Autenticador': autenticador,
                        'Objetivo': objetivo,
                        'Segundo Relatório': 'Sim' if is_second_report else 'Não'
                    })
                except ValueError as e:
                    print(f"Erro ao processar {filename}: {e}")
                except Exception as e:
                    print(f"Erro inesperado ao processar {filename}: {e}")

    print(f"\nTotal de arquivos processados com sucesso: {len(data)}")

    if not data:
        print("Nenhum arquivo válido foi processado. Verifique os critérios de seleção.")
        return

    df = pd.DataFrame(data)
    print("\nColunas no DataFrame:", df.columns.tolist())

    try:
        df = df.sort_values(['Assentamento', 'Nome T1', 'Tipo de documento PGT'])
        print("DataFrame ordenado com sucesso")
    except KeyError as e:
        print(f"Erro ao ordenar DataFrame: {e}")
        print("Continuando sem ordenação...")

    try:
        # Garante que o diretório de saída existe
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Remove o arquivo existente se houver
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
                print(f"Arquivo existente removido: {output_path}")
                # Pequena pausa para garantir que o sistema de arquivos está atualizado
                time.sleep(1)
            except Exception as e:
                print(f"Aviso: Não foi possível remover o arquivo existente: {e}")

        # Tenta salvar o arquivo usando ExcelWriter
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl', mode='w') as writer:
                df.to_excel(writer, index=False)
            print(f'\nPlanilha gerada com sucesso: {output_path}')
        except Exception as e:
            print(f"Erro ao salvar com ExcelWriter: {e}")
            # Tenta método alternativo de salvamento
            df.to_excel(output_path, index=False, engine='openpyxl')
            print(f'\nPlanilha gerada com sucesso (método alternativo): {output_path}')

        # Verifica se o arquivo foi realmente criado
        if os.path.exists(output_path):
            print(f'Verificação: arquivo existe no caminho especificado')
        else:
            print(f"Aviso: Arquivo não encontrado após salvamento")

    except Exception as e:
        print(f"Erro ao manipular arquivo de saída: {e}")
        # Tenta salvar em um local alternativo em caso de erro
        alternative_path = os.path.join(os.path.dirname(output_path), 'contPGT_backup.xlsx')
        try:
            df.to_excel(alternative_path, index=False, engine='openpyxl')
            print(f"Planilha salva em local alternativo: {alternative_path}")
        except Exception as e2:
            print(f"Erro ao salvar no local alternativo: {e2}")


def main():
    """Função principal que executa o processamento completo."""
    # Caminhos dos arquivos
    directory_path = ('D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/'
                     '02_SO/11_municipiosPAs')
    output_path = ('D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/'
                  '03_equipeGEOTI/08_automacoes/02_SO/02_contPGT.xlsx')
    csv_mapping_file = ('D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/'
                       '03_equipeGEOTI/08_automacoes/02_SO/'
                       '02_codsipraPAsMunicipios.csv')

    print("\n=== Iniciando processamento ===")
    print(f"Diretório de entrada: {directory_path}")
    print(f"Arquivo de saída: {output_path}")
    print(f"Arquivo de mapeamento: {csv_mapping_file}")

    try:
        # Inicializa a classe de dados de localização
        loc_data = LocalizationData()

        # Carrega o mapeamento e cria os dicionários
        df_mapping, assentamento_to_municipio, assentamento_to_codsipra = load_mapping(
            csv_mapping_file
        )

        # Processa os arquivos PDF
        process_pdfs_in_directory(
            directory_path, 
            output_path, 
            df_mapping, 
            assentamento_to_municipio, 
            assentamento_to_codsipra, 
            loc_data
        )
    except Exception as e:
        print(f"\nErro crítico durante a execução: {e}")

    print("\n=== Processamento finalizado ===")


if __name__ == "__main__":
    main()
