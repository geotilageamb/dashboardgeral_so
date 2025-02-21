import os
import PyPDF2
import pandas as pd
import re

# Função para carregar o dicionário de padronização dos nomes dos técnicos de um arquivo CSV
def carregar_padronizacao_tecnicos(csv_path):
    df = pd.read_csv(csv_path)
    return dict(zip(df['Nome Original'], df['Nome Padronizado']))

# Função para padronizar os nomes dos técnicos
def padronizar_nome_tecnico(nome, padronizacao_tecnicos):
    return padronizacao_tecnicos.get(nome, nome)

# Função para encontrar um trecho de texto em um PDF
def encontrar_texto(caminho_pdf, trecho):
    with open(caminho_pdf, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            if trecho in text:
                return True
    return False

# Função para extrair texto após um padrão específico
def extrair_texto_apos_padrao(texto, padrao):
    resultado = re.search(padrao, texto)
    if resultado:
        return texto[resultado.end():].strip()
    else:
        return None

# Função para extrair uma data do texto
def extrair_data(texto):
    padrao = r"\d{2}/\d{2}/\d{4}"
    resultado = re.search(padrao, texto)
    if resultado:
        return resultado.group()
    else:
        return None

# Função para extrair a data de um PDF
def extrair_data_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_paginas = len(reader.pages)
        texto_ultima_pagina = reader.pages[num_paginas - 1].extract_text()
        padrao = r"Documento assinado eletronicamente por "
        texto_apos_padrao = extrair_texto_apos_padrao(texto_ultima_pagina, padrao)
        if texto_apos_padrao:
            return extrair_data(texto_apos_padrao)
        else:
            return None

# Função para extrair o nome do técnico de um PDF
def extrair_tecnico_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_paginas = len(reader.pages)
        texto_ultima_pagina = reader.pages[num_paginas - 1].extract_text()
        padrao = r"Documento assinado eletronicamente por (.+?)\d"
        resultado = re.search(padrao, texto_ultima_pagina)
        if resultado:
            nome_tecnico = resultado.group(1).strip()
            return nome_tecnico
        else:
            return None

# Função para extrair o assentamento de um PDF
def extrair_assentamento_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        texto_primeira_pagina = reader.pages[0].extract_text()
        padrao = r"PA\s*(.+?)\s*PR0"
        resultado = re.search(padrao, texto_primeira_pagina)
        if resultado:
            return resultado.group(1).strip()
        else:
            return None

# Função para verificar o tipo de laudo com base no nome do arquivo
def verificar_tipo_laudo(nome_arquivo):
    if 'DecBeneficiario' in nome_arquivo:
        return 'Laudo Declaração de Beneficiário'
    elif 'SimpBeneficiario' in nome_arquivo:
        return 'Laudo Simplificado de Beneficiário'
    elif 'CompBeneficiario' in nome_arquivo:
        return 'Laudo Completo de Beneficiário'
    elif 'DecOcupante' in nome_arquivo:
        return 'Laudo Declaração de Ocupante'
    elif 'SimpOcupante' in nome_arquivo:
        return 'Laudo Simplificado de Ocupante'
    elif 'CompOcupante' in nome_arquivo:
        return 'Laudo Completo de Ocupante'
    elif 'LoteVago' in nome_arquivo:
        return 'Laudo Lote Vago'
    else:
        return None

# Função para extrair o número do lote (LXX) do nome do arquivo
def extrair_LXX(nome_arquivo):
    padrao = r"L(\d+)"
    resultado = re.search(padrao, nome_arquivo)
    if resultado:
        return resultado.group(1)
    else:
        return None

# Função para carregar datas de mutirão e vistoria de um arquivo CSV
def carregar_datas(csv_path):
    df = pd.read_csv(csv_path)
    datas_mtr = df[df['tipo'] == 'mutirao']['data'].tolist()
    datas_vl = df[df['tipo'] == 'vistoria']['data'].tolist()
    return datas_mtr, datas_vl

# Função para carregar o mapeamento de assentamentos para municípios e códigos SIPRA
def carregar_municipios(csv_path):
    df = pd.read_csv(csv_path)
    municipios_map = dict(zip(df['Assentamento'], df['Município']))
    codsipra_map = dict(zip(df['Assentamento'], df['Codsipra']))
    return municipios_map, codsipra_map

# Função principal
def main():
    pasta_pdf = 'D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/02_SO/11_municipiosPAs'
    caminho_csv_datas = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/01_SO/01_datasModalidade.csv'
    caminho_csv_municipios = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/01_SO/01_codsipraPAsMunicipios.csv'
    caminho_csv_tecnicos = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/01_SO/01_nomesTecnicos.csv'
    resultados = []

    # Carregar padronização dos nomes dos técnicos
    padronizacao_tecnicos = carregar_padronizacao_tecnicos(caminho_csv_tecnicos)

    # Carregar datas de mutirão e vistoria
    datas_mtr, datas_vl = carregar_datas(caminho_csv_datas)

    # Carregar mapeamento de assentamentos para municípios e códigos SIPRA
    municipios_map, codsipra_map = carregar_municipios(caminho_csv_municipios)

    # Trechos que devem estar no nome do arquivo
    trechos_validos = [
        "DecOcupante", "SimpOcupante", "CompOcupante",
        "DecBeneficiario", "SimpBeneficiario", "CompBeneficiario",
        "LoteVago"
    ]

    for root, dirs, files in os.walk(pasta_pdf):
        for arquivo in files:
            if arquivo.endswith('.pdf') and any(trecho in arquivo for trecho in trechos_validos):
                caminho_completo = os.path.join(root, arquivo)
                data = extrair_data_pdf(caminho_completo)
                if data is None:
                    print(f"Falha ao extrair data do arquivo: {caminho_completo}")
                    continue

                tipo_laudo = verificar_tipo_laudo(arquivo)
                LXX = extrair_LXX(arquivo)
                tecnico = extrair_tecnico_pdf(caminho_completo)
                tecnico = padronizar_nome_tecnico(tecnico, padronizacao_tecnicos)
                assentamento = extrair_assentamento_pdf(caminho_completo)

                # Obter o município e o código SIPRA correspondente ao assentamento
                municipio = municipios_map.get(assentamento, "Desconhecido")
                codigo_sipra = codsipra_map.get(assentamento, "Desconhecido")

                modalidade = None
                if data in datas_mtr:
                    modalidade = "MUTIRÃO"
                elif data in datas_vl:
                    modalidade = "VISTORIA IN LOCO"

                resultados.append({
                    'Código SIPRA': codigo_sipra,
                    'Município': municipio,
                    'Assentamento': assentamento,
                    'Lote': LXX,
                    'Arquivo': arquivo,
                    'Data': data,
                    'Tipo de Laudo': tipo_laudo,
                    'Técnico': tecnico,
                    'Modalidade': modalidade
                })

    df = pd.DataFrame(resultados)

    if not df.empty:
        caminho_arquivo_excel = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/01_SO/01_laudos_SO_infos.xlsx'

        # Exclua o arquivo existente, se houver
        if os.path.exists(caminho_arquivo_excel):
            os.remove(caminho_arquivo_excel)

        # Reordenando as colunas
        df = df[['Código SIPRA', 'Município', 'Assentamento', 'Lote', 'Arquivo', 'Tipo de Laudo', 'Data', 'Técnico', 'Modalidade']]

        df.to_excel(caminho_arquivo_excel, index=False)

        print("Dados extraídos e salvos em", caminho_arquivo_excel)
    else:
        print("Nenhum dado foi extraído dos PDFs.")

if __name__ == "__main__":
    main()
