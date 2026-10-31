import asyncio
from datetime import datetime
import aiocoap
import aiocoap.resource as resource

# ==========================================================
# CẤU HÌNH COAP SERVER
# ==========================================================
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5683
RESOURCE_PATH = ("iot", "lab", "message")
URI_PATH_STR = "/" + "/".join(RESOURCE_PATH)

# ==========================================================
# ĐỊNH NGHĨA TÀI NGUYÊN (COAP RESOURCE)
# ==========================================================
class LabMessageResource(resource.Resource):
    """
    Tài nguyên CoAP tại URI: /iot/lab/message
    - GET: Trả về thông điệp chào mừng từ Server (hoặc thông điệp POST gần nhất).
    - POST: Tiếp nhận thông điệp từ Client, hiển thị payload kèm thời gian,
            và phản hồi xác nhận (Code 2.04 Changed).
    """

    def __init__(self, resource_path_str: str = URI_PATH_STR):
        super().__init__()
        self.resource_path_str = resource_path_str
        self.default_greeting = "Xin chao tu CoAP Server"
        self.last_message = None  # Lưu thông điệp POST gần nhất (Gợi ý mở rộng)

    async def render_get(self, request):
        """Xử lý yêu cầu GET từ CoAP Client"""
        print(f"GET request received: {self.resource_path_str}")

        # Trả về thông điệp POST gần nhất nếu có, hoặc thông điệp chào mừng mặc định
        response_payload = self.last_message if self.last_message else self.default_greeting
        return aiocoap.Message(
            code=aiocoap.CONTENT,
            payload=response_payload.encode("utf-8")
        )

    async def render_post(self, request):
        """Xử lý yêu cầu POST từ CoAP Client"""
        now_str = datetime.now().strftime("%H:%M:%S")
        payload_str = request.payload.decode("utf-8", errors="replace")
        self.last_message = payload_str

        print("POST request received:")
        print(f"Payload: {payload_str}")
        print(f"Time: {now_str}")

        # Trả về phản hồi xác nhận thành công (2.04 Changed)
        response_text = "Server da nhan thong diep"
        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload=response_text.encode("utf-8")
        )


# ==========================================================
# HÀM KHỞI CHẠY SERVER
# ==========================================================
async def start_server():
    root = resource.Site()
    # Đăng ký tài nguyên tại cây URI: /iot/lab/message
    root.add_resource(RESOURCE_PATH, LabMessageResource())

    # Khởi tạo Server Context và lắng nghe trên IP & Cổng cấu hình
    server_context = await aiocoap.Context.create_server_context(
        root,
        bind=(SERVER_HOST, SERVER_PORT)
    )

    print("=" * 60)
    print("CoAP Server")
    print(f"CoAP Server started on port {SERVER_PORT}")
    print(f"Listening on: coap://{SERVER_HOST}:{SERVER_PORT}{URI_PATH_STR}")
    print("Nhan Ctrl+C de dung Server.")
    print("=" * 60)

    try:
        # Giữ Server chạy liên tục cho đến khi nhận tín hiệu dừng
        await asyncio.get_running_loop().create_future()
    except asyncio.CancelledError:
        pass
    finally:
        print("\nDang dong CoAP Server...")
        await server_context.shutdown()
        print("Server da dung thanh cong.")


if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\n[INFO] Da ngat chuong trinh Server boi nguoi dung (Ctrl+C).")
