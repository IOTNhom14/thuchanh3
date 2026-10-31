import asyncio
import json
import sys
import aiocoap
import aiocoap.resource as resource
from aiocoap.numbers.codes import Code

# Khắc phục giới hạn asyncio UDP trên hệ điều hành Windows
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class SmartLightResource(resource.ObservableResource):
    def __init__(self):
        super().__init__()
        self.device_id = "light01"
        self.status = "OFF"  # Trạng thái mặc định ban đầu là OFF

    async def render_get(self, request):
        """Xử lý yêu cầu GET từ Client và trả về trạng thái hiện tại."""
        payload_data = {
            "device_id": self.device_id,
            "status": self.status
        }
        payload_bytes = json.dumps(payload_data).encode("utf-8")
        # Content-Format 50 tương ứng với application/json
        return aiocoap.Message(payload=payload_bytes, code=Code.CONTENT, content_format=50)

    async def render_put(self, request):
        """Xử lý lệnh điều khiển PUT để bật/tắt đèn."""
        try:
            req_data = json.loads(request.payload.decode("utf-8"))
            command = req_data.get("command", "").upper()
            dev_id = req_data.get("device_id", self.device_id)

            print("\nPUT request received:")
            print(f"Device: {dev_id}")
            print(f"Command: {command}")

            if command in ["ON", "OFF"]:
                state_changed = (self.status != command)
                old_status = self.status
                self.status = command

                # Nếu trạng thái thay đổi thực sự, gửi thông báo tới các observer
                if state_changed:
                    print(f"Light state changed: {old_status} -> {self.status}")
                    print(f"Notify observers: {self.status}")
                    self.updated_state()

                return aiocoap.Message(code=Code.CHANGED, payload=b"Status updated")
            else:
                return aiocoap.Message(code=Code.BAD_REQUEST, payload=b"Invalid command. Use ON or OFF")
        except Exception as err:
            return aiocoap.Message(code=Code.BAD_REQUEST, payload=str(err).encode("utf-8"))

async def main():
    root = resource.Site()
    # Cung cấp tài nguyên tại URI /iot/lab/light01/status
    root.add_resource(['iot', 'lab', 'light01', 'status'], SmartLightResource())

    await aiocoap.Context.create_server_context(root, bind=('127.0.0.1', 5683))
    print("CoAP Smart Light Server started...")
    print("Resource: /iot/lab/light01/status")

    # Giữ server tiếp tục lắng nghe yêu cầu
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCoAP Server da dung.")