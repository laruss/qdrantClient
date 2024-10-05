import motor.motor_asyncio

from env import env

client = motor.motor_asyncio.AsyncIOMotorClient(env.MONGODB_URL)
db = client[env.MONGODB_DB_NAME]
