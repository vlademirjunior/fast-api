# Variavéis de Ambiente
- Copie .env-example para .env

# SECRET KEY
- gera string em base64 com 64 caracteres hexadecimal 32 bits para secret key
`openssl rand -hex 32`

# Rodando
`poetry install`
`docker-compose up`
- Caso instale novas dependencias pode ser necessário reconstruir a imagem docker
`docker-compose up --build`

# Instalando e configurando o Pyenv
- Garantir que todas as dependecias estão instaladas
`sudo apt-get update; sudo apt-get install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev`

- Baixar e executar o script de instalação
`curl https://pyenv.run | bash`

- Adicione o seguinte script no arquivo ~/.bashrc
`# pyenv
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"`

- source ~/.bashrc
- Feche e abre o shell

- Valide se esta tudo certo
`pyenv --version`

## Comandos básicos pyenv
`
lista as versões de python disponíveis
pyenv install -l

instala uma versão
pyenv install <version>

mostra versão instalada
pyenv global

define uma versão
pyenv global <version>

lista versões instaladas
pyenv versions
`

Ex.:
- Instalar o python 3.11.0 em um ambiente virtual
`pyenv install 3.11.0`
- Conferir instalação se tiver aparecendo a versão 3.11.0
`pyenv versions`
- Definir a versão como atual
`pyenv global 3.11.0`
- Verificar se está tudo certo
`pyenv global`

# Poetry instalação e configuração
- Instalação seguindo a documentação
`https://python-poetry.org/docs/#installation`

## Como usar
- Em uma pasta zerada, para iniciar um projeto poetry
`poetry init`
-- Só enter até o fim se quiser...

- Iniciar o ambiente virtual
`poetry shell`
-- Aqui se ja existir um ambiente virtual você pode trocar e se não existir você pode criar.
-- se tiver no vscode tem que dar um `CTRL + P` e em seguida `> Python: Select Interpreter` e em seguida selecionar 
-- o ambiente criado/activate (poetry)


- Adicionar dependencias
`poetry add fastapi uvicorn Jinja2 python-multipart aiofile`


### Imagens free
- https://freepngimg.com/