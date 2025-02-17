import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    return pd.read_excel('04_contPareceres.xlsx')

def show_dashboard():
    st.header("Pareceres Conclusivos")
    df_pareceres = load_data()

    assentamentos = ['Todos'] + sorted(list(df_pareceres['Assentamento'].unique()))
    tipos = ['Todos'] + sorted(list(df_pareceres['Tipo'].unique()))

    col1, col2 = st.sidebar.columns(2)

    with col1:
        selected_assentamento = st.selectbox("Assentamento:", assentamentos, key="parecer_assentamento")
    with col2:
        selected_tipo = st.selectbox("Tipo:", tipos, key="parecer_tipo")

    # Aplicar filtros
    if selected_assentamento != "Todos":
        df_pareceres = df_pareceres[df_pareceres['Assentamento'] == selected_assentamento]
    if selected_tipo != "Todos":
        df_pareceres = df_pareceres[df_pareceres['Tipo'] == selected_tipo]

    # Métricas principais
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Padrão", df_pareceres[df_pareceres['Tipo'] == 'Padrão'].shape[0])
    with col2:
        st.metric("Desbloqueio", df_pareceres[df_pareceres['Tipo'] == 'Desbloqueio'].shape[0])

    # Barras de Progresso
    st.subheader("Progresso dos Pareceres")

    # Calcular totais e percentuais para Pareceres Padrão
    padrao_total = len(df_pareceres[df_pareceres['Tipo'] == 'Padrão'])
    total_padrao = 4239
    percentual_padrao = (padrao_total / total_padrao) * 100

    # Calcular totais e percentuais para Pareceres de Desbloqueio
    desbloqueio_total = len(df_pareceres[df_pareceres['Tipo'] == 'Desbloqueio'])
    total_desbloqueio = 500
    percentual_desbloqueio = (desbloqueio_total / total_desbloqueio) * 100

    # Criar duas colunas para as barras de progresso
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Pareceres Padrão**")
        st.progress(min(percentual_padrao/100, 1.0))
        st.write(f"{padrao_total} de {total_padrao} pareceres concluídos ({percentual_padrao:.1f}%)")

    with col2:
        st.markdown("**Pareceres de Desbloqueio**")
        st.progress(min(percentual_desbloqueio/100, 1.0))
        st.write(f"{desbloqueio_total} de {total_desbloqueio} pareceres concluídos ({percentual_desbloqueio:.1f}%)")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição por Tipo")
        tipo_data = df_pareceres['Tipo'].value_counts()
        fig_tipo = px.pie(
            names=tipo_data.index,
            values=tipo_data.values,
            title='Distribuição por Tipo',
            color_discrete_map={'Padrão': 'lightblue', 'Desbloqueio': 'coral'}
        )
        st.plotly_chart(fig_tipo)

    with col2:
        st.subheader("Distribuição por Assentamento")
        assentamento_data = df_pareceres['Assentamento'].value_counts()
        fig_assentamento = px.pie(
            names=assentamento_data.index,
            values=assentamento_data.values,
            title='Distribuição por Assentamento'
        )
        st.plotly_chart(fig_assentamento)

    # Dados detalhados
    st.subheader("Relação de pareceres")
    st.dataframe(
        df_pareceres[['Lote', 'Assentamento', 'Município', 'Código SIPRA', 'Tipo', 'Caminho']]
    )

if __name__ == "__main__":
    st.set_page_config(
        page_title="Dashboard Pareceres",
        page_icon="📊",
        layout="wide"
    )
    show_dashboard()
