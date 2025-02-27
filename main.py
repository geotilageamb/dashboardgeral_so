"""Dashboard Supervisão Ocupacional - TED INCRA/UFPR."""

import streamlit as st
from a_dashboard_laudos import show_dashboard as show_dashboard_laudos
from b_dashboard_documentos import show_dashboard as show_dashboard_documentos
from c_dashboard_docs_recebidos import show_dashboard as show_dashboard_docs_recebidos
from d_dashboard_pareceres import show_dashboard as show_dashboard_pareceres
from e_dashboard_planilhas import show_dashboard as show_dashboard_planilhas


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
