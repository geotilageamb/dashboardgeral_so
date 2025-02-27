"""Dashboard Supervisão Ocupacional - TED INCRA/UFPR com autenticação."""

import streamlit as st
from a_dashboard_laudos import show_dashboard as show_dashboard_laudos
from b_dashboard_documentos import show_dashboard as show_dashboard_documentos
from c_dashboard_docs_recebidos import show_dashboard as show_dashboard_docs_recebidos
from d_dashboard_pareceres import show_dashboard as show_dashboard_pareceres
from e_dashboard_planilhas import show_dashboard as show_dashboard_planilhas


def setup_authentication():
    """Configura a autenticação do dashboard."""
    # Configuração dos usuários permitidos
    # Você pode substituir por uma fonte de dados mais robusta (banco de dados, etc.)
    AUTHORIZED_USERS = {
        "admin@ufpr.br": "senha123",
        "usuario@incra.gov.br": "senha456",
        # Adicione mais usuários conforme necessário
    }

    # Configuração da tela de login
    auth_config = {
        "form_name": "Login TED INCRA/UFPR",
        "login_button_label": "Entrar",
        "logout_button_label": "Sair",
        "hide_menu": True,  # Oculta o menu do Streamlit durante o login
        "allow_logout": True,
        "validator": lambda username, password: username in AUTHORIZED_USERS and AUTHORIZED_USERS[username] == password
    }

    # Tenta fazer login
    login_status = st.login(**auth_config)

    return login_status.is_logged_in


def show_dashboard():
    """Função que exibe o conteúdo principal do dashboard."""
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


def main():
    """Função principal que configura e exibe o dashboard com autenticação."""
    # Configuração da página
    st.set_page_config(
        page_title="Dashboard TED INCRA/UFPR",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Verifica autenticação
    is_authenticated = setup_authentication()

    # Exibe o dashboard apenas se o usuário estiver autenticado
    if is_authenticated:
        # Adiciona botão de logout no sidebar
        if st.sidebar.button("Sair do Sistema"):
            st.logout()
            st.rerun()

        # Exibe o dashboard
        show_dashboard()
    else:
        # Esta parte só será exibida se o login falhar
        # O formulário de login é gerenciado automaticamente pelo st.login()
        st.warning("Por favor, faça login para acessar o dashboard.")


if __name__ == "__main__":
    main()
