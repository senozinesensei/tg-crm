"""Seed script to create default admin user."""
import asyncio
from sqlalchemy import select
from app.database import async_session
from app.models.user import User
from app.models.settings import Settings
from app.services.auth_service import hash_password


async def seed():
    async with async_session() as db:
        # Create default admin user
        result = await db.execute(select(User).where(User.email == "admin@admin.com"))
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email="admin@admin.com",
                hashed_password=hash_password("admin123"),
                full_name="Admin",
                is_active=True,
            )
            db.add(user)
            print("Created default admin user: admin@admin.com / admin123")

        # Create default settings row
        result = await db.execute(select(Settings).where(Settings.id == 1))
        settings = result.scalar_one_or_none()
        if not settings:
            settings = Settings(id=1)
            db.add(settings)
            print("Created default settings row")

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
