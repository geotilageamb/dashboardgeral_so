"""Módulo de autenticação para o Dashboard Supervisão Ocupacional - TED INCRA/UFPR."""

import streamlit as st


def check_authentication():
    """
    Verifica se o usuário está autenticado.

    Returns:
        bool: True se o usuário estiver autenticado, False caso contrário.
    """
    # Correção: verificar se o email existe no objeto experimental_user
    # Um usuário autenticado sempre terá um email definido
    return hasattr(st.experimental_user, "email") and st.experimental_user.email != ""


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

    # Verifica se o email existe antes de exibi-lo
    if hasattr(st.experimental_user, "email"):
        st.sidebar.write(f"**Usuário:** {st.experimental_user.email}")
    elif hasattr(st.experimental_user, "name"):
        st.sidebar.write(f"**Usuário:** {st.experimental_user.name}")
    else:
        st.sidebar.write("**Usuário autenticado**")

    if st.sidebar.button("Sair do Sistema"):
        st.logout()
        st.rerun()
