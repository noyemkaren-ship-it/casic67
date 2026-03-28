from fastapi import APIRouter, Response, Request, HTTPException
from api.services import get_all_users, reg, first_game_slot, get_user_balance
from schemas.user import User, UserPatch
from database.UserRepository import UserRepository
from urllib.parse import quote, unquote

router = APIRouter()
user_repo = UserRepository()

@router.get("/users")
async def get_users_endpoint():
    return get_all_users()

@router.post("/register")
async def register_user(user: User, response: Response):
    result = reg(name=user.name, password=user.password)
    if result and not isinstance(result, dict):
        # Кодируем имя для cookie (поддержка русских букв)
        encoded_name = quote(user.name)
        response.set_cookie(
            key="user", 
            value=encoded_name,
            httponly=False,
            max_age=3600,
            path="/"
        )
        return {"message": "Registration successful", "user": result}
    return result

@router.post("/login")
async def login_user(user: User, response: Response):
    if user_repo.login(user.name, user.password):
        # Кодируем имя для cookie (поддержка русских букв)
        encoded_name = quote(user.name)
        response.set_cookie(
            key="user", 
            value=encoded_name,
            httponly=False,
            max_age=3600,
            path="/"
        )
        return {"message": "Login successful"}
    return {"message": "Invalid credentials"}

@router.get("/first_game_slot")
async def first_game_slot_endpoint(request: Request, bet: int = 100):
    username_encoded = request.cookies.get("user")
    
    if not username_encoded:
        raise HTTPException(status_code=401, detail="Please login first")
    
    username = unquote(username_encoded)
    
    user = user_repo.get_by_name(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = first_game_slot(username, bet)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/user/{name}/balance")
async def get_balance(name: str):
    balance = get_user_balance(name)
    if balance is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"name": name, "balance": balance}

@router.patch("/user/balance")
async def update_balance(user: UserPatch):
    user_repo.patch_balance_user(user.name, user.balance)
    return {"message": "Balance updated successfully"}