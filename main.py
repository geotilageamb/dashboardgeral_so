import streamlit as st
from dashboard_laudos import show_dashboard as show_dashboard_laudos
from dashboard_documentos import show_dashboard as show_dashboard_documentos
from dashboard_pareceres import show_dashboard as show_dashboard_pareceres
from dashboard_planilhas import show_dashboard as show_dashboard_planilhas

def main():
    st.title("Dashboard Supervisão Ocupacional - TED INCRA/UFPR")

    # Criação das abas
    tab1, tab2, tab3, tab4 = st.tabs([
        "Laudos de supervisão ocupacional",
        "Documentação PGT",
        "Pareceres conclusivos",
        "Planilhas monitoramento"
        
    ])

    # Configuração do menu lateral para cada aba
    with tab1:
        st.sidebar.title("Filtros - Laudos de supervisão ocupacional")
        # Adicione aqui os filtros específicos para o dashboard de Laudos de supervisão ocupacional
        show_dashboard_laudos()
            
    with tab2:
        st.sidebar.title("Filtros - Documentação PGT")
        # Adicione aqui os filtros específicos para o dashboard de Documentação PGT
        show_dashboard_documentos()
        
    with tab3:
        st.sidebar.title("Filtros - Pareceres conclusivos")
        # Adicione aqui os filtros específicos para o dashboard de Pareceres conclusivos
        show_dashboard_pareceres()

    with tab4:
        st.sidebar.title("Filtros - Planilhas monitoramento")
        # Adicione aqui os filtros específicos para o dashboard de Planilhas monitoramento
        show_dashboard_planilhas()

if __name__ == "__main__":
    main()
