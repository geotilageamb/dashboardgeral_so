# Documentação sobre as metas e produtos da Supervisão Ocupacional (SO) conforme Plano de Trabalho de 09/2024 e 
sobre os códigos python e planilhas que alimentam esses indicadores.


## Nome original das planilhas geradas pelos códigos python que extraem as infomações

01_laudos_SO_infos.xlsx
Meta 2.1 - Produtos 2.1.1 e 2.1.2

02_contPGT.xlsx
Meta 2.2 - Produtos 2.2.1, 2.2.2, 2.2.3 e 2.2.4

03_contDocsRecebidos.xlsx
Meta 2.2 - Produto 2.2.1 - Etapa 2.2.1.1

04_contPareceres.xlsx
Meta 2.3 - Produtos 2.3.1 e 2.3.2


05_contPlanilhas.xlsx
Meta 2.4 - Produto 2.4.1

## Metas e produtos da SO conforme Plano de Trabalho de 09/2024

### Meta 2.1 (Supervisão Ocupacional de lotes em Projetos de Assentamento de Reforma Agrária)

├── 2.1.1 Laudo de supervisão ocupacional in loco (Total a atingir: 4739)

└── 2.1.2 Laudo de supervisão ocupacional mutirão (Total a atingir: 2746)

### Meta 2.2 (Analisar solicitações de regularização de ocupantes)

├── 2.2.1 Relatórios de conformidades inseridos nos respectivos processos SEI de ocupantes irregulares (Total a atingir: 2246)

│   └── 2.2.1.1 Coleta suplementar de documentos via canais de atendimento (Total a atingir: X)

├── 2.2.2 Notificação de documentos pendentes de ocupantes irregulares (Total a atingir: 674)

├── 2.2.3 Relatório de conformidades de ocupantes irregulares notificados (Total a atingir: 337)

└── 2.2.4 Parecer favorável ou desfavorável à regularização via PGT ou assinado e inserido no SEI (Total a atingir: 1622)

### Meta 2.3 (Analisar a atualização e regularização cadastral de beneficiários)

├── 2.3.1 Parecer com vistas à atualização e regularização cadastral de beneficiários do PNRA (Total a atingir: 4239)

└── 2.3.2 Relatório com vistas ao desbloqueio de beneficiários do PNRA junto ao TCU (Total a atingir: 500)

### Meta 2.4 (Planejar, monitorar e sistematizar as supervisões ocupacionais e as respectivas atualizações de beneficiários e regularizações de ocupantes durante o período de atendimento)

└── 2.4.1 Planilha de monitoramento das demandas levantadas, circunstâncias encontradas durante a supervisão, movimentações dos processos e encaminhamentos (Total a atingir: 129)

### Legenda

├── Verde - o respectivo documento segue sendo o vigente

└── Laranja - há previsão de mudança no documento padrão


## Documentação sobre as colunas das planilhas

### Planilha 1 (Meta 2.1)

├── Código SIPRA (código único que todo assentamento tem no sistema do INCRA, extraído de arquivo CSV)

├── Município (extraído de arquivo CSV)

├── Assentamento (nome do assentamento extraído de dentro do próprio laudo)

├── Lote (número do lote do assentamento, é numérico mas pode ter letras e às vezes até traço "-", extraído do próprio laudo)

├── Arquivo (nome do arquivo do laudo conforme ele está no SharePoint)

├── Tipo de Laudo (tipo de laudo extraído de dentro do próprio laudo)

├── Data (data de elaboração do laudo extraída de dentro do próprio laudo)

├── Técnico (nome do técnico que elaborou o laudo extraído de dentro do próprio laudo)

└── Modalidade (modalidade da supervisão ocupacional, que pode ser vistoria in loco ou mutirão, informação cruzada entre a data do laudo e datas dos campos da SO no CSV)

### Planilha 2 (Meta 2.2)
├── Tipo de documento PGT (tipo do documento conforme qual produto ele representa, extraído de dentro do próprio documento e renomeado por código python)

├── Assentamento (nome do assentamento extraído de dentro do próprio documento)

├── Município (extraído de arquivo CSV)

├── Código SIPRA (código único que todo assentamento tem no sistema do INCRA, extraído de arquivo CSV)

├── Nome T1 (primeiro nome do Titular 1 do lote, extraído de dentro do próprio documento e colocado também no nome do arquivo PDF para facilitar identificação pela SO)

├── Autenticador (código autenticador do documento extraído de dentro do próprio documento)

├── Objetivo (informação para diferenciar relatórios de conformidade que são para titulação ou regularização, extraído de dentro do próprio documento)

└── Segundo Relatório (booleano "Sim/Não" para identificar segundos relatórios de conformidades para o mesmo assentado, o que representa um produto por si só, informação feita identificando se já havia um relatório dentro da pasta)

### Planilha 3 (Meta 2.2 - Produto 2.2.1 - Etapa 2.2.1.1)

├── Caminho (caminho completo do arquivo)

├── Município (extraído de arquivo CSV)

├── Assentamento (nome do assentamento extraído do caminho do arquivo, que menciona o nome do assentamento, comparado com arquivo CSV para correção)

├── Código SIPRA (código único que todo assentamento tem no sistema do INCRA, extraído de arquivo CSV)

├── Arquivo (nome do arquivo)

└── Lote (número do lote do assentamento, é numérico mas pode ter letras e às vezes até traço "-", extraído do caminho)

### Planilha 4 (Meta 2.3)

├── Lote (número do lote do assentamento, é numérico mas pode ter letras e às vezes até traço "-", extraído do nome do arquivo)

├── Assentamento (nome do assentamento extraído do nome do arquivo)

├── Código SIPRA (código único que todo assentamento tem no sistema do INCRA, extraído de arquivo CSV)

├── Tipo (informação para identificar pareceres padrão e pareceres para desbloqueio, extraído de dentro do parecer)

└── Caminho (caminho completo do arquivo)

### Planilha 5 (Meta 2.4)

├── Município (extraído do caminho do arquivo e comparado com arquivo CSV para correção)

├── Assentamento (extraído do caminho do arquivo e comparado com arquivo CSV para correção)

├── Código SIPRA (código único que todo assentamento tem no sistema do INCRA, extraído de arquivo CSV)

└── Planilha de monitoramento (booleano "Sim/Não" identificando se há planilha para o assentamento ou não)


## Documentação sobre os códigos python backend que fazem ajustes e levantamento dos indicadores

### 01_1_infosLaudosModalidade.py

└── Extrai as informações e gera a Planilha 1 (bibliotecas os, re, pandas e PyPDF2)

### 01_2_copiadorPlanilha.py

└── Copia a planilha gerada pelo código 01_1_infosLaudosModalidade.py do SharePoint para o GitHub (bibliotecas shutil e os)

### 02_1_renomeador_docsPGTWEB.py

└── Renomeia os arquivos referentes a meta 2.2 conforme regras definidas (bibliotecas os, pandas, PyPDF2, re, shutil, unidecode, thefuzz, collections e datetime)

### 02_2_quantificadorDocsPGTWEB.py

└── Extrai as informações e gera a Planilha 2 (bibliotecas os, re, time, pandas, thefuzz)

### 02_3_copiadorPlanilhaDocsPGTWEB.py

└── Copia a planilha gerada pelo código 02_2_quantificadorDocsPGTWEB.py do SharePoint para o GitHub (bibliotecas shutil e os)

### 03_1_contarDocsRecebidos.py

└── Extrai as informações e gera a Planilha 3 (bibliotecas os, re, pandas e thefuzz)

### 03_2_copiadorPlanilhaDocsRecebidos.py

└── Copia a planilha gerada pelo código 03_1_contarDocsRecebidos.py do SharePoint para o GitHub (bibliotecas shutil e os)

### 04_1_quantificadorPareceres.py

└── Extrai as informações e gera a Planilha 4 (bibliotecas os, re, pandas, PyPDF2 e thefuzz)

### 04_2_copiadorPlanilhaPareceres.py

└── Copia a planilha gerada pelo código 04_1_quantificadorPareceres.py do SharePoint para o GitHub (bibliotecas shutil e os)

### 05_1_contadorPlanilhasProd_SO.py

└── Extrai as informações e gera a Planilha 5 (bibliotecas os, pandas e thefuzz)

### 05_2_copiadorPlanilhasProducaoSO.py

└── Copia a planilha gerada pelo código 05_1_contadorPlanilhasProd_SO.py do SharePoint para o GitHub (bibliotecas shutil e os)


## Documentação sobre os códigos python frontend que fazem o dashboard em si no Streamlit

### main.py

└── Faz o dashboard inteiro, puxando os códigos de cada aba (biblioteca streamlit)

### a_dashboard_laudos.py

└── Faz a aba do dashboard referente a meta 2.1 (bibliotecas unicodedata, datetime, pandas, plotly.express e streamlit)

### b_dashboard_documentos.py

└── Faz a aba do dashboard referente a meta 2.2 (bibliotecas pandas, plotly.express, plotly.graph_objects e streamlit)

### c_dashboard_docs_recebidos.py

└── Faz a aba do dashboard referente a meta 2.2 - produto 2.2.1 - etapa 2.2.1.1 (bibliotecas unicodedata, pandas,
plotly.express e streamlit)

### d_dashboard_pareceres.py

└── Faz a aba do dashboard referente a meta 2.3 (bibliotecas pandas, plotly.express, plotly.graph_objects e streamlit)

### e_dashboard_planilhas.py

└── Faz a aba do dashboard referente a meta 2.4 (bibliotecas pandas, plotly.express e streamlit)


OBS: Todos os códigos python estão seguindo o estilo PEP8.
