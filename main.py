"""Dashboard Supervisão Ocupacional - TED INCRA/UFPR."""

import streamlit as st
from a_dashboard_laudos import show_dashboard as show_dashboard_laudos
from b_dashboard_documentos import show_dashboard as show_dashboard_documentos
from c_dashboard_docs_recebidos import show_dashboard as show_dashboard_docs_recebidos
from d_dashboard_pareceres import show_dashboard as show_dashboard_pareceres
from e_dashboard_planilhas import show_dashboard as show_dashboard_planilhas

# Configuração da página - DEVE ser a primeira chamada Streamlit
st.set_page_config(
    page_title="Dashboard Supervisão Ocupacional - TED INCRA/UFPR",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# CSS para ocultar elementos do Streamlit
hide_streamlit_elements = """
    <style>
    /* Oculta o menu principal, rodapé e cabeçalho */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Oculta especificamente o ícone do GitHub no canto inferior direito */
    .stActionButton, .stGithubButton {
        display: none !important;
        visibility: hidden !important;
    }

    /* Oculta todos os elementos no canto inferior direito */
    section[data-testid="stBottomRightButtons"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Oculta qualquer ícone circular no canto inferior */
    .e1wbw7k90, .css-1p1nwyz, .css-1offfwp {
        display: none !important;
    }

    /* Oculta o botão de compartilhamento/GitHub */
    button[kind="secondary"] {
        display: none !important;
    }

    /* Oculta qualquer elemento com ícone circular */
    [data-testid="baseButton-headerNoPadding"] {
        display: none !important;
    }
    </style>
"""
st.markdown(hide_streamlit_elements, unsafe_allow_html=True)


def main():
    """Função principal que configura e exibe o dashboard."""
    st.title("Dashboard Supervisão Ocupacional - TED INCRA/UFPR")

    # Criação das abas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "2.1 Laudos",
        "2.2 Documentação PGT",
        "2.2.1.1 Documentos recebidos",
        "2.3 Pareceres conclusivos",
        "2.4 Planilhas monitoramento"
    ])

    # Configuração do menu lateral para cada aba
    with tab1:
        st.sidebar.title("Filtros - 2.1 Laudos")
        show_dashboard_laudos()

    with tab2:
        st.sidebar.title("Filtros - 2.2 Documentação PGT")
        show_dashboard_documentos()

    with tab3:
        st.sidebar.title("Filtros - 2.2.1.1 Documentos recebidos")
        show_dashboard_docs_recebidos()

    with tab4:
        st.sidebar.title("Filtros - 2.3 Pareceres conclusivos")
        show_dashboard_pareceres()

    with tab5:
        st.sidebar.title("Filtros - 2.4 Planilhas monitoramento")
        show_dashboard_planilhas()


if __name__ == "__main__":
    main()
