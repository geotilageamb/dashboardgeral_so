#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para processamento de documentos PDF relacionados a assentamentos.
Combina funcionalidades de renomeação de arquivos.
"""

import os
import pandas as pd
import PyPDF2
import re
import shutil
import unidecode
from thefuzz import process
from collections import defaultdict
from datetime import datetime


def extract_text_from_pdf(pdf_path):
    """Extrai o texto de um arquivo PDF."""
    print(f"Tentando abrir o arquivo: {pdf_path}")
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''
        return text
    except Exception as e:
        print(f"Erro ao processar o arquivo {pdf_path}: {e}")
        return ""


def extract_date_from_text(pdf_text):
    """Extrai a data de um texto de PDF."""
    date_match = re.search(r'em (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})', pdf_text)
    if date_match:
        date_str = date_match.group(1)
        try:
            return datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        except ValueError as e:
            print(f"Erro ao converter a data: {e}")
    return None


def extract_info_from_filename(filename):
    """Extrai informações do nome do arquivo."""
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
    """Carrega o arquivo de mapeamento CSV."""
    try:
        df_mapping = pd.read_csv(csv_file, delimiter=',')
        print(f"Arquivo de mapeamento carregado com sucesso. "
              f"Total de registros: {len(df_mapping)}")
        return df_mapping
    except Exception as e:
        print(f"Erro ao carregar arquivo de mapeamento: {e}")
        raise


def normalize_text(text):
    """Normaliza o texto removendo acentos e convertendo para minúsculas."""
    if not text:
        return ""
    return unidecode.unidecode(text.lower().strip())


def find_best_match(name, choices):
    """Encontra a melhor correspondência para um nome em uma lista de opções."""
    if not name:
        return 'Desconhecido'
    match, score, _ = process.extractOne(name, choices)
    return match if score > 80 else 'Desconhecido'


def find_best_match_in_csv(pa_name, df_mapping):
    """Encontra a melhor correspondência para um nome de PA no DataFrame de mapeamento."""
    if not pa_name:
        return None, None

    normalized_pa = normalize_text(pa_name)
    choices = df_mapping['Assentamento'].tolist()
    normalized_choices = [normalize_text(choice) for choice in choices]

    match = process.extractOne(normalized_pa, normalized_choices)
    if match and match[1] > 80:
        index = normalized_choices.index(match[0])
        return df_mapping.iloc[index]['Assentamento'], df_mapping.iloc[index]['nomePA']
    return None, None


def find_pa_name_in_text(text):
    """Encontra o nome do PA no texto do PDF."""
    patterns = [
        r'PA\s+([^\.,:;\n]+)',
        r'Projeto de Assentamento\s+([^\.,:;\n]+)',
        r'P\.A\.\s+([^\.,:;\n]+)'
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            pa_name = match.group(1).strip()
            if pa_name:
                return pa_name
    return None


def preprocess_assentamento(assentamento):
    """Pré-processa o nome do assentamento para padronização."""
    substitutions = {
        "PASAOJOAOMARIA": "SÃO JOÃO MARIA",
        "PAJOS": "JOSÉ DIAS",
    }
    return substitutions.get(assentamento, assentamento)


def is_correct_format(filename):
    """Verifica se o nome do arquivo está no formato correto."""
    patterns = [
        r'^analiseRegularizacao_PA[A-Za-z0-9]+_[A-Za-z]+_[A-F0-9]+\.pdf$',
        r'^relatorioConformidades(?:Regularizacao|Titulacao)?_PA[A-Za-z0-9]+_[A-Za-z]+_[A-F0-9]+\.pdf$',
        r'^solicitacaoDocComplementar_PA[A-Za-z0-9]+_[A-Za-z]+_[A-F0-9]+\.pdf$',
        r'^2_relatorioConformidades(?:Regularizacao|Titulacao)?_PA[A-Za-z0-9]+_[A-Za-z]+_[A-F0-9]+\.pdf$'
    ]
    return any(re.match(pattern, filename) for pattern in patterns)


def should_process_file(filename):
    """Verifica se o arquivo deve ser processado."""
    prefixes = [
        "ANALISE_RO_",
        "analiseRegularizacao_",
        "RELATORIO_CONFORMIDADES_",
        "relatorioConformidades",
        "SOLICITACAO_DOCUMENTACAO_COMPLEMENTAR_",
        "solicitacaoDocComplementar_"
    ]
    return filename.endswith(".pdf") and any(filename.startswith(prefix) for prefix in prefixes)


def is_relatorio_conformidades(filename):
    """Verifica se o arquivo é um relatório de conformidades."""
    return filename.startswith(("RELATORIO_CONFORMIDADES_", "relatorioConformidades"))


def rename_analise_regularizacao(original_name, pdf_text):
    """Renomeia arquivos de análise de regularização."""
    reduced_name = re.sub(r'ANALISE_RO_', 'analiseRegularizacao_', 
                          original_name, flags=re.IGNORECASE)
    settlement_match = re.search(
        r'Projeto de Assentamento:\s*(PA [A-Z\s]+)(?= Processo Administrativo \(SEI\))', 
        pdf_text
    )
    settlement_name = settlement_match.group(1).replace(' ', '').replace('\n', '') \
        if settlement_match else "UnknownSettlement"
    assented_match = re.search(r'Nome Completo:\s*([A-Za-z]+)', pdf_text)
    assented_name = assented_match.group(1) if assented_match else "UnknownAssented"
    new_name = f"{reduced_name.split('_')[0]}_{settlement_name}_{assented_name}_" \
               f"{reduced_name.split('_')[-1]}"
    return new_name


def rename_relatorio_conformidades(original_name, pdf_text):
    """Renomeia arquivos de relatório de conformidades."""
    if "Solicitação de Regularização de Ocupantes em Assentamentos" in pdf_text:
        prefix = "relatorioConformidadesRegularizacao_"
    elif "Solicitação de Titulação de Assentamento" in pdf_text:
        prefix = "relatorioConformidadesTitulacao_"
    else:
        prefix = "relatorioConformidades_"

    reduced_name = re.sub(r'RELATORIO_CONFORMIDADES_', prefix, 
                          original_name, flags=re.IGNORECASE)
    settlement_match = re.search(
        r'Projeto Assentamento:\s*[^-]+-\s*(PA [A-Z\s]+)(?= Processo administrativo \(SEI\))', 
        pdf_text
    )
    settlement_name = settlement_match.group(1).replace(' ', '').replace('\n', '').strip() \
        if settlement_match else "UnknownSettlement"
    assented_match = re.search(r'Nome:\s*([A-Za-z]+)', pdf_text)
    assented_name = assented_match.group(1) if assented_match else "UnknownAssented"
    new_name = f"{reduced_name.split('_')[0]}_{settlement_name}_{assented_name}_" \
               f"{reduced_name.split('_')[-1]}"
    return new_name


def rename_solicitacao_documentacao(original_name, pdf_text):
    """Renomeia arquivos de solicitação de documentação complementar."""
    reduced_name = re.sub(r'SOLICITACAO_DOCUMENTACAO_COMPLEMENTAR_', 
                          'solicitacaoDocComplementar_', 
                          original_name, flags=re.IGNORECASE)
    settlement_match = re.search(r'PA\s*([A-Z\s]+?)(?=,|$)', pdf_text)
    if not settlement_match:
        settlement_match = re.search(r'Projeto de Assentamento\s*([A-Z\s]+)', pdf_text)
    settlement_name = settlement_match.group(1).replace(' ', '').replace('\n', '') \
        if settlement_match else "UnknownSettlement"
    assented_match = re.search(r'Sr(?:\(a\))?\.\s*([A-Za-z]+)', pdf_text)
    if not assented_match:
        assented_match = re.search(r',\s*([A-Za-z]+)\s+[A-Za-z]+\s+[A-Za-z]+', pdf_text)
    assented_name = assented_match.group(1).replace('\n', '') \
        if assented_match else "UnknownAssented"
    new_name = f"{reduced_name.split('_')[0]}_{settlement_name}_{assented_name}_" \
               f"{reduced_name.split('_')[-1]}"
    return new_name


def rename_unknown_settlement_files(directory_path, df_mapping):
    """Renomeia arquivos com UnknownSettlement usando o mapeamento."""
    print("\nIniciando análise de arquivos com UnknownSettlement...")

    for root, _, files in os.walk(directory_path):
        for filename in files:
            if 'UnknownSettlement' in filename and filename.endswith('.pdf'):
                full_path = os.path.join(root, filename)
                print(f"\nAnalisando arquivo: {filename}")

                pdf_text = extract_text_from_pdf(full_path)
                pa_name = find_pa_name_in_text(pdf_text)

                if pa_name:
                    print(f"Nome do PA encontrado no PDF: {pa_name}")

                    assentamento, nome_pa = find_best_match_in_csv(pa_name, df_mapping)

                    if assentamento and nome_pa:
                        new_filename = filename.replace('UnknownSettlement', nome_pa)
                        new_full_path = os.path.join(root, new_filename)

                        try:
                            shutil.move(full_path, new_full_path)
                            print(f"Arquivo renomeado com sucesso para: {new_filename}")
                        except Exception as e:
                            print(f"Erro ao renomear arquivo: {e}")
                    else:
                        print(f"Não foi encontrada correspondência adequada no CSV para: {pa_name}")
                else:
                    print(f"Não foi possível encontrar o nome do PA no arquivo PDF")


def process_pdfs_in_directory(directory_path, df_mapping):
    """Processa os PDFs no diretório para renomeação."""
    output = []
    report_files = defaultdict(list)
    renamed_files = {}

    # Primeiro passo: coletar informações e renomear arquivos que precisam ser renomeados
    for root, _, files in os.walk(directory_path):
        conformidades_files = []

        for filename in files:
            if not should_process_file(filename):
                continue

            pdf_path = os.path.join(root, filename)

            # Verificar se o arquivo já está no formato correto
            if is_correct_format(filename):
                print(f"Arquivo já está no formato correto, pulando renomeação: {filename}")

                # Ainda precisamos processar relatórios de conformidade para possível prefixo
                if is_relatorio_conformidades(filename):
                    pdf_text = extract_text_from_pdf(pdf_path)
                    report_date = extract_date_from_text(pdf_text)
                    if report_date:
                        conformidades_files.append((pdf_path, filename, report_date))
                continue

            print(f"Processando arquivo: {pdf_path}")
            pdf_text = extract_text_from_pdf(pdf_path)

            if is_relatorio_conformidades(filename):
                report_date = extract_date_from_text(pdf_text)
                if report_date:
                    conformidades_files.append((pdf_path, filename, report_date))

            # Renomear apenas se não estiver no formato correto
            new_file_name = None
            if filename.startswith(("ANALISE_RO_", "analiseRegularizacao_")):
                new_file_name = rename_analise_regularizacao(filename, pdf_text)
            elif is_relatorio_conformidades(filename):
                new_file_name = rename_relatorio_conformidades(filename, pdf_text)
            elif filename.startswith(("SOLICITACAO_DOCUMENTACAO_COMPLEMENTAR_", 
                                     "solicitacaoDocComplementar_")):
                new_file_name = rename_solicitacao_documentacao(filename, pdf_text)

            if new_file_name and new_file_name != filename:
                new_file_path = os.path.join(root, new_file_name)
                try:
                    os.rename(pdf_path, new_file_path)
                    renamed_files[pdf_path] = new_file_path
                    output.append(f"Renomeado: '{filename}' para '{new_file_name}'")
                except Exception as e:
                    print(f"Erro ao renomear o arquivo {pdf_path}: {e}")

        # Processar relatórios de conformidade da pasta atual
        if len(conformidades_files) > 1:
            conformidades_files.sort(key=lambda x: x[2], reverse=True)
            most_recent = conformidades_files[0]

            current_path = renamed_files.get(most_recent[0], most_recent[0])
            current_name = os.path.basename(current_path)

            if not current_name.startswith("2_"):
                new_name_with_prefix = f"2_{current_name}"
                new_file_path = os.path.join(root, new_name_with_prefix)
                try:
                    os.rename(current_path, new_file_path)
                    output.append(f"Adicionado prefixo: '{current_name}' para '{new_name_with_prefix}'")
                except Exception as e:
                    print(f"Erro ao adicionar prefixo ao arquivo {current_path}: {e}")

    # Após processar todos os arquivos, chama a função para renomear arquivos com UnknownSettlement
    rename_unknown_settlement_files(directory_path, df_mapping)

    return output


def main():
    """Função principal que executa o fluxo completo do programa."""
    # Caminhos dos arquivos
    directory_path = 'D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/02_SO/11_municipiosPAs'
    output_path = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/02_SO/02_contPGT.xlsx'
    csv_mapping_file = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/02_SO/02_codsipraPAsMunicipiosNomePAs.csv'

    print("\n=== Iniciando processamento ===")
    print(f"Diretório de entrada: {directory_path}")
    print(f"Arquivo de mapeamento: {csv_mapping_file}")

    try:
        # Carrega o arquivo de mapeamento
        df_mapping = load_mapping(csv_mapping_file)

        # Primeiro renomeia os arquivos conforme necessário
        rename_results = process_pdfs_in_directory(directory_path, df_mapping)
        for line in rename_results:
            print(line)

        print("\nFunção de geração de relatório desativada conforme solicitado.")
    except Exception as e:
        print(f"\nErro crítico durante a execução: {e}")

    print("\n=== Processamento finalizado ===")


if __name__ == "__main__":
    main()
