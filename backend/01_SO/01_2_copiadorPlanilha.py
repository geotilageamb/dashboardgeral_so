import shutil
import os

# Caminhos dos arquivos
caminho_sharepoint = 'D:/ufpr.br/Intranet do LAGEAMB - TRANSVERSAIS/03_equipeGEOTI/08_automacoes/01_SO/01_laudos_SO_infos.xlsx'
caminho_repositorio = 'C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so/01_laudos_SO_infos.xlsx'

# Copiar e substituir o arquivo do SharePoint para o repositório
shutil.copyfile(caminho_sharepoint, caminho_repositorio)

# Caminho para o executável do Git
git_executable = '"C:/Program Files/Git/cmd/git.exe"'

# Navegar até o diretório do repositório e executar comandos Git
os.system(f'cd C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so && {git_executable} pull --no-edit')
os.system(f'cd C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so && {git_executable} add 01_laudos_SO_infos.xlsx')
os.system(f'cd C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so && {git_executable} commit -m "Atualização do arquivo de laudos"')
os.system(f'cd C:/Users/CoordenaçãodeTidoLag/Desktop/dashboardgeral_so && {git_executable} push')
