from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from api.router import router
from api.services import get_user_balance
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="KingWeb")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,  # ← Важно для cookie!
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix="/api")

@app.get("/", tags=["page"])
async def read_root(request: Request):
    cookies = request.cookies
    user = cookies.get("user")
    
    if user:

        balance = get_user_balance(user)
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "balance": balance if balance else 0}
        )
    else:
        return templates.TemplateResponse("error.html", {"request": request})
    
    
    
@app.get("/login/page", tags=["page"])
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register/page", tags=["page"])
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/info", tags=["page"])
async def info(request: Request):
    return templates.TemplateResponse("info.html", {"request": request})