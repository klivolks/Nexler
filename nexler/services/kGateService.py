from threading import Thread
import asyncio
import json
import signal
import requests
import websockets

from app.kGateActions import despatch

from nexler.utils.config_util import Config


is_running = False
kgate_thread = None


class KGateService:

    def __init__(self):
        ws_service = Config().get("KGATE_WS_URL").rstrip("/")
        http_service = Config().get("KGATE_HTTP_URL").rstrip("/")
        self.client_id = Config().get("KGATE_CLIENT_ID")
        self.origin = Config().get("SERVICE_NAME")

        self.ws_url = ws_service + "/messenger/ws"
        self.publish_url = http_service + "/messenger/publish"

    async def subscribe(self, channel):

        headers = {
            "X-Client-Id": self.client_id,
            "Origin": self.origin
        }

        async with websockets.connect(
            self.ws_url,
            additional_headers=headers
        ) as ws:

            print(f"kGate connected: {channel}")

            await ws.send(json.dumps({
                "type": "subscribe",
                "channel": channel
            }))

            async for raw in ws:

                if not is_running:
                    break

                frame = json.loads(raw)

                if frame.get("type") == "event":

                    despatch(frame["channel"], frame.get("payload"))

                    await ws.send(json.dumps({
                        "type": "ack",
                        "channel": frame["channel"],
                        "message_id": frame["message_id"]
                    }))


    def publish(self, channel, payload):

        return requests.post(
            self.publish_url,
            headers={
                "X-Client-Id": self.client_id,
                "Origin": self.origin,
                "Content-Type": "application/json"
            },
            json={
                "channel": channel,
                "payload": payload
            }
        )


def consume_kgate_events():

    global is_running

    kgate = KGateService()

    channels = Config("app/config/kGateChannels.json").get("channels")

    async def runner():

        tasks = []

        for channel in channels:
            tasks.append(
                kgate.subscribe(channel)
            )

        await asyncio.gather(*tasks)


    asyncio.run(runner())


def start_kgate_thread():

    global is_running, kgate_thread

    is_running = True

    kgate_thread = Thread(
        target=consume_kgate_events,
        daemon=True
    )

    kgate_thread.start()

    print("kGate subscriber thread started.")



def stop_kgate_thread():

    global is_running, kgate_thread

    is_running = False

    if kgate_thread and kgate_thread.is_alive():
        kgate_thread.join()

    print("kGate subscriber stopped.")



def setup_kgate(app):

    start_kgate_thread()

    def handle_shutdown_signal(signum, frame):

        print(f"Received signal {signum}, shutting down...")

        stop_kgate_thread()


    signal.signal(signal.SIGTERM, handle_shutdown_signal)
    signal.signal(signal.SIGINT, handle_shutdown_signal)