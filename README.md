# dashboardgeral_so

Esse dashboard sistematiza diversos indicadores da equipe de supervisão ocupacional do Programa TED INCRA/UFPR
Link: https://so-dashboardgeral.streamlit.app

# Backend

A alimentação desse dashboard, no backend, envolve 5 planilhas (.xlsx), 5 planilhas (.csv) e 10 códigos python (.py):

As páginas do dashboard e os respectivos arquivos envolvidos:

D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes

01_SO (Pasta referente à primeira página do dashboard)
- 01_1_infosLaudosModalide.py (código python que extrai informações dos laudos dentro do SharePoint da SO e gera uma planilha com essas informações)
- 01_2_copiadorPlanilha.py (código python que copia a planilha de informações do SharePoint para o repositório do GitHub)
- 01_codsipraPAsMunicipios.csv (arquivo csv que alimenta o código python com os municípios, assentamentos e códigos SIPRA)
- 01_datasModalidade.csv (arquivo csv que alimenta o código python com a modalidade dos laudos conforme data de elaboração do laudo)
- 01_laudos_SO_infos.xlsx (planilha gerada pelo código python com as informações dos laudos)
- 01_nomesTecnicos.csv (arquivo csv que alimenta o código python com o nome dos técnicos da SO)

02_SO (Pasta referente à segunda página do dashboard)
- 02_1_renomeador_docsPGTWEB.py (código python que identifica e renomeia arquivos da PGT - Plataforma de Governança Territorial presentes no SharePoint da SO, conforme regras definidas)
- 02_2_quantificadorDocsPGTWEB.py (código python que quantifica os documentos da PGT - Plataforma de Governança Territorial presentes no SharePoint da SO, gerando planilha com essas informações)
- 02_3_copiadorPlanilhaDocsPGTWEB.py (código python que copia a planilha de informações do SharePoint para o repositório do GitHub)
- 02_codsipraPAsMunicipios.csv (arquivo csv que alimenta o código python com os municípios, assentamentos e códigos SIPRA)
- 02_contPGT.xlsx (planilha gerada pelo código python com as informações dos documentos da PGT - Plataforma de Governança Territorial)

03_SO (Pasta referente à terceira página do dashboard)
- 03_1_contarDocsRecebidos.py (código python que identifica quantifica os documentos recebidos dos assentados pela SO)
- 03_2_copiadorPlanilhaDocsRecebidos.py (código python que copia a planilha de informações do SharePoint para o repositório do GitHub)
- 03_codsipraPAsMunicipios.csv (arquivo csv que alimenta o código python com os municípios, assentamentos e códigos SIPRA)
- 03_contDocsRecebidos.xlsx (planilha gerada pelo código python com as informações dos documentos recebidos pelos assentados)

  04_SO (Pasta referente à quarta página do dashboard)
- 04_1_quantificadorPareceres.py (código python que identifica quantifica os documentos recebidos dos assentados pela SO)
- 04_2_copiadorPlanilhaPareceres.py (código python que copia a planilha de informações do SharePoint para o repositório do GitHub)
- 04_codsipraPAsMunicipios.csv (arquivo csv que alimenta o código python com os municípios, assentamentos e códigos SIPRA)
- 04_contPareceres.xlsx (planilha gerada pelo código python com as informações dos documentos recebidos pelos assentados)
