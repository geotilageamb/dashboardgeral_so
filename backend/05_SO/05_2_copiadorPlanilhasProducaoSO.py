import shutil
import os

# Caminhos dos arquivos
caminho_sharepoint = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/05_SO/05_contPlanilhas.xlsx'
caminho_repositorio = 'C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so/05_contPlanilhas.xlsx'

# Copiar e substituir o arquivo do SharePoint para o repositório
shutil.copyfile(caminho_sharepoint, caminho_repositorio)

# Caminho para o executável do Git
git_executable = '"C:/Program Files/Git/cmd/git.exe"'

# Navegar até o diretório do repositório e executar comandos Git
os.system(f'cd C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so && {git_executable} pull --no-edit')
os.system(f'cd C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so && {git_executable} add 05_contPlanilhas.xlsx')
os.system(f'cd C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so && {git_executable} commit -m "Atualização do arquivo de planilhas"')
os.system(f'cd C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so && {git_executable} push')