import os
import pandas as pd
from thefuzz import process
import PyPDF2
import re

def load_mapping(csv_file):
    try:
        df_mapping = pd.read_csv(csv_file)
        return df_mapping
    except Exception as e:
        print(f"Erro ao ler arquivo CSV: {str(e)}")
        return pd.DataFrame()

def read_pdf_content(file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            last_page = pdf_reader.pages[-1]
            return last_page.extract_text()
    except Exception as e:
        print(f"Erro ao ler PDF {file_path}: {str(e)}")
        return ""

def check_document_type(content):
    if not content:
        return "Padrão"

    content = content.lower()
    encaminhamentos_match = re.search(r'encaminhamentos.*$', content, re.DOTALL)
    if not encaminhamentos_match:
        return "Padrão"

    final_text = encaminhamentos_match.group(0).lower()
    keywords = ['bloqueado', 'bloqueada', 'bloqueio', 'desbloqueio', 'desbloquear']

    for keyword in keywords:
        if keyword in final_text:
            return "Desbloqueio"

    return "Padrão"

def get_assentamento_info(filename, df_mapping):
    try:
        nome_assentamento = filename.split('_PA')[1].split('_')[0].strip()

        match = process.extractOne(nome_assentamento, 
                                 df_mapping['Assentamento'].tolist(),
                                 score_cutoff=60)

        if match:
            assentamento_match = match[0]
            municipio = df_mapping[df_mapping['Assentamento'] == assentamento_match]['Município'].iloc[0]
            codsipra = df_mapping[df_mapping['Assentamento'] == assentamento_match]['Codsipra'].iloc[0]
            return assentamento_match, municipio, codsipra

    except Exception as e:
        print(f"Erro ao extrair assentamento de {filename}: {str(e)}")

    return 'N/A', 'N/A', 'N/A'

def generate_spreadsheet_from_folder(folder_path, csv_path, output_path):
    df_mapping = load_mapping(csv_path)
    if df_mapping.empty:
        print("Erro: Não foi possível carregar o arquivo de mapeamento.")
        return

    data = []

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if ('parecerconclusivo' in filename.lower() and 
                filename.endswith('.pdf') and
                'ocupante_' not in filename.lower()):
                try:
                    parts = filename.split('_')
                    lote = parts[0] if len(parts) > 0 else 'N/A'

                    assentamento, municipio, codsipra = get_assentamento_info(filename, df_mapping)

                    file_path = os.path.join(root, filename)
                    content = read_pdf_content(file_path)
                    tipo = check_document_type(content)

                    relative_path = os.path.relpath(root, folder_path)
                    caminho = os.path.join(relative_path, filename) if relative_path != '.' else filename

                    data.append([
                        lote,
                        assentamento,
                        municipio,
                        codsipra,
                        tipo,
                        caminho
                    ])

                except Exception as e:
                    print(f"Erro ao processar arquivo {filename}: {str(e)}")
                    data.append(['N/A', 'N/A', 'N/A', 'N/A', 'N/A', caminho])

    df = pd.DataFrame(data, columns=[
        'Lote',
        'Assentamento',
        'Município',
        'Código SIPRA',
        'Tipo',
        'Caminho'
    ])

    try:
        df.to_excel(output_path, index=False)
        print(f"Planilha gerada com sucesso em: {output_path}")
    except Exception as e:
        print(f"Erro ao salvar a planilha: {str(e)}")

# Caminhos para os arquivos
folder_path = 'D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/02_SO/11_municipiosPAs'
csv_path = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/04_SO/04_codsipraPAsMunicipios.csv'
output_path = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/04_SO/04_contPareceres.xlsx'

generate_spreadsheet_from_folder(folder_path, csv_path, output_path)
