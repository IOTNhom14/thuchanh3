# BÁO CÁO THỰC HÀNH: LẬP TRÌNH PYTHON VỚI GIAO THỨC CoAP

---

## 1. THÔNG TIN SINH VIÊN THỰC HIỆN

- **Lớp / Nhóm:** Nhóm 4 thực hành IoT
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
|-- "Bài 2. Mô phỏng cảm biến nhiệt độ và độ ẩm bằng CoAP"/
|   |-- sensor_server_bai2.py   # CoAP Sensor Server phát sinh ngẫu nhiên nhiệt độ, độ ẩm
|   |-- monitor_client_bai2.py  # CoAP Monitor Client định kỳ gửi GET thăm dò
|
|-- "Bài 3. Mô phỏng hệ thống giám sát và điều khiển đèn thông minh bằng CoAP Observe"/
    |-- light_server_bai3.py     # CoAP Smart Light Server (ObservableResource)
    |-- light_controller_bai3.py # Client điều khiển đèn (PUT lệnh ON/OFF, GET trạng thái)
    |-- light_monitor_bai3.py    # Client giám sát đèn theo thời gian thực (CoAP Observe)
```

---

## 5. ĐỊA CHỈ IP, CỔNG VÀ URI CÁC TÀI NGUYÊN CoAP

|       Bài       | Tên chương trình    | Địa chỉ IP / Host | Cổng UDP | URI Tài nguyên                          | Phương thức hỗ trợ                                                                                                       |
| :--------------: | :---------------------- | :------------------: | :-------: | :---------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **Bài 1** | `coap_server_bai1.py` |    `127.0.0.1`    | `5683` | `coap://127.0.0.1:5683/iot/lab/message` | **GET**: Lấy thông điệp chào mừng (hoặc thông điệp POST gần nhất)<br>**POST**: Gửi thông tin sinh viên |
| **Bài 2** | `sensor_server_bai2.py` |    `127.0.0.1`    | `5683` | `coap://127.0.0.1:5683/iot/lab/sensor01/data` | **GET**: Lấy dữ liệu cảm biến (nhiệt độ, độ ẩm) mới nhất dạng JSON |
| **Bài 3** | `light_server_bai3.py` |    `127.0.0.1`    | `5683` | `coap://127.0.0.1:5683/iot/lab/light01/status` | **GET**: Đọc trạng thái đèn & Đăng ký quan sát Observe (`observe=0`)<br>**PUT**: Điều khiển bật/tắt đèn (`ON` / `OFF`) |

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

## 8. LOG MINH CHỨNG CHƯƠNG TRÌNH HOẠT ĐỘNG (BÀI 1)

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

---

## 9. CÁCH CHẠY TỪNG CHƯƠNG TRÌNH (BÀI 2 - CẢM BIẾN NHIỆT ĐỘ & ĐỘ ẨM)

Hệ thống mô phỏng cảm biến nhiệt độ và độ ẩm sử dụng CoAP gồm 2 chương trình:
- **`sensor_server_bai2.py` (CoAP Sensor Server):** Khởi chạy Server lắng nghe trên cổng UDP `5683`, tự động cập nhật ngẫu nhiên thông số nhiệt độ (20.0 – 40.0°C) và độ ẩm (30.0 – 80.0%) sau mỗi 3 giây và phục vụ tại URI `coap://127.0.0.1:5683/iot/lab/sensor01/data`.
- **`monitor_client_bai2.py` (CoAP Monitor Client):** Thiết lập cơ chế định kỳ gửi yêu cầu GET (mỗi 3 giây) đến Server để thu thập thông số môi trường, giải mã dữ liệu JSON và phân tích đánh giá các ngưỡng cảnh báo an toàn.

> **Quy tắc:** Khởi động **Sensor Server** trước, sau đó mở terminal mới để chạy **Monitor Client**.

### Bước 1: Khởi động CoAP Sensor Server

Mở Terminal thứ nhất và chạy:

```bash
cd "Bài 2. Mô phỏng cảm biến nhiệt độ và độ ẩm bằng CoAP"
python sensor_server_bai2.py
```

### Bước 2: Khởi động CoAP Monitor Client

Mở Terminal thứ hai và chạy:

```bash
cd "Bài 2. Mô phỏng cảm biến nhiệt độ và độ ẩm bằng CoAP"
python monitor_client_bai2.py
```

Chương trình sẽ tự động truy vấn định kỳ mỗi 3 giây, hiển thị dữ liệu nhận được và đưa ra cảnh báo tức thời nếu phát hiện nhiệt độ cao (> 35°C) hoặc độ ẩm thấp (< 40%). Nhấn `Ctrl+C` để dừng chương trình.

---

## 10. KẾT QUẢ ĐẠT ĐƯỢC CỦA BÀI 2

1. **Mô phỏng nguồn dữ liệu IoT động (Dynamic IoT Telemetry):**
   - Server triển khai tác vụ nền bất đồng bộ `asyncio.create_task(sensor_resource.update_sensor_data())` liên tục sinh ngẫu nhiên các giá trị đo đạc: nhiệt độ từ `20.0` đến `40.0°C` và độ ẩm từ `30.0` đến `80.0%` theo chu kỳ 3 giây.
   - Luồng cập nhật dữ liệu chạy ngầm không gây block hay trễ quá trình tiếp nhận và phản hồi các gói tin CoAP trên cổng UDP 5683.

2. **Chuẩn hóa trao đổi dữ liệu RESTful qua JSON:**
   - Khi Client gửi yêu cầu GET, Server trích xuất giá trị đo hiện tại và đóng gói thành chuỗi JSON:
     ```json
     {
       "device_id": "sensor01",
       "temperature": 28.5,
       "humidity": 65.2
     }
     ```
   - Thiết lập header `Content-Format` mang giá trị `50` (`application/json`) theo đúng đặc tả IANA CoAP Content-Formats.

3. **Cơ chế thu thập dữ liệu định kỳ (Polling Pattern):**
   - Client thiết lập vòng lặp bất đồng bộ gửi GET request đều đặn mỗi 3 giây tới URI `coap://127.0.0.1:5683/iot/lab/sensor01/data`.
   - Sử dụng `asyncio.wait_for(..., timeout=5.0)` thiết lập timeout 5 giây cho mỗi yêu cầu, đảm bảo Client không bị treo vô hạn nếu mạng gặp sự cố.

4. **Tự động phân tích và cảnh báo ngưỡng (Threshold Evaluation):**
   - Phân tích cú pháp JSON và so khớp với các quy tắc cảnh báo:
     - Khi `temperature > 35`: Kích hoạt cảnh báo `CANH BAO: Nhiet do cao`.
     - Khi `humidity < 40`: Kích hoạt cảnh báo `CANH BAO: Do am thap`.
     - Khi các thông số đều nằm trong dải cho phép: Xác nhận `Trang thai: Binh thuong`.

5. **Xử lý ngoại lệ và đảm bảo độ bền vững (Resilience):**
   - Client bắt các ngoại lệ `asyncio.TimeoutError` (Server phản hồi chậm hoặc không phản hồi), `json.JSONDecodeError` (lỗi định dạng dữ liệu), và ngoại lệ mạng tổng quát để ứng dụng tiếp tục hoạt động ổn định ở các chu kỳ sau mà không bị ngắt quãng.

---

## 11. LOG MINH CHỨNG CHƯƠNG TRÌNH HOẠT ĐỘNG (BÀI 2)

### 11.1. Log thực tế phía CoAP Sensor Server (`sensor_server_bai2.py`)

```text
Sensor CoAP Server started on coap://localhost:5683/iot/lab/sensor01/data
[10:15:02] Cap nhat du lieu: Temp = 27.4 C, Hum = 62.8 %
[10:15:05] Cap nhat du lieu: Temp = 36.2 C, Hum = 58.1 %
[10:15:06] GET request received: /iot/lab/sensor01/data
[10:15:08] Cap nhat du lieu: Temp = 31.5 C, Hum = 35.4 %
[10:15:09] GET request received: /iot/lab/sensor01/data
[10:15:11] Cap nhat du lieu: Temp = 29.0 C, Hum = 68.3 %
[10:15:12] GET request received: /iot/lab/sensor01/data
```

### 11.2. Log thực tế phía CoAP Monitor Client (`monitor_client_bai2.py`)

```text
Bat dau giam sat tai nguyen: coap://127.0.0.1:5683/iot/lab/sensor01/data (Nhan Ctrl+C de dung)...

[10:15:06] Received sensor data
Device: sensor01
Temperature: 36.2 C
Humidity: 58.1 %
CANH BAO: Nhiet do cao
------------------------------
[10:15:09] Received sensor data
Device: sensor01
Temperature: 31.5 C
Humidity: 35.4 %
CANH BAO: Do am thap
------------------------------
[10:15:12] Received sensor data
Device: sensor01
Temperature: 29.0 C
Humidity: 68.3 %
Trang thai: Binh thuong
------------------------------
```

---

## 12. CÁCH CHẠY TỪNG CHƯƠNG TRÌNH (BÀI 3 - CoAP OBSERVE)

Hệ thống mô phỏng giám sát và điều khiển đèn thông minh qua CoAP Observe gồm 3 thành phần:
- **CoAP Server:** Quản lý tài nguyên trạng thái đèn thông minh và phân phối thông báo quan sát (`light_server_bai3.py`).
- **Monitor Client:** Đăng ký quan sát (Observe) trạng thái đèn và tự động nhận thông báo khi có thay đổi (`light_monitor_bai3.py`).
- **Controller Client:** Gửi lệnh điều khiển bật/tắt (PUT) hoặc kiểm tra trạng thái tức thời (GET) (`light_controller_bai3.py`).

> **Quy tắc:** Khởi động **Server** trước, sau đó mở Terminal thứ hai chạy **Monitor Client**, cuối cùng mở Terminal thứ ba chạy **Controller Client**.

### Bước 1: Khởi động CoAP Smart Light Server

Mở Terminal thứ nhất và chạy:

```bash
cd "Bài 3. Mô phỏng hệ thống giám sát và điều khiển đèn thông minh bằng CoAP Observe"
python light_server_bai3.py
```

### Bước 2: Khởi động Client Giám sát trạng thái đèn (CoAP Observe)

Mở Terminal thứ hai và chạy:

```bash
cd "Bài 3. Mô phỏng hệ thống giám sát và điều khiển đèn thông minh bằng CoAP Observe"
python light_monitor_bai3.py
```

Client sẽ gửi yêu cầu GET kèm option `observe=0` để đăng ký theo dõi tài nguyên `/iot/lab/light01/status`, hiển thị trạng thái ban đầu (`OFF`) và duy trì lắng nghe các thông báo (Notify) từ Server.

### Bước 3: Khởi động Client Điều khiển đèn

Mở Terminal thứ ba và chạy:

```bash
cd "Bài 3. Mô phỏng hệ thống giám sát và điều khiển đèn thông minh bằng CoAP Observe"
python light_controller_bai3.py
```

Nhập các lệnh điều khiển tương tác qua bàn phím:
- `ON`: Gửi yêu cầu PUT để bật đèn (`"command": "ON"`).
- `OFF`: Gửi yêu cầu PUT để tắt đèn (`"command": "OFF"`).
- `STATUS`: Gửi yêu cầu GET để tra cứu trạng thái đèn hiện tại.
- `EXIT`: Thoát chương trình điều khiển.

---

## 13. KẾT QUẢ ĐẠT ĐƯỢC CỦA BÀI 3

1. **Ứng dụng cơ chế CoAP Observe (RFC 7641):**
   - Kế thừa lớp `ObservableResource` từ `aiocoap.resource` để biến tài nguyên đèn (`SmartLightResource`) thành tài nguyên có khả năng quan sát.
   - Monitor Client đăng ký lắng nghe trạng thái bằng `Message(code=Code.GET, uri=URI, observe=0)`.
   - Server tự động quản lý danh sách các Observers đã đăng ký.

2. **Cơ chế cập nhật tự động (Server-Push / Asynchronous Notification):**
   - Khi có sự thay đổi trạng thái từ `OFF -> ON` hoặc `ON -> OFF` thông qua lệnh điều khiển PUT, Server gọi `self.updated_state()`.
   - Hệ thống tự động đẩy gói tin cập nhật (Notify) đến tất cả các Monitor Client đang đăng ký mà không cần Client phải gửi yêu cầu thăm dò liên tục (polling), giúp tối ưu hóa băng thông mạng và tiết kiệm năng lượng cho các thiết bị IoT constrained.

3. **Giao thức điều khiển và định dạng dữ liệu chuẩn RESTful IoT:**
   - Sử dụng định dạng `application/json` (CoAP Content-Format `50`) để trao đổi dữ liệu:
     - Dữ liệu trạng thái phản hồi: `{"device_id": "light01", "status": "ON"|"OFF"}`.
     - Dữ liệu lệnh điều khiển: `{"device_id": "light01", "command": "ON"|"OFF"}`.
   - Áp dụng chuẩn các mã phản hồi CoAP:
     - `2.05 Content`: Trả về trạng thái hiện tại kèm payload JSON.
     - `2.04 Changed`: Thông báo trạng thái đã được cập nhật thành công sau lệnh PUT.
     - `4.00 Bad Request`: Báo lỗi khi lệnh nhận được không hợp lệ (không phải `ON` hoặc `OFF`).

4. **Tối ưu hóa và xử lý tương thích hệ điều hành Windows:**
   - Cấu hình `asyncio.WindowsSelectorEventLoopPolicy` để khắc phục hạn chế xử lý socket UDP bất đồng bộ trên Windows.
   - Sử dụng địa chỉ IPv4 tường minh `127.0.0.1` thay cho `localhost` để tránh xung đột phân giải IPv6 (`::1`) dẫn đến lỗi Winsock `WinError 10054 (WSAECONNRESET)`.

---

## 14. LOG MINH CHỨNG CHƯƠNG TRÌNH HOẠT ĐỘNG (BÀI 3)

### 14.1. Log thực tế phía CoAP Server (`light_server_bai3.py`)

```text
CoAP Smart Light Server started...
Resource: /iot/lab/light01/status

PUT request received:
Device: light01
Command: ON
Light state changed: OFF -> ON
Notify observers: ON

PUT request received:
Device: light01
Command: OFF
Light state changed: ON -> OFF
Notify observers: OFF
```

### 14.2. Log thực tế phía Monitor Client (`light_monitor_bai3.py` - CoAP Observe)

```text
Registering CoAP Observe...
Observe registration successful
[03:47:28] Initial State
Device: light01
Status: OFF

[03:50:04] State Updated
Device: light01
Status: ON

[03:50:45] State Updated
Device: light01
Status: OFF
```

### 14.3. Log thực tế phía Controller Client (`light_controller_bai3.py`)

```text
Nhap lenh (ON/OFF/STATUS/EXIT): ON
Sending PUT request...
Response Code: 2.04 Changed
Da bat den light01

Nhap lenh (ON/OFF/STATUS/EXIT): STATUS
Sending GET request...
Response Code: 2.05 Content
Response:
{"device_id": "light01", "status": "ON"}

Nhap lenh (ON/OFF/STATUS/EXIT): OFF
Sending PUT request...
Response Code: 2.04 Changed
Da tat den light01

Nhap lenh (ON/OFF/STATUS/EXIT): STATUS
Sending GET request...
Response Code: 2.05 Content
Response:
{"device_id": "light01", "status": "OFF"}

Nhap lenh (ON/OFF/STATUS/EXIT): EXIT
Ket thuc chuong trinh dieu khien.
```

