"""Módulo de autenticação para o Dashboard Supervisão Ocupacional - TED INCRA/UFPR."""

import streamlit as st


def check_authentication():
    """
    Verifica se o usuário está autenticado.

    Returns:
        bool: True se o usuário estiver autenticado, False caso contrário.
    """
    return st.experimental_user.is_logged_in


def show_login_screen():
    """
    Exibe a tela de login com opções de provedores.
    """
    st.title("Dashboard Supervisão Ocupacional - TED INCRA/UFPR")
    st.write("Por favor, faça login para acessar o dashboard.")

    # Layout de botões de login
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login com Google", use_container_width=True):
            st.login("google")

    with col2:
        if st.button("Login com Microsoft", use_container_width=True):
            st.login("microsoft")


def show_user_info():
    """
    Exibe informações do usuário logado e botão de logout no sidebar.
    """
    st.sidebar.markdown("---")
    st.sidebar.write(f"**Usuário:** {st.experimental_user.email}")

    if st.sidebar.button("Sair do Sistema"):
        st.logout()
        st.rerun()

