from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
import paho.mqtt.client as mqtt
import asyncio
import json
import uuid
from loguru import logger


class DeviceService:
    def __init__(self):
        self.MQTT_BROKER = "broker.emqx.io"
        self.MQTT_PORT = 1883
        self.MQTT_TOPIC = "project/soil"
        self.MQTT_CLIENT_ID = f"mqtt-client-{uuid.uuid4()}"
        self.MQTT_USERNAME = "admin"
        self.MQTT_PASSWORD = "public"

        self.mqtt_client = mqtt.Client(client_id=self.MQTT_CLIENT_ID)
        self.message_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()  

        self.mqtt_client.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)
        self.mqtt_client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        """Callback function for handling received MQTT messages"""
        try:
            message = msg.payload.decode()
            asyncio.run_coroutine_threadsafe(self.message_queue.put(message), self.loop)
        except Exception as e:
            logger.error(f"Error in on_message: {e}")

    def publish_message(self, topic: str, message: str):
        """Gửi dữ liệu lên MQTT broker."""
        try:
            self.mqtt_client.publish(topic, message)
            logger.info(f"Gửi dữ liệu: {message} tới topic: {topic}")
        except Exception as e:
            logger.error(f"Lỗi khi gửi dữ liệu tới MQTT: {e}")

    def connect_mqtt(self):
        """Connect to the MQTT broker and start the loop"""
        try:
            self.mqtt_client.connect(self.MQTT_BROKER, self.MQTT_PORT, 60)
            self.mqtt_client.loop_start()
            self.mqtt_client.subscribe(self.MQTT_TOPIC)
        except Exception as e:
            logger.error(f"MQTT connection error: {e}")

    async def event_generator(self):
        """Asynchronous generator for sending messages to frontend via SSE"""
        while True:
            try:
                message = await self.message_queue.get()
                logger.info(f"Dữ liệu đã được lấy ra từ queue: {message}")
                payload = {"humidity": message}
                formatted_payload = f"{json.dumps(payload)}\n\n"
                yield formatted_payload
            except Exception as e:
                logger.error(f"Error in event_generator: {e}")

    def setup_routes(self):
        """Set up FastAPI routes for SSE"""
        self.connect_mqtt() 
        return EventSourceResponse(self.event_generator())


