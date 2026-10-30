import asyncio
import json
import random
from datetime import datetime
import aiocoap
import aiocoap.resource as resource

class SensorResource(resource.Resource):
    def __init__(self):
        super().__init__()
        self.device_id = "sensor01"
        self.temperature = 28.5
        self.humidity = 65.2

    async def update_sensor_data(self):
        """Tự động cập nhật dữ liệu cảm biến ngẫu nhiên mỗi 3 giây"""
        while True:
            # Sinh ngẫu nhiên nhiệt độ (20.0 - 40.0°C) và độ ẩm (30.0 - 80.0%)
            self.temperature = round(random.uniform(20.0, 40.0), 1)
            self.humidity = round(random.uniform(30.0, 80.0), 1)
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] Cap nhat du lieu: Temp = {self.temperature} C, Hum = {self.humidity} %")
            await asyncio.sleep(3)

    async def render_get(self, request):
        """Xử lý yêu cầu GET và trả về giá trị cảm biến mới nhất dạng JSON"""
        now = datetime.now().strftime("%H:%M:%S")
        print(f"[{now}] GET request received: /iot/lab/sensor01/data")

        payload_dict = {
            "device_id": self.device_id,
            "temperature": self.temperature,
            "humidity": self.humidity
        }
        payload_bytes = json.dumps(payload_dict).encode('utf-8')

        # Content-Format 50 tương ứng với application/json trong chuẩn CoAP
        return aiocoap.Message(
            payload=payload_bytes,
            content_format=aiocoap.numbers.media_types_rev['application/json']
        )

async def main():
    # Khởi tạo cây tài nguyên CoAP
    root = resource.Site()
    sensor_resource = SensorResource()

    # Gắn tài nguyên vào đường dẫn /iot/lab/sensor01/data
    root.add_resource(['iot', 'lab', 'sensor01', 'data'], sensor_resource)

    # Khởi tạo CoAP Server trên địa chỉ 127.0.0.1, cổng mặc định 5683
    await aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683))
    print("Sensor CoAP Server started on coap://localhost:5683/iot/lab/sensor01/data")

    # Chạy tác vụ cập nhật dữ liệu cảm biến định kỳ mỗi 3 giây
    asyncio.create_task(sensor_resource.update_sensor_data())

    # Duy trì hoạt động của Server
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDa dung Sensor CoAP Server.")