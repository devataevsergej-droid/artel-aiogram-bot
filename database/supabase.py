import httpx
from config import config

HEADERS = {
    "apikey": config.SUPABASE_KEY,
    "Authorization": f"Bearer {config.SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

async def get_user_field(user_id: int, field: str):
    url = f"{config.SUPABASE_URL}/rest/v1/users?user_id=eq.{user_id}&select={field}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=HEADERS)
        if r.status_code == 200:
            data = r.json()
            return data[0].get(field) if data else None
    return None

async def upsert_user(user_id: int, username: str, name: str):
    data = {
        "user_id": str(user_id),
        "name": name,
        "username": username or "",
        "ref_count": 0,
        "loyalty_score": 0,
        "loyalty_rank": "Новичок",
        "funnel_stage": "start",
        "created_at": "now()"
    }
    url = f"{config.SUPABASE_URL}/rest/v1/users"
    headers = {**HEADERS, "Prefer": "resolution=merge-duplicates"}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=data, headers=headers)

async def add_loyalty_score_db(user_id: int, points: int):
    """Начислить баллы пользователю"""
    try:
        # Получаем текущие баллы
        url_get = f"{config.SUPABASE_URL}/rest/v1/users?user_id=eq.{user_id}&select=loyalty_score"
        async with httpx.AsyncClient() as client:
            r = await client.get(url_get, headers=HEADERS)
            if r.status_code == 200 and r.json():
                current_score = r.json()[0].get("loyalty_score", 0)
            else:
                current_score = 0
        
        new_score = current_score + points
        
        # Обновляем баллы
        url_patch = f"{config.SUPABASE_URL}/rest/v1/users?user_id=eq.{user_id}"
        async with httpx.AsyncClient() as client:
            await client.patch(url_patch, json={"loyalty_score": new_score}, headers=HEADERS)
        
        print(f"✅ Начислено {points} баллов пользователю {user_id}. Теперь: {new_score}")
        return new_score
    except Exception as e:
        print(f"❌ Ошибка начисления баллов: {e}")
        return None

async def log_action(user_id: int, action: str):
    """Записывает действие пользователя в таблицу logs"""
    url = f"{config.SUPABASE_URL}/rest/v1/logs"
    headers = {
        "apikey": config.SUPABASE_KEY,
        "Authorization": f"Bearer {config.SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    data = {
        "user_id": str(user_id),
        "action": action
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=data, headers=headers)

async def get_user_rank(user_id: int):
    """Получает ранг и баллы пользователя"""
    url = f"{config.SUPABASE_URL}/rest/v1/users?user_id=eq.{user_id}&select=loyalty_rank,loyalty_score"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=HEADERS)
        if r.status_code == 200 and r.json():
            return r.json()[0]
    return {"loyalty_rank": "Новичок", "loyalty_score": 0}
