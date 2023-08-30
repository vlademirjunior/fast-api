from fastapi import FastAPI, Request, status, UploadFile
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta, timezone
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
from aiofile import async_open
from uuid import uuid4

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')
media = Path('media') # o Path informa que o diretório está no mesmo diretório que o atual = main.

@app.get('/')
async def index(request: Request, usuario: str = 'Vlademir Santos'):
    diferenca = timedelta(hours=-3) # utc-3
    fuso_horario = timezone(diferenca)
    data_atual = datetime.now(tz=fuso_horario)
    context = {
        'request': request,
        'data_atual': data_atual,
        'usuario': usuario
    }

    return templates.TemplateResponse('index.html', context=context)

@app.get('/assinatura')
async def assinatura(request: Request, id: str = 'Assinatura XYZ'):
    context = {
        'request': request,
        'id': id
    }

    return templates.TemplateResponse('assinatura.html', context=context)

@app.post('/newsletter')
async def newsletter(request: Request):
    form = await request.form()
    email: str = form.get('email')
    
    print(f"Cliente quer se cadastrar na newsletter: {email}")

    return RedirectResponse(str(request.url_for('index')) + '#contact', status_code=status.HTTP_303_SEE_OTHER)

@app.post('/upload')
async def upload(request: Request):
    form = await request.form()
    email: str = form.get('email')
    arquivo: UploadFile = form.get('arquivo')
    print(f"Nome do arquivo: {arquivo.filename}")
    print(f"Tipo do arquivo: {arquivo.content_type}")
    
    print(f"Cliente quer se cadastrar na newsletter: {email}")

    arquivo_ext: str = arquivo.filename.split('.')[1]
    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}" #evitar override do arquivo

    async with async_open(f"{media}/{novo_nome}", "wb") as afile: #a de async w de write e b de binary
        await afile.write(arquivo.file.read())# file é um binary que é o content

    # obs.: por padrão os arquivos carregados nao ficam disponiveis para uso, para deixar para uso temos que
    # configurar da mesma forma que foi feito com static.
    context = {
        'request': request,
        'imagem': novo_nome,
    }
    return templates.TemplateResponse('assinatura.html', context=context)