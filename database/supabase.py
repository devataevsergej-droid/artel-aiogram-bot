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
    current = await get_user_field(user_id, 'loyalty_score') or 0
    new_score = current + points
    url = f"{config.SUPABASE_URL}/rest/v1/users?user_id=eq.{user_id}"
    async with httpx.AsyncClient() as client:
        await client.patch(url, json={"loyalty_score": new_score}, headers=HEADERS)
