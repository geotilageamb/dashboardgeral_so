"""
Script para processar dados de assentamentos e municípios, gerando relatório consolidado.
"""
import os
import pandas as pd
from thefuzz import process


def encontrar_correspondencia(nome, lista_referencia):
    """Encontra a melhor correspondência usando fuzzy matching."""
    match = process.extractOne(nome, lista_referencia)
    return match[0] if match and match[1] >= 80 else None


# Caminhos das pastas
PASTA_BASE = r"D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/02_SO/11_municipiosPAs"
PASTA_DESTINO = r"D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/05_SO"

# Ler apenas o CSV com a coluna nomePA
ARQUIVO_CSV = r"D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/05_SO/05_codsipraPAsmunicipiosNomePAs.csv"

# Ler o CSV de referência
df_referencia = pd.read_csv(ARQUIVO_CSV)
print(f"Colunas do CSV: {df_referencia.columns.tolist()}")

# Verificar se a coluna nomePA existe
if 'nomePA' not in df_referencia.columns:
    print("ERRO: A coluna 'nomePA' não foi encontrada no CSV!")
    exit(1)

resultados = []

# Percorrer todas as pastas
for root, dirs, files in os.walk(PASTA_BASE):
    # Procurar arquivo de instrução processual
    planilha_encontrada = False
    for file in files:
        if 'planilhainstrucaoprocessual' in file.lower() and file.endswith('.xlsx'):
            planilha_encontrada = True
            pasta_atual = root

            # Lista única de municípios do CSV
            municipios_ref = df_referencia['Município'].unique()

            # Encontrar município
            nome_pasta = os.path.basename(pasta_atual)
            municipio = encontrar_correspondencia(nome_pasta, municipios_ref)

            if municipio:
                print(f"Município encontrado: {municipio}")
                # Procurar pastas de PAs no mesmo diretório
                pas_pasta = [d for d in os.listdir(pasta_atual) if '_PA' in d]

                # Para cada PA encontrado
                for pa_pasta in pas_pasta:
                    # Encontrar correspondência do PA usando a coluna nomePA
                    nomes_pas_ref = df_referencia['nomePA'].tolist()
                    pa_nome_correspondente = encontrar_correspondencia(pa_pasta, nomes_pas_ref)

                    if pa_nome_correspondente:
                        print(f"PA encontrado: {pa_nome_correspondente}")
                        # Buscar informações correspondentes no mesmo CSV
                        pa_info = df_referencia[df_referencia['nomePA'] == pa_nome_correspondente]

                        if not pa_info.empty:
                            # Filtrar apenas os registros do município correto
                            pa_info_municipio = pa_info[pa_info['Município'] == municipio]

                            if not pa_info_municipio.empty:
                                pa_info = pa_info_municipio

                            assentamento = pa_info['Assentamento'].iloc[0]
                            codigo_sipra = pa_info['Codsipra'].iloc[0]

                            resultados.append({
                                'Município': municipio,
                                'Assentamento': assentamento,
                                'Código SIPRA': codigo_sipra,
                                'Planilha de monitoramento': 'Sim' if planilha_encontrada else 'Não'
                            })

# Criar DataFrame com os resultados
if resultados:
    df_resultado = pd.DataFrame(resultados)

    # Remover duplicatas mantendo o 'Sim' se existir
    df_resultado = df_resultado.sort_values(
        'Planilha de monitoramento',
        ascending=False
    ).drop_duplicates(
        subset=['Município', 'Assentamento', 'Código SIPRA'],
        keep='first'
    )

    # Ordenar por Município e Assentamento
    df_resultado = df_resultado.sort_values(['Município', 'Assentamento'])

    # Salvar resultado
    arquivo_saida = os.path.join(PASTA_DESTINO, '05_contPlanilhas.xlsx')
    df_resultado.to_excel(arquivo_saida, index=False)
    print(f"\nArquivo salvo em: {arquivo_saida}")
    print(f"Total de registros: {len(df_resultado)}")
else:
    print("Nenhum resultado encontrado.")
