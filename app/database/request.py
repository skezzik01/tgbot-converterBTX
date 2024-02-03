from app.database.models import User, CounterConvert, WhiteList, Admins, async_session
from sqlalchemy import select, delete, update
from datetime import datetime


async def get_user(user_id) -> User:
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == user_id))
        return result
    
    
async def get_users_ids():
    async with async_session() as session:
        users = await session.scalars(select(User.tg_id))
        return users
    

async def add_user(user_id, firstname, username) -> User:
    try:
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == user_id))
            
            if user is None:
                new_user = User(
                    tg_id=user_id,
                    name=firstname,
                    username=username,
                    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Форматирование даты
                )
                session.add(new_user)
                await session.commit()
                return new_user
            
            return user
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
    
    
async def delete_user(user_id):
    async with async_session() as session:
        await session.execute(delete(User).where(User.tg_id == user_id))
        await session.commit()


async def get_admin(user_id) -> Admins:
    async with async_session() as session:
        result = await session.scalar(select(Admins).where(Admins.user_id == user_id))
        return result
    
async def get_admins() -> Admins:
    async with async_session() as session:
        admins = await session.scalars(select(Admins.user_id))
        return admins
    
    
async def add_user_whitelist(user_id):
    async with async_session() as session:
        session.add(WhiteList(user_id=user_id["userid"], date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        session.add(CounterConvert(user_id=user_id["userid"]))
        await session.commit()
        

async def delete_user_whitelist(user_id):
    async with async_session() as session:
        await session.execute(delete(WhiteList).where(WhiteList.user_id == user_id["userid"]))
        await session.commit()


async def get_whitelist(user_id) -> WhiteList:
    async with async_session() as session:
        result = await session.scalar(select(WhiteList).where(WhiteList.user_id == user_id))
        return result
    

async def get_whitelist_users() -> WhiteList:
    async with async_session() as session:
        users = await session.scalars(select(WhiteList.user_id))
        return users


async def add_counter_convert(user_id, name) -> CounterConvert:
    async with async_session() as session:
        session.add(CounterConvert(user_id=user_id, name=name))
        await session.commit()
    
    
async def get_counter_convert(user_id) -> CounterConvert:
    async with async_session() as session:
        result = await session.scalar(select(CounterConvert).where(CounterConvert.user_id == user_id))
        return result
    

async def update_counters_convert(user_id) -> CounterConvert:
    async with async_session() as session:
        user_count = await session.scalar(select(CounterConvert).where(CounterConvert.user_id == user_id))
        await session.execute(update(CounterConvert).where(CounterConvert.user_id == user_id).values(today = user_count.today + 1, total = user_count.total + 1))
        await session.commit()


async def clear_counters_convert(user_id):    
    async with async_session() as session:
        await session.execute(update(CounterConvert).where(CounterConvert.user_id == user_id).values(today = 0))
        await session.commit()