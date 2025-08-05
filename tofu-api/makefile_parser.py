# Importa o módulo 're' para trabalhar com expressões regulares.
import re
# Importa 'Path' da biblioteca 'pathlib' para manipulação de caminhos de arquivos.
from pathlib import Path


# Função para analisar um arquivo Makefile e retornar os alvos (targets) definidos.
def parse_makefile(makefile_path: Path):
    # Verifica se o caminho do arquivo existe; se não existir, retorna uma lista vazia.
    if not makefile_path.exists():
        return []

    # Inicializa uma lista vazia para armazenar os nomes dos alvos encontrados.
    targets = []
    # Abre o arquivo Makefile para leitura.
    with makefile_path.open() as f:
        # Itera sobre cada linha do arquivo.
        for line in f:
            # Usa expressão regular para encontrar linhas que definem um alvo (target).
            match = re.match(r"^([a-zA-Z0-9_-]+):", line)
            if match:
                # Extrai o nome do alvo do grupo de captura da expressão regular.
                target = match.group(1)
                # Ignora alvos que começam com ponto (.), pois geralmente são internos do Makefile.
                if not target.startswith("."):
                    # Adiciona o alvo à lista de targets.
                    targets.append(target)
    # Retorna a lista de alvos encontrados no Makefile.
    return targets
