from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()


conn = sqlite3.connect("data/database.db")
cursor = conn.cursor()


app.mount("/static", StaticFiles(directory="templates/static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request, login: str = None):
    sql = "SELECT * FROM user WHERE login='{}';".format(login)
    try:
        abo = cursor.execute(sql).fetchall()
    except sqlite3.Warning as e:
        abo = cursor.executescript(sql).fetchall()
    if len(abo):
        return templates.TemplateResponse("index.html", {"request": request, "user": abo[0][2]})
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/fixed")
async def root(request: Request, login: str = None):
    sql = "SELECT * FROM user WHERE login=?"
    try:
        abo = cursor.execute(sql, (login,)).fetchall()
    except sqlite3.Warning as e:
        abo = cursor.executescript(sql).fetchall()
    if len(abo):
        return templates.TemplateResponse("index.html", {"request": request, "user": abo[0][2]})
    return templates.TemplateResponse("index.html", {"request": request})
# ';drop table article;--