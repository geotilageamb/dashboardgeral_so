import os
import pandas as pd
from thefuzz import process
import time

def extract_info_from_filename(filename):
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
    try:
        df_mapping = pd.read_csv(csv_file, delimiter=',')
        print(f"Arquivo de mapeamento carregado com sucesso. Total de registros: {len(df_mapping)}")
        return df_mapping
    except Exception as e:
        print(f"Erro ao carregar arquivo de mapeamento: {e}")
        raise

def find_best_match(name, choices):
    if not name:
        return 'Desconhecido'
    match, score, _ = process.extractOne(name, choices)
    return match if score > 80 else 'Desconhecido'

def preprocess_assentamento(assentamento):
    substitutions = {
        "PASAOJOAOMARIA": "SÃO JOÃO MARIA"
    }
    return substitutions.get(assentamento, assentamento)

def process_pdfs_in_directory(directory_path, output_path, df_mapping):
    tipo_documento_map = {
        'analiseRegularizacao': 'Análise para regularização',
        'relatorioConformidadesRegularizacao': 'Relatório de conformidades para regularização',
        'relatorioConformidadesTitulacao': 'Relatório de conformidades para titulação',
        'solicitacaoDocComplementar': 'Solicitação de documentação complementar'
    }

    valid_prefixes = set(tipo_documento_map.keys())
    data = []

    print(f"\nBuscando arquivos PDF em: {directory_path}")

    for root, dirs, files in os.walk(directory_path):
        pdf_files = [f for f in files if f.endswith('.pdf')]
        print(f"\nEncontrados {len(pdf_files)} arquivos PDF em: {root}")

        for filename in pdf_files:
            check_filename = filename[2:] if filename.startswith('2_') else filename

            if any(check_filename.startswith(prefix) for prefix in valid_prefixes):
                try:
                    print(f"Processando: {filename}")
                    tipo_documento, assentamento, nome_t1, autenticador, is_second_report = extract_info_from_filename(filename)

                    assentamento = preprocess_assentamento(assentamento)
                    tipo_documento_full = tipo_documento_map.get(tipo_documento, tipo_documento)
                    if is_second_report:
                        tipo_documento_full += ' (2º Relatório)'

                    objetivo = ''
                    if 'Regularizacao' in tipo_documento:
                        objetivo = 'Regularização'
                    elif 'Titulacao' in tipo_documento:
                        objetivo = 'Titulação'

                    best_assentamento = find_best_match(assentamento, df_mapping['Assentamento'])
                    municipio_row = df_mapping[df_mapping['Assentamento'] == best_assentamento]
                    municipio = municipio_row['Município'].values[0] if not municipio_row.empty else 'Desconhecido'
                    codsipra = municipio_row['Codsipra'].values[0] if not municipio_row.empty else 'Desconhecido'

                    data.append({
                        'Tipo de documento PGT': tipo_documento_full,
                        'Assentamento': best_assentamento,
                        'Município': municipio,
                        'Código SIPRA': codsipra,  # Adiciona o Código SIPRA
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

# Caminhos dos arquivos
directory_path = 'D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/02_SO/11_municipiosPAs'
output_path = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/02_SO/02_contPGT.xlsx'
csv_mapping_file = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/02_SO/02_codsipraPAsMunicipios.csv'

print("\n=== Iniciando processamento ===")
print(f"Diretório de entrada: {directory_path}")
print(f"Arquivo de saída: {output_path}")
print(f"Arquivo de mapeamento: {csv_mapping_file}")

try:
    df_mapping = load_mapping(csv_mapping_file)
    process_pdfs_in_directory(directory_path, output_path, df_mapping)
except Exception as e:
    print(f"\nErro crítico durante a execução: {e}")

print("\n=== Processamento finalizado ===")
