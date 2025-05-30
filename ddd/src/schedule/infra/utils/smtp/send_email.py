import asyncio
import os
from typing import List

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

load_dotenv()

naver_id, naver_password = os.getenv("NAVER_ID"), os.getenv("NAVER_PASSWORD")
conf = ConnectionConfig(
    MAIL_USERNAME=naver_id,
    MAIL_PASSWORD=naver_password,
    MAIL_SERVER=os.getenv("SMTP_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_PORT=587,
    MAIL_FROM_NAME="test_user",
    MAIL_FROM=os.getenv("SMTP_MAIL_FROM"),
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


asyncio.run(send_email(to_email=["test_user_email"], subject="test", body="test"))
