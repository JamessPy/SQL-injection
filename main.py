from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pyodbc

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# MSSQL bağlantısı
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=TestDB;"
    "Trusted_Connection=yes;"
)
@app.get("/")
def root():
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    #TEHLİKELİ: f-string ile dinamik SQL (SQL Injection'a açık!)
    query = f"SELECT * FROM Users WHERE username = '{username}' AND password = '{password}'"
    print("Sorgu:", query) 

    try:
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()
    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": f"Hata: {str(e)}"
        })

    if user:
        return RedirectResponse(url="/index", status_code=302)
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Kullanıcı adı veya şifre hatalı!"
        })

@app.get("/index", response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
