import os
import re
import PyPDF2
from collections import defaultdict
from datetime import datetime

def extract_text_from_pdf(pdf_path):
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
    date_match = re.search(r'em (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})', pdf_text)
    if date_match:
        date_str = date_match.group(1)
        try:
            return datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        except ValueError as e:
            print(f"Erro ao converter a data: {e}")
    return None

def is_correct_format(filename):
    patterns = [
        r'^analiseRegularizacao_PA[A-Z]+_[A-Za-z]+_[A-F0-9]+\.pdf$',
        r'^relatorioConformidades(?:Regularizacao|Titulacao)?_PA[A-Z]+_[A-Za-z]+_[A-F0-9]+\.pdf$',
        r'^solicitacaoDocComplementar_PA[A-Z]+_[A-Za-z]+_[A-F0-9]+\.pdf$',
        r'^2_relatorioConformidades(?:Regularizacao|Titulacao)?_PA[A-Z]+_[A-Za-z]+_[A-F0-9]+\.pdf$'
    ]
    return any(re.match(pattern, filename) for pattern in patterns)

def rename_analise_regularizacao(original_name, pdf_text):
    reduced_name = re.sub(r'ANALISE_RO_', 'analiseRegularizacao_', original_name, flags=re.IGNORECASE)
    settlement_match = re.search(r'Projeto de Assentamento:\s*(PA [A-Z\s]+)(?= Processo Administrativo \(SEI\))', pdf_text)
    settlement_name = settlement_match.group(1).replace(' ', '').replace('\n', '') if settlement_match else "UnknownSettlement"
    assented_match = re.search(r'Nome Completo:\s*([A-Za-z]+)', pdf_text)
    assented_name = assented_match.group(1) if assented_match else "UnknownAssented"
    new_name = f"{reduced_name.split('_')[0]}_{settlement_name}_{assented_name}_{reduced_name.split('_')[-1]}"
    return new_name

def rename_relatorio_conformidades(original_name, pdf_text):
    if "Solicitação de Regularização de Ocupantes em Assentamentos" in pdf_text:
        prefix = "relatorioConformidadesRegularizacao_"
    elif "Solicitação de Titulação de Assentamento" in pdf_text:
        prefix = "relatorioConformidadesTitulacao_"
    else:
        prefix = "relatorioConformidades_"

    reduced_name = re.sub(r'RELATORIO_CONFORMIDADES_', prefix, original_name, flags=re.IGNORECASE)
    settlement_match = re.search(r'Projeto Assentamento:\s*[^-]+-\s*(PA [A-Z\s]+)(?= Processo administrativo \(SEI\))', pdf_text)
    settlement_name = settlement_match.group(1).replace(' ', '').replace('\n', '').strip() if settlement_match else "UnknownSettlement"
    assented_match = re.search(r'Nome:\s*([A-Za-z]+)', pdf_text)
    assented_name = assented_match.group(1) if assented_match else "UnknownAssented"
    new_name = f"{reduced_name.split('_')[0]}_{settlement_name}_{assented_name}_{reduced_name.split('_')[-1]}"
    return new_name

def rename_solicitacao_documentacao(original_name, pdf_text):
    reduced_name = re.sub(r'SOLICITACAO_DOCUMENTACAO_COMPLEMENTAR_', 'solicitacaoDocComplementar_', original_name, flags=re.IGNORECASE)
    settlement_match = re.search(r'PA\s*([A-Z\s]+?)(?=,|$)', pdf_text)
    if not settlement_match:
        settlement_match = re.search(r'Projeto de Assentamento\s*([A-Z\s]+)', pdf_text)
    settlement_name = settlement_match.group(1).replace(' ', '').replace('\n', '') if settlement_match else "UnknownSettlement"
    assented_match = re.search(r'Sr(?:\(a\))?\.\s*([A-Za-z]+)', pdf_text)
    if not assented_match:
        assented_match = re.search(r',\s*([A-Za-z]+)\s+[A-Za-z]+\s+[A-Za-z]+', pdf_text)
    assented_name = assented_match.group(1).replace('\n', '') if assented_match else "UnknownAssented"
    new_name = f"{reduced_name.split('_')[0]}_{settlement_name}_{assented_name}_{reduced_name.split('_')[-1]}"
    return new_name

def should_process_file(filename):
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
    return filename.startswith(("RELATORIO_CONFORMIDADES_", "relatorioConformidades"))

def process_pdfs_in_directory(directory_path):
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

            # Se o arquivo já está no formato correto e não é um relatório de conformidade,
            # podemos pular a renomeação
            if is_correct_format(filename) and not is_relatorio_conformidades(filename):
                continue

            print(f"Processando arquivo: {pdf_path}")
            pdf_text = extract_text_from_pdf(pdf_path)

            if is_relatorio_conformidades(filename):
                report_date = extract_date_from_text(pdf_text)
                if report_date:
                    conformidades_files.append((pdf_path, filename, report_date))

            # Renomear apenas se não estiver no formato correto
            if not is_correct_format(filename):
                new_file_name = None
                if filename.startswith(("ANALISE_RO_", "analiseRegularizacao_")):
                    new_file_name = rename_analise_regularizacao(filename, pdf_text)
                elif is_relatorio_conformidades(filename):
                    new_file_name = rename_relatorio_conformidades(filename, pdf_text)
                elif filename.startswith(("SOLICITACAO_DOCUMENTACAO_COMPLEMENTAR_", "solicitacaoDocComplementar_")):
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

    return output

if __name__ == "__main__":
    directory_path = r"D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/02_SO/11_municipiosPAs"
    result = process_pdfs_in_directory(directory_path)
    for line in result:
        print(line)
