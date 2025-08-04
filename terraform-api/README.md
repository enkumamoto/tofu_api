# 🐍 Terraform API

## 🚀 `main.py` - O Capitão da Nave

**Função:** Coordena toda a operação da API.

### O que este cara faz:
- 🌐 **Gerencia todos os endpoints** - É o rosto da API, quem conversa com o mundo exterior
- 📁 **Controla o diretório base** - Sabe onde estão seus módulos Terraform
- 🎯 **Executa comandos** - Quando você pede "roda um tf-plan", ele que faz acontecer
- 🔗 **Orquestra os outros arquivos** - Chama os arquivos quando necessário

### Endpoints que ele oferece:
```python
GET  /lista_diretorio              # "Quais módulos temos?"
GET  /modules/{nome}/commands      # "Que comandos posso usar?"
POST /modules/{nome}/run/{comando} # "Executa isso pra mim!"
POST /set_base_path               # "Muda o diretório base"
GET  /get_base_path               # "Onde estamos trabalhando?"
```

### Como ele funciona:
```python
# Quando você pede para executar um comando:
# 1. Verifica se o módulo existe
# 2. Configura as variáveis de ambiente
# 3. Roda o comando com subprocess.run()
# 4. Te devolve o resultado (ou o erro, se algo deu ruim 😅)
```

---

## 🔍 `modules_handler.py` - O Explorador

**Função:** Encontrar módulos Terraform no projeto.

### O que este cara faz:
- 🕵️ **Vasculha diretórios** - Procura por pastas que tenham Makefile
- 🚫 **Filtra o que interessa** - Ignora a pasta `terraform-api`
- 📋 **Organiza a lista** - Te entrega uma lista limpa dos módulos disponíveis

### Como ele trabalha:
```python
def list_modules(base_path: Path):
    # Traduzindo: "Me diz todas as pastas que têm Makefile"
    return [
        pasta.name for pasta in base_path.iterdir()
        if pasta.is_dir()                    # É uma pasta? ✅
        and (pasta / "Makefile").exists()    # Tem Makefile? ✅
        and pasta.name != "terraform-api"   # Não é nossa própria pasta? ✅
    ]
```

### Exemplo prático:
```
📁 Projeto/
├── 1.0-RG/ (tem Makefile) ✅
├── 2.0-BLOB_STORAGE/ (tem Makefile) ✅  
├── terraform-api/ (nossa pasta) ❌
└── docs/ (sem Makefile) ❌

Resultado: ["1.0-RG", "2.0-BLOB_STORAGE"]
```

---

## 📖 `makefile_parser.py` - O Tradutor

**Função:** Ler Makefiles e descobrir quais comandos você pode usar.

### O que este cara faz:
- 📝 **Lê Makefiles linha por linha** - Como um detetive investigando pistas
- 🔎 **Usa regex para encontrar targets** - Procura por padrões como `comando:`
- 🙈 **Ignora comandos internos** - Skipa coisas que começam com "." 
- 📊 **Te entrega uma lista limpa** - Só os comandos que realmente importam

### Como ele decifra um Makefile:
```python
# Para cada linha do Makefile:
match = re.match(r"^([a-zA-Z0-9_-]+):", line)

# Se encontrar algo como "tf-plan:", ele pensa:
# "Opa! Achei um comando chamado 'tf-plan'!"
```

### Exemplo em ação:
```makefile
# Makefile original:
tf-setup:
    @echo "Inicializando..."
    
tf-plan:
    @echo "Criando plano..."
    
.PHONY: help  # <- Este ele ignora (começa com .)

# Resultado: ["tf-setup", "tf-plan"]
```

---

## 🤝 Como Eles Trabalham em Equipe

Imagine uma conversa típica entre os três:

**👤 Usuário:** "Quais módulos tenho disponíveis?"

**🚀 main.py:** "Deixa comigo! Ei, modules_handler, me ajuda aí!"

**🔍 modules_handler.py:** "Beleza! Achei: 1.0-RG, 2.0-BLOB_STORAGE, 4.0-DATABASE"

**🚀 main.py:** "Obrigado! Aqui está a resposta!"

---

**👤 Usuário:** "Que comandos posso usar no módulo 1.0-RG?"

**🚀 main.py:** "makefile_parser, sua vez de brilhar!"

**📖 makefile_parser.py:** "Deixa eu ver... tf-setup, tf-plan, tf-apply, tf-destroy!"

**🚀 main.py:** "Perfeito! Cliente atendido!"

---

**👤 Usuário:** "Executa tf-plan no 1.0-RG!"

**🚀 main.py:** "Agora é comigo! subprocess.run(['make', 'tf-plan']) e... pronto! ✨"

## 🎯 Resumo da Galera

| Arquivo | Especialidade | Bordão |
|---------|--------------|---------|
| `main.py` | Gerenciar a API | "Eu coordeno tudo!" 👑 |
| `modules_handler.py` | Encontrar módulos | "Eu sei onde estão!" 🗺️ |
| `makefile_parser.py` | Ler Makefiles | "Eu decifro códigos!" 🔍 |

## 💡 Dicas para Desenvolvedores

**Quer mexer no código?**

- 🆕 **Novo endpoint?** → Mexe no `main.py`
- 🔍 **Nova lógica de busca?** → `modules_handler.py` é seu amigo
- 📖 **Novo tipo de arquivo para ler?** → `makefile_parser.py` pode ajudar

**Regra de ouro:** Cada arquivo cuida das suas funções. Mantenha assim e todos ficarão organizados e funcionais! 😊

---

## 📚 Documentações das Tecnologias Utilizadas

### 🐍 Python & Bibliotecas Core
- **[Python](https://docs.python.org/3/)** - A linguagem principal da nossa API
- **[pathlib](https://docs.python.org/3/library/pathlib.html)** - Para manipulação de caminhos de arquivos e diretórios
- **[subprocess](https://docs.python.org/3/library/subprocess.html)** - Para executar comandos do sistema (como `make`)
- **[re (regex)](https://docs.python.org/3/library/re.html)** - Para encontrar padrões nos Makefiles

### 🚀 Framework Web
- **[FastAPI](https://fastapi.tiangolo.com/)** - O framework web que faz toda a mágica da API
  - **[Documentação em Português](https://fastapi.tiangolo.com/pt/)** - Para quem prefere em português! 🇧🇷
- **[Uvicorn](https://www.uvicorn.org/)** - O servidor ASGI que roda nossa aplicação
- **[Pydantic](https://docs.pydantic.dev/)** - Validação de dados (vem junto com o FastAPI)

### 🛠️ Ferramentas de Infraestrutura
- **[Terraform](https://developer.hashicorp.com/terraform/docs)** - Para provisionar infraestrutura como código
- **[OpenTofu](https://opentofu.org/docs/)** - Fork open-source do Terraform
- **[Make](https://www.gnu.org/software/make/manual/)** - Para automatizar comandos repetitivos

### ☁️ Azure
- **[Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)** - Para autenticação e gerenciamento do Azure
- **[Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)** - Provider específico para Azure

### 🔧 Utilitários
- **[python-multipart](https://github.com/andrew-d/python-multipart)** - Para lidar com uploads de arquivos (se necessário)
- **[aiofiles](https://github.com/Tinche/aiofiles)** - Para operações assíncronas com arquivos

### 📖 Recursos Adicionais
- **[HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)** - Para entender os códigos de resposta
- **[REST API Design](https://restfulapi.net/)** - Boas práticas para APIs REST
- **[JSON](https://www.json.org/json-en.html)** - Formato de dados que usamos nas respostas

## 🎓 Para Começar a Estudar

Se você é novo nessas tecnologias, recomendo começar por:

1. **[Tutorial FastAPI](https://fastapi.tiangolo.com/tutorial/)** - Super didático e bem explicado
2. **[Terraform Getting Started](https://developer.hashicorp.com/terraform/tutorials/aws-get-started)** - Conceitos básicos
3. **[Python pathlib tutorial](https://realpython.com/python-pathlib/)** - Para manipular arquivos como um pro

---

*Agora você tem todas as referências para se aprofundar em cada tecnologia! Happy coding! 🎉*
