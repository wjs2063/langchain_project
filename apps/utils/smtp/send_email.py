import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from typing import List
import asyncio

load_dotenv()

naver_id, naver_password = os.getenv("NAVER_ID"), os.getenv("NAVER_PASSWORD")
conf = ConnectionConfig(
    MAIL_USERNAME=naver_id,
    MAIL_PASSWORD=naver_password,
    MAIL_SERVER="smtp.naver.com",
    MAIL_STARTTLS=True,
    MAIL_PORT=587,
    MAIL_FROM_NAME="jaehyeon",
    MAIL_FROM="jahy5352@naver.com",
    MAIL_SSL_TLS=False,
)


# or background or celery task
async def send_email(to_email: List[str], subject: str, body: str):
    fm = FastMail(conf)
    message = MessageSchema(
        subject=subject,
        recipients=to_email,
        body=body,
        subtype=MessageType.html,
    )
    await fm.send_message(message)
    return {"status": "ok", "msg": "mail sent"}


asyncio.run(send_email())
