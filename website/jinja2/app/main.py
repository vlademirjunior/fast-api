from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from time import time
from functools import wraps

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')


def rate_limited(max_calls: int, time_frame: int, route: str):
    def decorator(func):
        calls = []

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            now = time()
            calls_in_time_frame = [
                call for call in calls if call > now - time_frame]
            if len(calls_in_time_frame) >= max_calls:
                return "Excedeu o limite de acessos."

            calls.append(now)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


@app.get('/')
@rate_limited(max_calls=60, time_frame=60, route="/")
async def index(request: Request):
    return templates.TemplateResponse('index.html', context={
        'request': request,
    })


@app.get('/assinatura/{assinatura:str}')
@rate_limited(max_calls=60, time_frame=60, route="/assinatura")
async def assinatura(request: Request, assinatura: str):
    return templates.TemplateResponse(f'assinatura-{assinatura}.html', context={
        'request': request
    })


@app.post('/newsletter')
@rate_limited(max_calls=60, time_frame=60, route="/newsletter")
async def newsletter(request: Request):
    import re

    form = await request.form()
    email: str = form.get('email')
    # Regez para validar email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if (re.fullmatch(regex, email)):
        from tinydb import TinyDB, Query
        db = TinyDB('newsletter.json')
        Newsletter = Query()
        email_cadastrado = len(db.search(Newsletter.email == email)) > 0
        if not email_cadastrado:
            db.insert({'email': email})

    return RedirectResponse(str(request.url_for('index')) + '#contact', status_code=status.HTTP_303_SEE_OTHER)
