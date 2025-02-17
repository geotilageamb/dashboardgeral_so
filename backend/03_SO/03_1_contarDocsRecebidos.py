import os
import re
import pandas as pd
from thefuzz import process  # Certifique-se de usar 'thefuzz' em vez de 'fuzzywuzzy'

# Diretórios de origem e destino
root_directory = 'D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/02_SO/11_municipiosPAs'
output_directory = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/03_SO'

# Caminho para o arquivo CSV de mapeamento
csv_mapping_file = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/03_SO/03_codsipraPAsMunicipios.csv'

# Dicionários de exceções
municipio_exceptions = {
    "diamantedOeste": "DIAMANTE DO OESTE",
    "mangueirinha": "MANGUEIRINHA",
    # Adicione exceções específicas para municípios aqui
}

assentamento_exceptions = {
    "PAAnderRodolfoHenrique": "ANDER RODOLFO HENRIQUE",
    "PA13DeNovembro": "13 DE NOVEMBRO",
    "PAVitoriaDaUniaoDoParana": "VITÓRIA DA UNIÃO DO PARANÁ",
    "VitoriaDaUniaoDoParana": "VITÓRIA DA UNIÃO DO PARANÁ",
    "E.Viva": "ESPERANÇA VIVA",
    "PA12deAbril": "12 DE ABRIL",
    "12deAbril": "12 DE ABRIL",

    # Adicione outras exceções para assentamentos aqui
}

# Função para carregar o mapeamento do CSV e criar um dicionário de mapeamento de assentamentos para municípios
def load_mapping(csv_file):
    df_mapping = pd.read_csv(csv_file, delimiter=',')  # Ajuste o delimitador se necessário
    # Criar um dicionário de mapeamento de assentamentos para municípios
    assentamento_to_municipio = dict(zip(df_mapping['Assentamento'].str.upper(), df_mapping['Município'].str.upper()))
    # Criar um dicionário para o mapeamento de Codsipra
    assentamento_to_codsipra = dict(zip(df_mapping['Assentamento'].str.upper(), df_mapping['Codsipra']))
    return df_mapping, assentamento_to_municipio, assentamento_to_codsipra

# Função para encontrar todos os arquivos PDF que começam com "Docs_"
def find_pdfs_with_prefix(root_dir, prefix):
    pdf_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith(prefix) and filename.endswith(".pdf"):
                pdf_files.append(os.path.join(dirpath, filename))
    return pdf_files

# Função para extrair Município e Assentamento do caminho do arquivo
def extract_info(file_path):
    # Converter o caminho do arquivo e o nome do arquivo para minúsculas para comparação
    file_path_lower = file_path.lower()
    file_name_lower = os.path.basename(file_path).lower()

    # Inicializar variáveis
    municipio = ''
    assentamento = ''

    # Verificar exceções no caminho do arquivo e no nome do arquivo
    for key, value in municipio_exceptions.items():
        if key in file_path_lower or key in file_name_lower:
            municipio = value
            break
    else:
        municipio_match = re.search(r'11_municipiosPAs[\\/](\d+_([^\\/]+))', file_path, re.IGNORECASE)
        municipio = municipio_match.group(2).replace('_', ' ') if municipio_match else ''

    for key, value in assentamento_exceptions.items():
        if key in file_path_lower or key in file_name_lower:
            assentamento = value
            break
    else:
        assentamento_match = re.search(r'\\(\d+_PA([^\\/]+))', file_path, re.IGNORECASE)
        assentamento = assentamento_match.group(2).replace('_', ' ') if assentamento_match else ''

        # Remover prefixos conhecidos como "PA" do assentamento
        if assentamento.startswith("PA"):
            assentamento = assentamento[2:]

        # Adicionar espaços entre letras maiúsculas que não são seguidas por outra maiúscula
        assentamento = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', assentamento)

    return municipio.upper(), assentamento.upper()

# Função para encontrar a melhor correspondência usando fuzzy matching
def find_best_match(name, choices):
    if not name:
        return 'Desconhecido'
    match, score, _ = process.extractOne(name, choices)
    return match if score > 80 else 'Desconhecido'

# Função para extrair o lote do nome do arquivo e padronizar para "Lote XXX"
def extract_lote(file_name):
    lote_match = re.search(r'(L\d{1,3}|Lote\d{1,3}|lote\d{1,3})', file_name)
    if lote_match:
        # Extrair apenas os números e formatar como "Lote XXX"
        lote_number = re.search(r'\d{1,3}', lote_match.group(0)).group(0)
        return f'Lote {lote_number.zfill(3)}'
    return 'Desconhecido'

# Função principal para executar o código
def execute_code(root_directory, output_directory, df_mapping, assentamento_to_municipio, assentamento_to_codsipra):
    pdf_files = find_pdfs_with_prefix(root_directory, "Docs_")

    # Preparar os dados para a planilha
    data = []
    for pdf_file in pdf_files:
        municipio, assentamento = extract_info(pdf_file)

        # Aplicar exceções antes de fuzzy matching
        if municipio in municipio_exceptions.values():
            best_municipio = municipio
        else:
            best_municipio = find_best_match(municipio, df_mapping['Município'])

        if assentamento in assentamento_exceptions.values():
            best_assentamento = assentamento
        else:
            best_assentamento = find_best_match(assentamento, df_mapping['Assentamento'])

        # Verificar se o assentamento tem um município correspondente no mapeamento
        if best_assentamento in assentamento_to_municipio:
            best_municipio = assentamento_to_municipio[best_assentamento]

        # Obter o Codsipra correspondente ao assentamento
        codsipra = assentamento_to_codsipra.get(best_assentamento, 'Desconhecido')

        # Extrair o nome do arquivo
        arquivo = os.path.basename(pdf_file)

        # Extrair o lote do nome do arquivo
        lote = extract_lote(arquivo)

        data.append([pdf_file, best_municipio, best_assentamento, codsipra, arquivo, lote])

    # Criar um DataFrame com os dados
    df = pd.DataFrame(data, columns=["Caminho Completo", "Município", "Assentamento", "Código SIPRA", "Arquivo", "Lote"])

    # Salvar o DataFrame em uma planilha Excel, substituindo o arquivo existente
    output_file = os.path.join(output_directory, '03_contDocsRecebidos.xlsx')
    df.to_excel(output_file, index=False)

    print(f'Planilha gerada: {output_file}')

if __name__ == "__main__":
    df_mapping, assentamento_to_municipio, assentamento_to_codsipra = load_mapping(csv_mapping_file)
    execute_code(root_directory, output_directory, df_mapping, assentamento_to_municipio, assentamento_to_codsipra)
