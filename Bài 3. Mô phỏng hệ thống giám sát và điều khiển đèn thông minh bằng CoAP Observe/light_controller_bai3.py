import asyncio
import json
import sys
from aiocoap import Context, Message, Code

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

URI = "coap://127.0.0.1:5683/iot/lab/light01/status"

async def main():
    protocol = await Context.create_client_context()

    while True:
        cmd = await asyncio.to_thread(input, "Nhap lenh (ON/OFF/STATUS/EXIT): ")
        cmd = cmd.strip().upper()

        if cmd == "EXIT":
            print("Ket thuc chuong trinh dieu khien.")
            break

        elif cmd in ["ON", "OFF"]:
            payload = json.dumps({"device_id": "light01", "command": cmd}).encode("utf-8")
            request = Message(code=Code.PUT, uri=URI, payload=payload, content_format=50)
            print("Sending PUT request...")
            try:
                response = await protocol.request(request).response
                print(f"Response Code: {response.code}")
                if response.code == Code.CHANGED:
                    print(f"Da {'bat' if cmd == 'ON' else 'tat'} den light01\n")
                else:
                    print(f"Phan hoi: {response.payload.decode('utf-8')}\n")
            except Exception as e:
                print(f"Loi ket noi: {e}\n")

        elif cmd == "STATUS":
            request = Message(code=Code.GET, uri=URI)
            print("Sending GET request...")
            try:
                response = await protocol.request(request).response
                print(f"Response Code: {response.code}")
                print(f"Response:\n{response.payload.decode('utf-8')}\n")
            except Exception as e:
                print(f"Loi ket noi: {e}\n")

        else:
            print("Lenh khong hop le. Vui long chon ON, OFF, STATUS hoac EXIT.\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nController da dong.")