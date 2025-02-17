import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    return pd.read_excel('02_contPGT.xlsx')

def show_dashboard():
    st.header("Produtos da meta 2.2")
    df_pgt = load_data()

    if 'Objetivo' in df_pgt.columns:
        df_pgt['Objetivo'].fillna('Não especificado', inplace=True)

    if 'Município' not in df_pgt.columns:
        st.error("A coluna 'Município' não está presente nos dados.")
        return

    tipos_documento = ['Todos'] + sorted(list(df_pgt['Tipo de documento PGT'].unique()))
    assentamentos = ['Todos'] + sorted(list(df_pgt['Assentamento'].unique()))
    municipios = ['Todos'] + sorted(list(df_pgt['Município'].unique()))
    nomes_t1 = ['Todos'] + sorted(list(df_pgt['Nome T1'].unique()))

    if 'Objetivo' in df_pgt.columns:
        objetivos = ['Todos'] + sorted(list(df_pgt['Objetivo'].unique()))
    else:
        objetivos = ['Todos']

    # Configuração dos filtros no sidebar
    selected_tipo_documento = st.sidebar.selectbox("Selecione um tipo de documento:", tipos_documento, key="tipo_documento_pgt_unique")
    selected_assentamento = st.sidebar.selectbox("Selecione um assentamento:", assentamentos, key="assentamento_pgt_unique")
    selected_municipio = st.sidebar.selectbox("Selecione um município:", municipios, key="municipio_pgt_unique")
    selected_nome_t1 = st.sidebar.selectbox("Selecione um nome T1:", nomes_t1, key="nome_t1_pgt_unique")
    selected_objetivo = st.sidebar.selectbox("Selecione um objetivo:", objetivos, key="objetivo_pgt_unique")

    # Aplicar filtros
    filtered_df = df_pgt.copy()
    if selected_tipo_documento != "Todos":
        filtered_df = filtered_df[filtered_df['Tipo de documento PGT'] == selected_tipo_documento]
    if selected_assentamento != "Todos":
        filtered_df = filtered_df[filtered_df['Assentamento'] == selected_assentamento]
    if selected_municipio != "Todos":
        filtered_df = filtered_df[filtered_df['Município'] == selected_municipio]
    if selected_nome_t1 != "Todos":
        filtered_df = filtered_df[filtered_df['Nome T1'] == selected_nome_t1]
    if selected_objetivo != "Todos" and 'Objetivo' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Objetivo'] == selected_objetivo]

    # Barras de Progresso
    st.subheader("Progresso da Documentação")

    # Calcular totais e percentuais
    relatorios_conf_atual = len(df_pgt[df_pgt['Tipo de documento PGT'] == 'Relatório de conformidades para regularização'])
    solicitacoes_atual = len(df_pgt[df_pgt['Tipo de documento PGT'] == 'Solicitação de documentação complementar'])
    segundos_relatorios_atual = len(df_pgt[df_pgt['Tipo de documento PGT'].str.contains('2º Relatório', na=False)])
    analise_reg_atual = len(df_pgt[df_pgt['Tipo de documento PGT'] == 'Análise para regularização'])

    # Definir metas
    total_relatorios_conf = 2246
    total_solicitacoes = 674
    total_segundos_relatorios = 337
    total_analise_reg = 1622

    # Calcular percentuais
    percentual_relatorios_conf = (relatorios_conf_atual / total_relatorios_conf) * 100
    percentual_solicitacoes = (solicitacoes_atual / total_solicitacoes) * 100
    percentual_segundos_relatorios = (segundos_relatorios_atual / total_segundos_relatorios) * 100
    percentual_analise_reg = (analise_reg_atual / total_analise_reg) * 100

    # Exibir barras de progresso em ordem
    st.markdown("**2.2.1. Relatório de conformidades para regularização**")
    st.progress(min(percentual_relatorios_conf/100, 1.0))
    st.write(f"{relatorios_conf_atual} de {total_relatorios_conf} documentos ({percentual_relatorios_conf:.1f}%)")

    st.markdown("**2.2.2. Solicitação de documentação complementar**")
    st.progress(min(percentual_solicitacoes/100, 1.0))
    st.write(f"{solicitacoes_atual} de {total_solicitacoes} documentos ({percentual_solicitacoes:.1f}%)")

    st.markdown("**2.2.3. Segundos relatórios de conformidades para regularização**")
    st.progress(min(percentual_segundos_relatorios/100, 1.0))
    st.write(f"{segundos_relatorios_atual} de {total_segundos_relatorios} documentos ({percentual_segundos_relatorios:.1f}%)")

    st.markdown("**2.2.4. Análise para regularização**")
    st.progress(min(percentual_analise_reg/100, 1.0))
    st.write(f"{analise_reg_atual} de {total_analise_reg} documentos ({percentual_analise_reg:.1f}%)")

    # Resto do dashboard permanece igual
    st.markdown("### Distribuição dos documentos por tipo")
    tipo_documento_data = filtered_df['Tipo de documento PGT'].value_counts()
    fig_tipo_documento = px.pie(
        names=tipo_documento_data.index,
        values=tipo_documento_data.values,
    )
    st.plotly_chart(fig_tipo_documento)

    st.markdown("### Distribuição dos documentos por assentamento")
    assentamento_data = filtered_df['Assentamento'].value_counts()
    st.bar_chart(assentamento_data)

    st.markdown("### Distribuição dos documentos por município")
    municipio_data = filtered_df['Município'].value_counts()
    fig_municipio = px.pie(
        names=municipio_data.index,
        values=municipio_data.values,
    )
    st.plotly_chart(fig_municipio)

    if 'Objetivo' in filtered_df.columns:
        st.markdown("### Distribuição dos documentos por objetivo")
        objetivo_data = filtered_df['Objetivo'].value_counts()
        st.bar_chart(objetivo_data)

    st.markdown("### Relação geral da documentação")
    st.write(filtered_df)

    total_por_tipo_assentamento = filtered_df.groupby(['Tipo de documento PGT', 'Assentamento']).size().reset_index(name='Quantidade de Documentos')
    st.markdown("### Quantidade de documentos por tipo e assentamento")
    st.write(total_por_tipo_assentamento)

if __name__ == "__main__":
    show_dashboard()
