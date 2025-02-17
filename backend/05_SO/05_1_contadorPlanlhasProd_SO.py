import os
import pandas as pd
from thefuzz import process

# Caminhos das pastas
pasta_base = r"D:/ufpr.br/Intranet do LAGEAMB - TED-INCRA/02_SO/11_municipiosPAs"
pasta_destino = r"D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/05_SO"
arquivo_csv = os.path.join(pasta_destino, "05_codsipraPAsMunicipios.csv")

# Ler o CSV de referência
df_referencia = pd.read_csv(arquivo_csv)
print(f"Colunas do CSV: {df_referencia.columns.tolist()}")
resultados = []

def encontrar_correspondencia(nome, lista_referencia):
    """Encontra a melhor correspondência usando fuzzy matching"""
    match = process.extractOne(nome, lista_referencia)
    return match[0] if match and match[1] >= 80 else None

# Percorrer todas as pastas
for root, dirs, files in os.walk(pasta_base):
    # Procurar arquivo de instrução processual
    planilha_encontrada = False
    for file in files:
        if 'planilhaInstrucaoProcessual'.lower() in file.lower() and file.endswith('.xlsx'):
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
                    # Encontrar correspondência do PA no CSV
                    pas_municipio = df_referencia[df_referencia['Município'] == municipio]['Assentamento'].tolist()
                    pa_nome = encontrar_correspondencia(pa_pasta, pas_municipio)

                    if pa_nome:
                        print(f"PA encontrado: {pa_nome}")
                        # Buscar código SIPRA
                        codigo_sipra = df_referencia[
                            (df_referencia['Município'] == municipio) & 
                            (df_referencia['Assentamento'] == pa_nome)
                        ]['Codsipra'].iloc[0]  # Alterado para 'Codsipra'

                        resultados.append({
                            'Município': municipio,
                            'Assentamento': pa_nome,
                            'Código SIPRA': codigo_sipra,
                            'Planilha de monitoramento': 'Sim' if planilha_encontrada else 'Não'
                        })

# Criar DataFrame com os resultados
if resultados:
    df_resultado = pd.DataFrame(resultados)

    # Remover duplicatas mantendo o 'Sim' se existir
    df_resultado = df_resultado.sort_values('Planilha de monitoramento', ascending=False).drop_duplicates(
        subset=['Município', 'Assentamento', 'Código SIPRA'], keep='first'
    )

    # Ordenar por Município e Assentamento
    df_resultado = df_resultado.sort_values(['Município', 'Assentamento'])

    # Salvar resultado
    arquivo_saida = os.path.join(pasta_destino, '05_contPlanilhas.xlsx')
    df_resultado.to_excel(arquivo_saida, index=False)
    print(f"\nArquivo salvo em: {arquivo_saida}")
    print(f"Total de registros: {len(df_resultado)}")
else:
    print("Nenhum resultado encontrado.")
