import asyncio
import json
import sys
from datetime import datetime
from aiocoap import Context, Message, Code

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

URI = "coap://127.0.0.1:5683/iot/lab/light01/status"

async def main():
    protocol = await Context.create_client_context()

    print("Registering CoAP Observe...")
    # Cấu hình observe=0 để đăng ký theo dõi trạng thái tài nguyên
    request = Message(code=Code.GET, uri=URI, observe=0)
    pr = protocol.request(request)

    # 1. Nhận trạng thái ban đầu của đèn
    initial_response = await pr.response
    print("Observe registration successful")

    now = datetime.now().strftime("%H:%M:%S")
    data = json.loads(initial_response.payload.decode("utf-8"))
    print(f"[{now}] Initial State")
    print(f"Device: {data.get('device_id')}")
    print(f"Status: {data.get('status')}\n")

    # 2. Lắng nghe các thông báo cập nhật tự động (Notify) từ Server
    try:
        async for notification in pr.observation:
            now = datetime.now().strftime("%H:%M:%S")
            data = json.loads(notification.payload.decode("utf-8"))
            print(f"[{now}] State Updated")
            print(f"Device: {data.get('device_id')}")
            print(f"Status: {data.get('status')}\n")
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMonitoring da dung.")