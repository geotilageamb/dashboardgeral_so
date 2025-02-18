import streamlit as st
import hashlib
from a_dashboard_laudos import show_dashboard as show_dashboard_laudos
from b_dashboard_documentos import show_dashboard as show_dashboard_documentos
from d_dashboard_pareceres import show_dashboard as show_dashboard_pareceres
from e_dashboard_planilhas import show_dashboard as show_dashboard_planilhas
from c_dashboard_docs_recebidos import show_dashboard as show_dashboard_docs_recebidos

# Hash da senha "199850"
SENHA_HASH = "8dc9fa69ec51a2e2165529f0fadae98f6a89497b9404bdc52651ba165fb9688f"

def verificar_senha(senha_digitada):
    """Verifica se a senha está correta usando hash."""
    senha_hash = hashlib.sha256(senha_digitada.encode()).hexdigest()
    return senha_hash == SENHA_HASH

def check_password():
    """Retorna `True` se a senha estiver correta."""
    def password_entered():
        """Verifica se a senha inserida está correta."""
        if verificar_senha(st.session_state["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Não armazena a senha
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Primeira execução, mostra o input para a senha
        st.text_input(
            "Por favor, digite a senha", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False

    return st.session_state["password_correct"]

def main():
    st.title("Dashboard Supervisão Ocupacional - TED INCRA/UFPR")

    if check_password():
        # Criação das abas
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "2.1 Laudos",
            "2.2 Documentação PGT",
            "2.3 Pareceres conclusivos",
            "2.2.1.1 Documentos recebidos",
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
            st.sidebar.title("Filtros - 2.3 Pareceres conclusivos")
            show_dashboard_pareceres()

        with tab4:
            st.sidebar.title("Filtros - Documentos recebidos")
            show_dashboard_docs_recebidos()

        with tab5:
            st.sidebar.title("Filtros - 2.4 Planilhas monitoramento")
            show_dashboard_planilhas()
    else:
        st.error("Senha incorreta. Por favor, tente novamente.")

if __name__ == "__main__":
    main()
