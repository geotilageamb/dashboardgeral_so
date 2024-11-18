import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

@st.cache_data
def load_data():
    # Atualize o caminho do arquivo para o novo arquivo
    return pd.read_excel('contPareceres.xlsx')

def show_dashboard():
    st.header("Pareceres Conclusivos")
    df_pareceres = load_data()

    assentamentos = ['Todos'] + sorted(list(df_pareceres['Assentamento'].unique()))
    formatos = ['Todos'] + sorted(list(df_pareceres['Formato'].unique()))
    andamentos = ['Todos'] + sorted(list(df_pareceres['Andamento'].unique()))
    tipos = ['Todos'] + sorted(list(df_pareceres['Tipo'].unique()))

    col1, col2 = st.sidebar.columns(2)

    with col1:
        selected_assentamento = st.selectbox("Assentamento:", assentamentos, key="parecer_assentamento")
        selected_formato = st.selectbox("Formato:", formatos, key="parecer_formato")

    with col2:
        selected_andamento = st.selectbox("Andamento:", andamentos, key="parecer_andamento")
        selected_tipo = st.selectbox("Tipo:", tipos, key="parecer_tipo")

    # Aplicar filtros
    if selected_assentamento != "Todos":
        df_pareceres = df_pareceres[df_pareceres['Assentamento'] == selected_assentamento]
    if selected_formato != "Todos":
        df_pareceres = df_pareceres[df_pareceres['Formato'] == selected_formato]
    if selected_andamento != "Todos":
        df_pareceres = df_pareceres[df_pareceres['Andamento'] == selected_andamento]
    if selected_tipo != "Todos":
        df_pareceres = df_pareceres[df_pareceres['Tipo'] == selected_tipo]

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Em elaboração", df_pareceres[df_pareceres['Andamento'] == 'Em elaboração'].shape[0])
    with col2:
        st.metric("Concluídos", df_pareceres[df_pareceres['Andamento'] == 'Concluído'].shape[0])
    with col3:
        st.metric("Padrão", df_pareceres[df_pareceres['Tipo'] == 'Padrão'].shape[0])
    with col4:
        st.metric("Desbloqueio", df_pareceres[df_pareceres['Tipo'] == 'Desbloqueio'].shape[0])

    # Gráfico de progresso dos pareceres Padrão
    st.subheader("Progresso dos Pareceres Padrão")
    padrao_em_elaboracao = df_pareceres[(df_pareceres['Tipo'] == 'Padrão') & 
                                       (df_pareceres['Andamento'] == 'Em elaboração') &
                                       (df_pareceres['Formato'] == 'PDF')].shape[0]
    padrao_concluidos = df_pareceres[(df_pareceres['Tipo'] == 'Padrão') & 
                                    (df_pareceres['Andamento'] == 'Concluído') &
                                    (df_pareceres['Formato'] == 'PDF')].shape[0]
    total_padrao = 1622

    fig_padrao = go.Figure()
    fig_padrao.add_trace(go.Bar(
        name='Em elaboração',
        x=['Pareceres Padrão'],
        y=[padrao_em_elaboracao],
        marker_color='orange'
    ))
    fig_padrao.add_trace(go.Bar(
        name='Concluídos',
        x=['Pareceres Padrão'],
        y=[padrao_concluidos],
        marker_color='green'
    ))
    fig_padrao.add_trace(go.Bar(
        name='Faltando',
        x=['Pareceres Padrão'],
        y=[max(0, total_padrao - (padrao_em_elaboracao + padrao_concluidos))],
        marker_color='lightgrey'
    ))
    fig_padrao.update_layout(
        barmode='stack',
        xaxis_title='Status',
        yaxis_title='Quantidade',
        legend_title='Legenda'
    )
    st.plotly_chart(fig_padrao)

    # Gráfico de progresso dos pareceres de Desbloqueio
    st.subheader("Progresso dos Pareceres de Desbloqueio")
    desbloqueio_em_elaboracao = df_pareceres[(df_pareceres['Tipo'] == 'Desbloqueio') & 
                                            (df_pareceres['Andamento'] == 'Em elaboração') &
                                            (df_pareceres['Formato'] == 'PDF')].shape[0]
    desbloqueio_concluidos = df_pareceres[(df_pareceres['Tipo'] == 'Desbloqueio') & 
                                         (df_pareceres['Andamento'] == 'Concluído') &
                                         (df_pareceres['Formato'] == 'PDF')].shape[0]
    total_desbloqueio = 500

    fig_desbloqueio = go.Figure()
    fig_desbloqueio.add_trace(go.Bar(
        name='Em elaboração',
        x=['Pareceres de Desbloqueio'],
        y=[desbloqueio_em_elaboracao],
        marker_color='orange'
    ))
    fig_desbloqueio.add_trace(go.Bar(
        name='Concluídos',
        x=['Pareceres de Desbloqueio'],
        y=[desbloqueio_concluidos],
        marker_color='green'
    ))
    fig_desbloqueio.add_trace(go.Bar(
        name='Faltando',
        x=['Pareceres de Desbloqueio'],
        y=[max(0, total_desbloqueio - (desbloqueio_em_elaboracao + desbloqueio_concluidos))],
        marker_color='lightgrey'
    ))
    fig_desbloqueio.update_layout(
        barmode='stack',
        xaxis_title='Status',
        yaxis_title='Quantidade',
        legend_title='Legenda'
    )
    st.plotly_chart(fig_desbloqueio)

    # Primeiro row com dois gráficos lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição por Andamento")
        andamento_data = df_pareceres['Andamento'].value_counts()
        fig_andamento = px.pie(
            names=andamento_data.index,
            values=andamento_data.values,
            title='Distribuição por Andamento',
            color_discrete_map={'Em elaboração': 'orange', 'Concluído': 'green'}
        )
        st.plotly_chart(fig_andamento)

    with col2:
        st.subheader("Distribuição por Tipo")
        tipo_data = df_pareceres['Tipo'].value_counts()
        fig_tipo = px.pie(
            names=tipo_data.index,
            values=tipo_data.values,
            title='Distribuição por Tipo',
            color_discrete_map={'Padrão': 'lightblue', 'Desbloqueio': 'coral'}
        )
        st.plotly_chart(fig_tipo)

    # Gráfico de assentamentos em uma nova linha
    st.subheader("Distribuição por Assentamento")
    assentamento_data = df_pareceres['Assentamento'].value_counts()
    fig_assentamento = px.pie(
        names=assentamento_data.index,
        values=assentamento_data.values,
        title='Distribuição por Assentamento'
    )
    st.plotly_chart(fig_assentamento)

    # Tabela cruzada
    st.subheader("Análise Detalhada")
    cross_tab = pd.crosstab(
        [df_pareceres['Andamento'], df_pareceres['Tipo']], 
        df_pareceres['Formato']
    ).reset_index()
    st.write(cross_tab)

    # Dados detalhados
    st.subheader("Relação de pareceres")
    st.dataframe(
        df_pareceres[['Lote', 'Assentamento', 'Município', 'Formato', 'Andamento', 'Tipo', 'Caminho']]
    )

if __name__ == "__main__":
    st.set_page_config(
        page_title="Dashboard Pareceres",
        page_icon="📊",
        layout="wide"
    )
    show_dashboard()
