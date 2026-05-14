from supabase import create_client
from config import config

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def get_user_field(user_id: int, field: str):
    try:
        result = supabase.table("users").select(field).eq("user_id", str(user_id)).execute()
        if result.data:
            return result.data[0].get(field)
    except:
        pass
    return None

def update_user_field(user_id: int, field: str, value):
    try:
        supabase.table("users").update({field: value}).eq("user_id", str(user_id)).execute()
    except:
        pass

def add_loyalty_score(user_id: int, points: int):
    current = get_user_field(user_id, "loyalty_score") or 0
    new_score = current + points
    update_user_field(user_id, "loyalty_score", new_score)
    
    for rank in config.RANKS:
        if new_score >= rank["min_score"]:
            new_rank = rank["name"]
    
    old_rank = get_user_field(user_id, "loyalty_rank") or "Новичок"
    if new_rank != old_rank:
        update_user_field(user_id, "loyalty_rank", new_rank)
        return new_rank
    return None

def upsert_user(user_id: int, username: str, name: str):
    """Создаёт или обновляет пользователя"""
    try:
        # Проверяем, есть ли уже
        existing = supabase.table("users").select("user_id").eq("user_id", str(user_id)).execute()
        
        if existing.data:
            # Обновляем имя
            supabase.table("users").update({"name": name}).eq("user_id", str(user_id)).execute()
        else:
            # Создаём нового
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
            supabase.table("users").insert(data).execute()
    except Exception as e:
        print(f"Ошибка upsert_user: {e}")
