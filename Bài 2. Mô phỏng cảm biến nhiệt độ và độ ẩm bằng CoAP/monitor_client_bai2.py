import asyncio
import json
from datetime import datetime
import aiocoap

SERVER_URI = "coap://127.0.0.1:5683/iot/lab/sensor01/data"

async def monitor_sensor():
    # Tạo ngữ cảnh CoAP Client
    protocol = await aiocoap.Context.create_client_context()
    print(f"Bat dau giam sat tai nguyen: {SERVER_URI} (Nhan Ctrl+C de dung)...\n")

    while True:
        request = aiocoap.Message(code=aiocoap.GET, uri=SERVER_URI)
        try:
            # Gửi yêu cầu GET và giới hạn thời gian chờ phản hồi (timeout 5 giây)
            response = await asyncio.wait_for(
                protocol.request(request).response,
                timeout=5.0
            )
            
            now = datetime.now().strftime("%H:%M:%S")
            data = json.loads(response.payload.decode('utf-8'))

            device_id = data.get("device_id", "Unknown")
            temperature = data.get("temperature", 0.0)
            humidity = data.get("humidity", 0.0)

            # Hiển thị thông tin theo đúng mẫu đầu ra
            print(f"[{now}] Received sensor data")
            print(f"Device: {device_id}")
            print(f"Temperature: {temperature} C")
            print(f"Humidity: {humidity} %")

            # Kiểm tra điều kiện ngưỡng cảnh báo
            has_warning = False
            if temperature > 35:
                print("CANH BAO: Nhiet do cao")
                has_warning = True
            if humidity < 40:
                print("CANH BAO: Do am thap")
                has_warning = True
            
            if not has_warning:
                print("Trang thai: Binh thuong")

            print("-" * 30)

        except asyncio.TimeoutError:
            print("Loi: Server khong phan hoi (Timeout)!")
            print("-" * 30)
        except json.JSONDecodeError:
            print("Loi: Du lieu nhan duoc khong dung dinh dang JSON!")
            print("-" * 30)
        except Exception as e:
            print(f"Loi ket noi CoAP: {e}")
            print("-" * 30)

        # Chờ 3 giây trước lần truy vấn tiếp theo
        await asyncio.sleep(3)

if __name__ == "__main__":
    try:
        asyncio.run(monitor_sensor())
    except KeyboardInterrupt:
        print("\nDa dung chuong trinh Monitoring CoAP Client.")