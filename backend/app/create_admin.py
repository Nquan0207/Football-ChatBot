# backend/app/scripts/create_admin.py
import asyncio
from app.db.models.auth_models import UserCreate, Role
from app.services.user_mongo_service import create_user
from app.core.config import settings

async def main():
    user_in = UserCreate(
        username="superadmin",
        email="admin@sportschatbot.com",
        password="Password123!",
        favorite_sports=["football"],
        favorite_team="Manchester United",
        membership=Role.premium,
    )
    admin = await create_user(user_in, roles=[Role.admin])
    print("Created admin:", admin)

if __name__ == "__main__":
    asyncio.run(main())
