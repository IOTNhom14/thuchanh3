# BÁO CÁO THỰC HÀNH: LẬP TRÌNH PYTHON VỚI GIAO THỨC CoAP

---

## 1. THÔNG TIN SINH VIÊN THỰC HIỆN
- **Lớp / Nhóm:** Nhóm 1 thực hành IoT
- **Hình thức nộp bài:** Qua GitHub Repository

---

## 2. PHIÊN BẢN PYTHON VÀ CÁC THƯ VIỆN SỬ DỤNG
- **Phiên bản Python:** Python 3.10+ (Đã thử nghiệm và hoạt động tối ưu trên Python 3.10 – Python 3.14)
- **Giao thức mạng:** CoAP (Constrained Application Protocol qua tầng truyền vận UDP)
- **Thư viện chính:**
  - `aiocoap` (phiên bản `0.4.17`): Thư viện chuẩn trong hệ sinh thái Python hỗ trợ CoAP bất đồng bộ (`asyncio`), xây dựng Resource Server và Client.
  - `asyncio`: Thư viện xử lý bất đồng bộ tích hợp sẵn trong Python Standard Library.
  - `argparse`: Phân tích tham số dòng lệnh cho Client.

---

## 3. CÁCH CÀI ĐẶT MÔI TRƯỜNG
1. Kiểm tra phiên bản Python:
   ```bash
   python3 --version
   ```
2. Cài đặt thư viện `aiocoap`:
   ```bash
   pip install aiocoap
   ```
   *(Trên macOS nếu sử dụng môi trường ngoài, có thể dùng `pip3 install --user aiocoap`)*

---

## 4. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
thuchanh3/
|-- .gitignore
|-- README.md
|-- "Thực hành buổi 3 python coap.docx"
|
|-- bai1/
|   |-- coap_server_bai1.py      # Chương trình 1: CoAP Server
|   |-- coap_client_bai1.py      # Chương trình 2: CoAP Client
|   |-- test_bai1.py            # Script tự động kiểm thử toàn bộ Bài 1
|
|-- bai2/                       # (Bài 2: Sensor CoAP Server & Monitor Client)
|   |-- sensor_server_bai2.py
|   |-- monitor_client_bai2.py
|
|-- bai3/                       # (Bài 3: Smart Light Server, Controller & Monitor Observe)
    |-- light_server_bai3.py
    |-- light_controller_bai3.py
    |-- light_monitor_bai3.py
```

---

## 5. ĐỊA CHỈ IP, CỔNG VÀ URI CÁC TÀI NGUYÊN CoAP

| Bài | Tên chương trình | Địa chỉ IP / Host | Cổng UDP | URI Tài nguyên | Phương thức hỗ trợ |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **Bài 1** | `coap_server_bai1.py` | `127.0.0.1` | `5683` | `coap://127.0.0.1:5683/iot/lab/message` | **GET**: Lấy thông điệp chào mừng (hoặc thông điệp POST gần nhất)<br>**POST**: Gửi thông tin sinh viên |

---

## 6. CÁCH CHẠY TỪNG CHƯƠNG TRÌNH (BÀI 1)

> **Quy tắc:** Luôn khởi động **CoAP Server** trước để lắng nghe trên cổng UDP 5683, sau đó mở terminal mới để chạy **CoAP Client**.

### Bước 1: Khởi động CoAP Server
Mở Terminal thứ nhất và chạy:
```bash
python3 bai1/coap_server_bai1.py
```

### Bước 2: Chạy CoAP Client
Mở Terminal thứ hai và chạy theo các trường hợp mong muốn:

1. **Chế độ cơ bản theo đúng yêu cầu đề bài (gửi GET và POST):**
   ```bash
   python3 bai1/coap_client_bai1.py
   ```

2. **Gợi ý mở rộng 1 - Client gửi nhiều thông điệp POST liên tiếp:**
   ```bash
   python3 bai1/coap_client_bai1.py --loop
   ```
   *(Mặc định gửi mỗi 3 giây; có thể tùy chỉnh khoảng thời gian, ví dụ `--interval 1.5`, nhấn `Ctrl+C` để dừng)*

3. **Gợi ý mở rộng 2 - Kiểm chứng Server lưu thông điệp POST gần nhất và trả về khi GET tiếp theo:**
   ```bash
   python3 bai1/coap_client_bai1.py --verify-cache
   ```

4. **Gợi ý mở rộng 3 - Thử nghiệm Client truy cập tài nguyên không tồn tại (4.04 Not Found):**
   ```bash
   python3 bai1/coap_client_bai1.py --test-404
   ```

5. **Gợi ý mở rộng 4 - Thử nghiệm khi Server không hoạt động & xử lý timeout:**
   Tắt Server (hoặc mở Client khi chưa bật Server):
   ```bash
   python3 bai1/coap_client_bai1.py
   ```

---

## 7. KẾT QUẢ ĐẠT ĐƯỢC CỦA BÀI 1

1. **Khởi tạo và lắng nghe CoAP Server:**
   - Server khởi tạo thành công trên cổng chuẩn CoAP `5683` qua giao thức UDP.
   - Định nghĩa đúng cây tài nguyên: `/iot/lab/message`.

2. **Xử lý phương thức GET:**
   - Trả về mã phản hồi chuẩn `2.05 Content`.
   - Payload phản hồi ban đầu: `Xin chao tu CoAP Server`.

3. **Xử lý phương thức POST:**
   - Nhận payload gồm thông tin sinh viên: `Xin chao tu CoAP Client - B23DCCN583 - Nguyen Cong Hai Nam`.
   - Hiển thị đầy đủ nội dung thông điệp kèm mốc thời gian nhận (`HH:MM:SS`) trên Server.
   - Trả về mã phản hồi chuẩn `2.04 Changed` với payload xác nhận: `Server da nhan thong diep`.

4. **Các gợi ý mở rộng:**
   - Hỗ trợ gửi POST liên tục theo vòng lặp có đánh số thứ tự (`--loop`).
   - Server lưu cache `last_message` và trả về đúng thông điệp sinh viên ở lần GET tiếp theo (`--verify-cache`).
   - Xử lý mã lỗi `4.04 Not Found` khi truy vấn sai URI (`--test-404`).
   - Xử lý mượt mà ngoại lệ `NetworkError` / `TimeoutError` khi mất kết nối Server, không làm sập ứng dụng.

---

## 8. LOG MINH CHỨNG CHƯƠNG TRÌNH HOẠT ĐỘNG

### 8.1. Log thực tế phía CoAP Client (Luồng chuẩn)
```text
============================================================
CoAP Client
Sinh vien: Nguyen Cong Hai Nam - MSV: B23DCCN583
============================================================
Sending GET request...
URI: coap://127.0.0.1:5683/iot/lab/message
Response:
Code: 2.05 Content
Payload: Xin chao tu CoAP Server

Sending POST request...
Payload: Xin chao tu CoAP Client - B23DCCN583 - Nguyen Cong Hai Nam
Response:
Code: 2.04 Changed
Payload: Server da nhan thong diep
```

### 8.2. Log thực tế phía CoAP Server
```text
============================================================
CoAP Server
CoAP Server started on port 5683
Listening on: coap://127.0.0.1:5683/iot/lab/message
Nhan Ctrl+C de dung Server.
============================================================
GET request received: /iot/lab/message
POST request received:
Payload: Xin chao tu CoAP Client - B23DCCN583 - Nguyen Cong Hai Nam
Time: 10:06:41
```