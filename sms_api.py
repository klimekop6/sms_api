import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

from ipaddress import IPv4Address
from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import (
    MessagingService,
    MessageRequestGSMError,
)
import asyncio

from adb_android import AndroidDevice
from config import API_KEY, DEVICE_IP

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )


device = AndroidDevice()

IPV4 = IPv4Address(DEVICE_IP)
session = AirmoreSession(IPV4)
service = MessagingService(session)


class Message(BaseModel):
    number: str = Field(regex="^[1-9][0-9]{8}$")
    text: str


app = FastAPI()


async def api_status():
    if not session.is_server_running:
        device.start_airmore()
        if not session.is_server_running:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    try:
        await asyncio.wait_for(asyncio.to_thread(session.request_authorization), 1)
    except asyncio.TimeoutError:
        device.unlock_screen()
        await asyncio.gather(
            asyncio.to_thread(session.request_authorization),
            asyncio.to_thread(device.authorize_device, 2),
        )
        if not session.request_authorization():
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.head("/status")
async def check_api_status():
    await api_status()


@app.post("/send_sms", dependencies=[Depends(api_key_auth)])
async def send_sms(message: Message):
    await api_status()
    try:
        service.send_message(message.number, message.text)
    except MessageRequestGSMError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
