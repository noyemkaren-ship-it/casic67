// Получаем имя пользователя из cookie
function getCookie(name) {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

// Функция игры
async function Spin() {
    const username = getCookie('user');
    
    if (!username) {
        alert('Пожалуйста, войдите в систему!');
        window.location.href = '/login';
        return;
    }
    
    const bet = prompt('Введите ставку:', '100');
    
    if (!bet) return;
    
    if (isNaN(bet) || parseInt(bet) <= 0) {
        alert('Ставка должна быть положительным числом!');
        return;
    }
    
    try {
        const response = await fetch(`/api/first_game_slot?bet=${bet}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            if (result.result === 'win') {
                alert(`🎉 ПОБЕДА! +${result.balance_change} монет!`);
            } else if (result.result === 'lose') {
                alert(`😢 ПРОИГРЫШ! -${Math.abs(result.balance_change)} монет!`);
            } else if (result.result === 'draw') {
                alert(`🤝 НИЧЬЯ! Ставка возвращена.`);
            } else if (result.result === 'jackpot') {
                alert(`💎💎💎 ДЖЕКПОТ! +${result.balance_change} монет! 💎💎💎`);
            }
            
            // Обновляем баланс
            if (result.new_balance !== undefined) {
                document.getElementById('balance').textContent = result.new_balance;
            } else {
                await updateBalance();
            }
        } else {
            alert(`Ошибка: ${result.detail || 'Что-то пошло не так!'}`);
            if (response.status === 401) {
                window.location.href = '/login';
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка соединения с сервером!');
    }
}

// Функция обновления баланса
async function updateBalance() {
    const username = getCookie('user');
    
    if (!username) return;
    
    try {
        const response = await fetch(`/api/user/${username}/balance`);
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('balance').textContent = data.balance;
        }
    } catch (error) {
        console.error('Error updating balance:', error);
    }
}

// Загружаем баланс при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    updateBalance();
    
    // Обновляем баланс каждые 5 секунд
    setInterval(updateBalance, 5000);
});


// Регистрация
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, password})
        });
        
        const result = await response.json();
        
        if (response.ok) {
            window.location.href = '/';
        } else {
            alert(result.message || 'Registration failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// Логин
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, password})
        });
        
        const result = await response.json();
        
        if (response.ok) {
            window.location.href = '/';
        } else {
            alert(result.message || 'Login failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
});