import streamlit as st
from 01_dashboard_laudos import show_dashboard as show_dashboard_laudos
from 02_dashboard_documentos import show_dashboard as show_dashboard_documentos
from 04_dashboard_pareceres import show_dashboard as show_dashboard_pareceres
from 05_dashboard_planilhas import show_dashboard as show_dashboard_planilhas
from 03_dashboard_docs_recebidos import show_dashboard as show_dashboard_docs_recebidos

def main():
    st.title("Dashboard Supervisão Ocupacional - TED INCRA/UFPR")

    # Criação das abas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Laudos de supervisão ocupacional",
        "Documentação PGT",
        "Pareceres conclusivos",
        "Documentos recebidos",
        "Planilhas monitoramento"

    ])

    # Configuração do menu lateral para cada aba
    with tab1:
        st.sidebar.title("Filtros - Laudos de supervisão ocupacional")
        show_dashboard_laudos()

    with tab2:
        st.sidebar.title("Filtros - Documentação PGT")
        show_dashboard_documentos()

    with tab3:
        st.sidebar.title("Filtros - Pareceres conclusivos")
        show_dashboard_pareceres()
        
    with tab4:
        st.sidebar.title("Filtros - Documentos recebidos")
        show_dashboard_docs_recebidos()

    with tab5:
        st.sidebar.title("Filtros - Planilhas monitoramento")
        show_dashboard_planilhas()

if __name__ == "__main__":
    main()
