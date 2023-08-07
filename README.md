
- openssl rand -hex 32 -> gera string em base64 com 64 caracteres hexadecimal 32 bits para apikey
- poetry add fastapi fastapi-versioning uvicorn requests aiohttp sqlalchemy psycopg2-binary pytest alembic python-decouple httpx passlib python-jose python-multipart fastapi-pagination
- poetry env info -p
    - adiciona o /bin/python no final e dar um find no select interpreter

- Rodar o programa: uvicorn main:app --reload
    - --reload faz recarregar automaticamente quando atualizar o codigo
    - --app é o nome da instancia do fastapi
    - main é o nome do arquivo

- toda vez antes de rodar o uvicorn dar um "source .env" para carregar as variaveis de ambiente para exportar todas as variaveis dentro do arquivo .env para dentro do sistema operacional
    - echo $ALPHAVANTAGE_APIKEY


- sqlalchemy é o ORM para interagir com banco de dados junto com psycopg2-binary
- pytest para teste unitario
- alembic para migrations do banco
- python-decouple para gerenciar as variaveis de ambiente melhor que a forma nativa.

- docker-compose run app

- todos os comandos agora sao dentro do container exceto instalacao de bibliotecas, instalar fora do container.
- docker-compose run --user 1000 app sh -c 'alembic init migrations' no linux
- docker-compose run --user 1000 app sh -c 'alembic init migrations' no mac (id -u no terminal) 
- docker-compose run --user 1000 app sh -c 'alembic revision --autogenerate -m "add categories table"'  -> gera migration script file mas nao executa/persiste no banco,é apenas a revisao
- docker-compose run --user 1000 app sh -c 'alembic upgrade head'  -> executa persistindo no banco
- docker-compose run --user 1000 app sh -c 'pytest'
- docker-compose run --user 1000 app sh -c 'pytest -k test_add_category_use_case'  -> teste especifico


# sempre que der erro: no module named 'xxxxxxx' precisamos instalar com poetry
- poetry add httpx
- docker-compose build -> sempre que atualizar o poetry pois precisa jogar para dentro da nossa imagem a lib instalada
- poetry add passlib -> hash
- poetry add python-jose -> para jwt no python
- docker-compose build -> sempre que atualizar o poetry pois precisa jogar para dentro da nossa imagem a lib instalada
- poetry add python-multipart -> para trabalhar com formulario no python




WXREA:
rm /home/meusuuario/.docker/config.json -> comando quando dar erro de credentials do docker ao rodar docker-compose up -d ou docker-compose build

HS256