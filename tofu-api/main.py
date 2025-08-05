# Importa as dependências necessárias do FastAPI, Pathlib, subprocessos e módulos personalizados.
from fastapi import FastAPI, HTTPException, Body, Query
from pathlib import Path
import subprocess
from makefile_parser import parse_makefile
from modules_handler import list_modules
from makefile_parser import parse_makefile

# Inicializa a aplicação FastAPI.
app = FastAPI()

# Define o diretório base do projeto, que é o diretório pai da pasta atual (tofu-api).
# Exemplo: /home/user/projeto
BASE_DIR = Path(__file__).resolve().parent.parent


# Endpoint para definir o diretório base do projeto.
@app.post("/set_base_path")
def set_base_path(path: str = Body(..., embed=True)):
    global BASE_DIR
    new_path = Path(path).resolve()
    # Verifica se o novo caminho existe e é um diretório.
    if not new_path.exists() or not new_path.is_dir():
        raise HTTPException(status_code=404, detail="Diretório inválido")
    BASE_DIR = new_path
    # Retorna mensagem informando o novo diretório base.
    return {"mensagem": f"Diretório base definido para: {BASE_DIR}"}


# Endpoint para obter o diretório base atual.
@app.get("/get_base_path")
def get_base_path():
    # Retorna o diretório base como string.
    return {"diretorio_base": str(BASE_DIR)}


# Endpoint para listar os subdiretórios que possuem Makefile, exceto o diretório da API.
@app.get("/lista_diretorio")
def listar_diretorios():
    """
    Lista todos os subdiretórios no diretório base que contenham Makefile,
    exceto o próprio diretório da API (tofu-api).
    """
    modulos = list_modules(BASE_DIR)
    # Retorna a lista de módulos encontrados.
    return {"modulos": modulos}


# Endpoint para listar os comandos disponíveis no Makefile de um módulo específico.
@app.get("/modules/{module_name}/commands")
def listar_comandos_makefile(module_name: str):
    module_path = BASE_DIR / module_name
    makefile = module_path / "Makefile"
    # Verifica se o Makefile existe no módulo.
    if not makefile.exists():
        raise HTTPException(status_code=404, detail="Makefile não encontrado")
    # Retorna os comandos disponíveis no Makefile.
    return {"comandos_disponiveis": parse_makefile(makefile)}


# Endpoint para executar um comando do Makefile em um módulo específico, podendo passar tfvars.
@app.post("/modules/{module_name}/run/{command}")
def executar_comando(module_name: str, command: str, tfvars: str = Query(None)):
    module_path = BASE_DIR / module_name
    # Verifica se o Makefile existe no módulo.
    if not (module_path / "Makefile").exists():
        raise HTTPException(status_code=404, detail="Makefile não encontrado")

    # Define a variável de ambiente TFVARS, usando o valor passado ou um padrão.
    env = {"TFVARS": tfvars or "default.tfvars"}
    try:
        # Executa o comando do Makefile usando subprocess.run.
        result = subprocess.run(
            ["make", command],
            cwd=module_path,
            capture_output=True,
            text=True,
            check=True,
            env={**env, **dict(**subprocess.os.environ)}
        )
        # Retorna o resultado da execução do comando.
        return {"output": result.stdout}
    except subprocess.CalledProcessError as e:
        # Em caso de erro, retorna o stderr como detalhe do erro.
        raise HTTPException(status_code=400, detail=e.stderr)
