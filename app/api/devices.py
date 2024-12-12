from email import message
from fastapi import APIRouter, Depends, HTTPException, Request
from app.services.device_service import DeviceService
from loguru import logger

router = APIRouter()
device_service = DeviceService()

@router.get("/events")
async def get_events():
    """Route để gửi dữ liệu SSE"""
    return device_service.setup_routes()

@router.post("/send-mqtt/")
async def send_to_mqtt(request: Request):
    try:
        data = await request.json()
        if data['message'] == True:
            message = 'on'
        else: 
            message = 'off'
        topic = 'project/control'
        device_service.publish_message(topic, message)
        return {"status": "success", "message": "Dữ liệu đã được gửi tới MQTT"}
    except Exception as e:
        logger.error(f"Lỗi khi xử lý yêu cầu: {e}")
        return {"status": "error", "message": str(e)}

@router.post("/send-status/")
async def send_to_mqtt(request: Request):
    try:
        data = await request.json()
        
        if data['message'] == True:
            message = 'Thủ công'
        else: 
            message = 'Tự động'
        logger.warning(f'{message}')
        topic = 'project/control'
        device_service.publish_message(topic, message)
        return {"status": "success", "message": "Dữ liệu đã được gửi tới MQTT"}
    except Exception as e:
        logger.error(f"Lỗi khi xử lý yêu cầu: {e}")
        return {"status": "error", "message": str(e)}
    
@router.post("/create-humidity/")
async def send_to_mqtt(request: Request):
    try:
        data = await request.json()
        message = data['message']
        topic = 'project/control'
        logger.warning(f'{message}')
        device_service.publish_message(topic, message)
        return {"status": "success", "message": "Dữ liệu đã được gửi tới MQTT"}
    except Exception as e:
        logger.error(f"Lỗi khi xử lý yêu cầu: {e}")
        return {"status": "error", "message": str(e)}