from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter
from datetime import datetime
import requests
import aiohttp

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

url = "http://localhost:8000"


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/registrar")
def registar(request: Request):
    msj = ""
    return templates.TemplateResponse("crear_usuario.html", {"request": request, "msj": msj})


@router.post("/registrar")
async def registar(request: Request):
    form = await request.form()
    usuario = {
        "username": form.get('username'),
        "password": form.get('password'),
        "nombre": form.get('nombre'),
        "apellido": form.get('apellido'),
        "direccion": form.get('direccion'),
        "telefono": form.get('telefono'),
        "correo": form.get('correo')
    }
    print(usuario)
    url_post = f"{url}/user/"
    print(f"{url_post}")
    # r = requests.post(url=url_post, json=usuario)
    async with aiohttp.ClientSession() as session:
        response = await session.request(method="POST", url=url_post, json=usuario)
        response_json = await response.json()
        if "Respuesta" in response_json:
            msj = "Usuario Creado Satisfactoriamente"
            type_alert = "success"
        else:
            msj = "Usurio no fue creado"
            type_alert = "danger"
        return templates.TemplateResponse("crear_usuario.html", {"request": request, "msj": msj, "type_alert": type_alert})
