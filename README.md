# Dashboard geral das metas e produtos da Supervisão Ocupacional (TED INCRA/UFPR)

Esse dashboard sistematiza diversos indicadores da equipe de supervisão ocupacional do Programa TED INCRA/UFPR
Link: https://so-dashboardgeral.streamlit.app

# Sumário
- [Resumo geral](#resumo-geral)
- [Backend](#backend)
  - [01_SO - Primeira página](#01_so-pasta-referente-à-primeira-página-do-dashboard)
  - [02_SO - Segunda página](#02_so-pasta-referente-à-segunda-página-do-dashboard)
  - [03_SO - Terceira página](#03_so-pasta-referente-à-terceira-página-do-dashboard)
  - [04_SO - Quarta página](#04_so-pasta-referente-à-quarta-página-do-dashboard)
  - [05_SO - Quinta página](#05_so-pasta-referente-à-quinta-página-do-dashboard)
- [Frontend](#frontend)
  - [Página 1 - Meta 2.1](#página-1-do-dashboard---meta-21-e-produtos-211-e-212)
  - [Página 2 - Meta 2.2](#página-2-do-dashboard---meta-22-e-produtos-221-222-223-e-224)
  - [Página 3 - Meta 2.3](#página-3-do-dashboard---meta-23-e-produtos-231-e-232)
  - [Página 4 - Meta 2.2.1.1](#página-4-do-dashboard---etapa-2211-da-meta-22)
  - [Página 5 - Meta 2.4](#página-5-do-dashboard---meta-24-e-produto-241)

# Resumo geral

# Backend

A alimentação desse dashboard, no backend, envolve 5 planilhas (.xlsx), 5 planilhas (.csv) e 10 códigos python (.py):

As páginas do dashboard e os respectivos arquivos envolvidos:

D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes

# 01_SO (Pasta referente à primeira página do dashboard)
- [01_1_infosLaudosModalidade.py](backend/01_SO/01_1_infosLaudosModalidade.py)
    - código python que extrai informações dos laudos dentro do SharePoint da SO e gera uma planilha com essas informações
- [01_2_copiadorPlanilha.py](backend/01_SO/01_2_copiadorPlanilha.py)
    - código python que copia a planilha de informações do SharePoint para o repositório do GitHub
- [01_codsipraPAsMunicipios.csv](backend/01_SO/01_codsipraPAsMunicipios.csv)
    - arquivo csv que alimenta o código python com os municípios, assentamentos e códigos SIPRA
- [01_datasModalidade.csv](backend/01_SO/01_datasModalidade.csv)
    - arquivo csv que alimenta o código python com a modalidade dos laudos conforme data de elaboração do laudo
- [01_laudos_SO_infos.xlsx](backend/01_SO/01_laudos_SO_infos.xlsx)
    - planilha gerada pelo código python com as informações dos laudos
- [01_nomesTecnicos.csv](backend/01_SO/01_nomesTecnicos.csv)
    - arquivo csv que alimenta o código python com o nome dos técnicos da SO

# 02_SO (Pasta referente à segunda página do dashboard)
- [02_1_renomeador_docsPGTWEB.py](backend/02_SO/02_1_renomeador_docsPGTWEB.py)
    - código python que identifica e renomeia arquivos da PGT - Plataforma de Governança Territorial presentes no SharePoint da SO, conforme regras definidas
- [02_2_quantificadorDocsPGTWEB.py](backend/02_SO/02_2_quantificadorDocsPGTWEB.py)
    - código python que quantifica os documentos da PGT - Plataforma de Governança Territorial presentes no SharePoint da SO, gerando planilha com essas informações
- [02_3_copiadorPlanilhaDocsPGTWEB.py](backend/02_SO/02_3_copiadorPlanilhaDocsPGTWEB.py)
    - código python que copia a planilha de informações do SharePoint para o repositório do GitHub
- [02_codsipraPAsMunicipios.csv](backend/02_SO/02_codsipraPAsMunicipios.csv)
    - arquivo csv que alimenta o código python com os municípios, assentamentos e códigos SIPRA
- [02_contPGT.xlsx](backend/02_SO/02_contPGT.xlsx)
    - planilha gerada pelo código python com as informações dos documentos da PGT - Plataforma de Governança Territorial

# 03_SO (Pasta referente à terceira página do dashboard)
- [03_1_contarDocsRecebidos.py](backend/03_SO/03_1_contarDocsRecebidos.py)
    - código python que identifica quantifica os documentos recebidos dos assentados pela SO
- [03_2_copiadorPlanilhaDocsRecebidos.py](backend/03_SO/03_2_copiadorPlanilhaDocsRecebidos.py)
    - código python que copia a planilha de informações do SharePoint para o repositório do GitHub
- [03_codsipraPAsMunicipios.csv](backend/03_SO/03_codsipraPAsMunicipios.csv)
    - arquivo csv que alimenta o código python com os municípios, assentamentos e códigos SIPRA
- [03_contDocsRecebidos.xlsx](backend/03_SO/03_contDocsRecebidos.xlsx)
    - planilha gerada pelo código python com as informações dos documentos recebidos pelos assentados

# 04_SO (Pasta referente à quarta página do dashboard)
- [04_1_quantificadorPareceres.py](backend/04_SO/04_1_quantificadorPareceres.py)
    - código python que identifica e quantifica os pareceres de beneficiário elaborados pela SO
- [04_2_copiadorPlanilhaPareceres.py](backend/04_SO/04_2_copiadorPlanilhaPareceres.py)
    - código python que copia a planilha de informações do SharePoint para o repositório do GitHub
- [04_codsipraPAsMunicipios.csv](backend/04_SO/04_codsipraPAsMunicipios.csv)
    - arquivo csv que alimenta o código python com os municípios, assentamentos e códigos SIPRA
- [04_contPareceres.xlsx](backend/04_SO/04_contPareceres.xlsx)
    - planilha gerada pelo código python com as informações dos pareceres de beneficiários elaborados pela SO

# 05_SO (Pasta referente à quinta página do dashboard)
- [05_1_contadorPlanilhasProd_SO.py](backend/05_SO/05_1_contadorPlanilhasProd_SO.py)
    - código python que identifica e quantifica as planilhas de monitoramento elaboradas pela SO
- [05_2_copiadorPlanilhasProducaoSO.py](backend/05_SO/05_2_copiadorPlanilhasProducaoSO.py)
    - código python que copia a planilha de informações do SharePoint para o repositório do GitHub
- [05_codsipraPAsMunicipios.csv](backend/05_SO/05_codsipraPAsMunicipios.csv)
    - arquivo csv que alimenta o código python com os municípios, assentamentos e códigos SIPRA
- [05_contPlanilhas.xlsx](backend/05_SO/05_contPlanilhas.xlsx)
    - planilha gerada pelo código python com as informações das planilhas de monitoramento elaboradas pela SO

# Frontend
Cada pasta (01_SO, 02_SO, etc.) representa uma página do dashboard e cada dashboard é alimentado por um código python e a respectiva planilha gerada no backend:

- Página 1 do dashboard - Meta 2.1 e produtos 2.1.1 e 2.1.2
    - [a_dashboard_laudos.py](/a_dashboard_laudos.py)
- Página 2 do dashboard - Meta 2.2 e produtos 2.2.1, 2.2.2, 2.2.3 e 2.2.4
    - [b_dashboard_documentos.py](/b_dashboard_documentos.py) 
- Página 3 do dashboard - Meta 2.3 e produtos 2.3.1 e 2.3.2
    - [c_dashboard_docs_recebidos.py](/c_dashboard_docs_recebidos.py)
- Página 4 do dashboard - Etapa 2.2.1.1 da meta 2.2
    - [d_dashboard_pareceres.py](/d_dashboard_pareceres.py)
- Página 5 do dashboard - Meta 2.4 e produto 2.4.1
    - [e_dashboard_planilhas.py](/e_dashboard_planilhas.py)

