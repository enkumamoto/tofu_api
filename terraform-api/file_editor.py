# Importa a classe Path do módulo pathlib, que permite manipular caminhos de arquivos e diretórios de forma orientada a objetos.
from pathlib import Path


# Função que lista arquivos editáveis em um diretório especificado por 'module_path'.
# Ela considera como editáveis os arquivos com extensões ".tf", ".tfvars" e ".tfbackend".
# Retorna uma lista com os nomes dos arquivos que possuem essas extensões.
def list_editable_files(module_path: str):
    valid_extensions = [".tf", ".tfvars", ".tfbackend"]
    return [str(f.name) for f in Path(module_path).iterdir() if f.suffix in valid_extensions]


# Função que lê o conteúdo de um arquivo.
# Recebe como parâmetro um objeto Path representando o caminho do arquivo.
# Retorna o conteúdo do arquivo como uma string.
def read_file_content(file_path: Path):
    return file_path.read_text()


# Função que escreve um conteúdo em um arquivo.
# Recebe como parâmetros um objeto Path (caminho do arquivo) e uma string 'content' (conteúdo a ser escrito).
# Substitui o conteúdo do arquivo pelo novo conteúdo fornecido.
def write_file_content(file_path: Path, content: str):
    file_path.write_text(content)
