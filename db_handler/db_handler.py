from create_bot import pg_manager
import asyncio
from sqlalchemy import BigInteger, String, Date

async def create_table_users(table_name="users"):
    async with pg_manager:
        await  pg_manager.create_table(table_name=table_name, columns=[
            {"name": "user_id", "type": BigInteger, "options": {"primary_key": True, "autoincrement": False}},
            {"name": "sign", "type": String}])

async def get_user_data(user_id: int, table_name="users"):
    async with pg_manager:
        user_info = await pg_manager.select_data(table_name=table_name, where_dict={'user_id':user_id}, one_dict=True)
        if user_info:
            return user_info
        else:
            return None

async def insert_user (user_data: dict, table_name="users"):
    async with pg_manager:
        await pg_manager.insert_data_with_update(table_name=table_name, records_data=user_data, conflict_column="user_id")



async def create_table_messages(table_name="messages"):
    async with pg_manager:
        await pg_manager.create_table(table_name=table_name, columns=[
            {"name": "message_id", "type": BigInteger, "options": {"primary_key": True, "autoincrement": False}},
            {"name": "chat_id", "type": BigInteger, "options": {"primary_key": True, "autoincrement": False}},
            {"name": "date", "type": Date}
        ])


