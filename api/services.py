from database.UserRepository import UserRepository
import random

user_repo = UserRepository()
    

def reg(name: str, password: str):
    result = user_repo.create_user(name, password)
    if result:
        return {"message": "User is created!"}
    return result


def get_all_users():
    return user_repo.get_all()

def get_user_by_name(name: str):
    return user_repo.get_by_name(name)

def first_game_slot(name: str, bet: int = 100):
    """Игровая логика"""
    user = user_repo.get_by_name(name)
    if not user:
        return {"error": "User not found"}
    
    if user.balance < bet:
        return {"error": f"Insufficient balance. You have {user.balance}, need {bet}"}
    
    slot = random.randint(1, 10)
    
    if slot == 1:  # Джекпот
        win_amount = bet * 5
        new_balance = user.balance + win_amount
        user_repo.patch_balance_user(name, new_balance)
        return {
            "message": f"JACKPOT! You won {win_amount}!",
            "result": "jackpot",
            "bet": bet,
            "win_amount": win_amount,
            "balance_change": win_amount,
            "new_balance": new_balance
        }
    elif slot <= 4:  # Выигрыш
        win_amount = bet * 2
        new_balance = user.balance + win_amount
        user_repo.patch_balance_user(name, new_balance)
        return {
            "message": f"You win! +{win_amount}",
            "result": "win",
            "bet": bet,
            "win_amount": win_amount,
            "balance_change": win_amount,
            "new_balance": new_balance
        }
    elif slot <= 6:  # Возврат
        return {
            "message": "It's a draw! Bet returned",
            "result": "draw",
            "bet": bet,
            "balance_change": 0,
            "new_balance": user.balance
        }
    else:  # Проигрыш
        new_balance = user.balance - bet
        user_repo.patch_balance_user(name, new_balance)
        return {
            "message": f"You lose! -{bet}",
            "result": "lose",
            "bet": bet,
            "balance_change": -bet,
            "new_balance": new_balance
        }
        
def get_user_balance(name: str):
    user = user_repo.get_by_name(name)
    if user:
        return user.balance
    return None
