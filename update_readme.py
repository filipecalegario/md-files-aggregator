import os
import re
import subprocess

# Caminho para o README
README_PATH = "README.md"

# Cabeçalho do README
readme_content = "# Índice dos Artigos\n\n"

# Encontrar todos os arquivos Markdown e extrair os títulos
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".md") and file != "README.md":
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                # Extrair o primeiro título de cada arquivo
                title = re.findall(r'^# (.+)', f.readline())
                if title:
                    # Adicionar título ao README com um link
                    relative_path = os.path.relpath(file_path)
                    readme_content += f"- [{title[0]}]({relative_path})\n"

# Atualizar o README.md
with open(README_PATH, 'w', encoding='utf-8') as f:
    f.write(readme_content)

# Adicionar alterações ao commit
subprocess.run(['git', 'add', README_PATH])
subprocess.run(['git', 'commit', '-m', 'Atualizar README com índice dos artigos'])
subprocess.run(['git', 'push'])
