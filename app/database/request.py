from app.database.models import User, Application, async_session
from sqlalchemy import select


async def get_applications():
    async with async_session() as session:
        result = await session.scalars(select(Application))
        return result
    
async def get_application(application_id) -> Application:
    async with async_session() as session:
        result = await session.scalar(select(Application).where(Application.id == application_id))
        return result