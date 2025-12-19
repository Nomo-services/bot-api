import asyncio

from passlib.context import CryptContext
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def encrypt_password(password: str):
    return pwd_context.hash(password)


async def verify_password(password: str, encrypted_password: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        pwd_context.verify,
        password,
        encrypted_password
    )
