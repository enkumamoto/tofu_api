# Importa a classe Path do módulo pathlib, que permite manipular caminhos de arquivos e diretórios de forma orientada a objetos.
from pathlib import Path


# Define a função list_modules que recebe um caminho base (base_path) do tipo Path.
def list_modules(base_path: Path):
    # Retorna uma lista com os nomes dos diretórios dentro de base_path que atendem a certos critérios.
    return [
        # Para cada item (f) encontrado ao iterar sobre base_path...
        f.name for f in base_path.iterdir()
        # Verifica se o item é um diretório.
        if f.is_dir()
        # Verifica se existe um arquivo chamado "Makefile" dentro do diretório.
        and (f / "Makefile").exists()
        # Exclui o diretório chamado "terraform-api" da lista de resultados.
        and f.name != "terraform-api"
    ]
