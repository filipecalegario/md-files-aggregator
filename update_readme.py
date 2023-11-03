import os
import re
from datetime import datetime
import subprocess

# Caminho para o README
README_PATH = "README.md"

# Cabecalho do README
readme_content = "# Índice dos Artigos\n\n"

# Lista para armazenar tuplas de título e data de modificação
articles = []

# Encontrar todos os arquivos Markdown e extrair os títulos
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".md") and file != "README.md":
            file_path = os.path.join(root, file)
            # Obter a data de modificação do arquivo
            # Obter a data do último commit que modificou o arquivo
            last_commit_date = subprocess.check_output(
                ["git", "log", "-1", "--format=%cd", file_path],
                universal_newlines=True
            ).strip()
            datetime_object_commit = datetime.strptime(last_commit_date, '%a %b %d %H:%M:%S %Y %z')
            datetime_object_mod = os.path.getmtime(file_path)
            datetime_object = max(datetime_object_commit, datetime_object_mod)
            with open(file_path, 'r', encoding='utf-8') as f:
                # Extrair o primeiro título de cada arquivo
                title = re.findall(r'^# (.+)', f.readline())
                if title:
                    # Adicionar título e data de modificação à lista
                    articles.append((title[0], datetime_object, file_path))

# Ordenar artigos do mais novo para o mais antigo
articles.sort(key=lambda x: x[1], reverse=True)

# Adicionar títulos ordenados ao README
for title, _, file_path in articles:
    print(title)
    relative_path = os.path.relpath(file_path)
    readme_content += f"- [{title}]({relative_path})\n"

# Atualizar o README.md
with open(README_PATH, 'w', encoding='utf-8') as f:
    f.write(readme_content)

# Adicionar alterações ao commit
subprocess.run(['git', 'add', README_PATH])
subprocess.run(['git', 'commit', '-m', 'Atualizar README com índice dos artigos'])
subprocess.run(['git', 'push'])
