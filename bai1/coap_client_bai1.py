import argparse
import asyncio
import sys
import aiocoap

# ==========================================================
# THÔNG TIN SINH VIÊN & CẤU HÌNH COAP CLIENT
# ==========================================================
STUDENT_NAME = "Nguyen Cong Hai Nam"
STUDENT_ID = "B23DCCN583"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5683
RESOURCE_PATH = "/iot/lab/message"

# ==========================================================
# CÁC HÀM GỬI YÊU CẦU COAP
# ==========================================================
async def send_get_request(client_context: aiocoap.Context, uri: str):
    """
    Thực hiện gửi yêu cầu GET tới CoAP Server
    """
    print("Sending GET request...")
    print(f"URI: {uri}")
    try:
        request = aiocoap.Message(code=aiocoap.GET, uri=uri)
        # Thiết lập timeout tối đa 5 giây khi chờ phản hồi
        response = await asyncio.wait_for(client_context.request(request).response, timeout=5.0)

        print("Response:")
        print(f"Code: {response.code}")
        payload_text = response.payload.decode("utf-8", errors="replace")
        print(f"Payload: {payload_text}")
        return response
    except (aiocoap.error.NetworkError, TimeoutError, asyncio.TimeoutError):
        print("[LOI] Khong the ket noi toi CoAP Server hoac timeout! Vui long kiem tra Server da duoc khoi dong chua.")
        return None
    except Exception as e:
        print(f"[LOI] Loi khong xac dinh khi gui GET: {e}")
        return None


async def send_post_request(client_context: aiocoap.Context, uri: str, payload_str: str):
    """
    Thực hiện gửi yêu cầu POST tới CoAP Server
    """
    print("Sending POST request...")
    print(f"Payload: {payload_str}")
    try:
        request = aiocoap.Message(
            code=aiocoap.POST,
            uri=uri,
            payload=payload_str.encode("utf-8")
        )
        # Thiết lập timeout tối đa 5 giây khi chờ phản hồi
        response = await asyncio.wait_for(client_context.request(request).response, timeout=5.0)

        print("Response:")
        print(f"Code: {response.code}")
        payload_text = response.payload.decode("utf-8", errors="replace")
        print(f"Payload: {payload_text}")
        return response
    except (aiocoap.error.NetworkError, TimeoutError, asyncio.TimeoutError):
        print("[LOI] Khong the ket noi toi CoAP Server hoac timeout! Vui long kiem tra Server da duoc khoi dong chua.")
        return None
    except Exception as e:
        print(f"[LOI] Loi khong xac dinh khi gui POST: {e}")
        return None


# ==========================================================
# HÀM CHÍNH
# ==========================================================
async def main():
    parser = argparse.ArgumentParser(description="CoAP Client - Bai 1: Gui va nhan thong diep CoAP")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Dia chi IP hoac Hostname cua CoAP Server (mac dinh: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Cong CoAP Server (mac dinh: 5683)")
    parser.add_argument("--loop", "-l", action="store_true", help="Goi y mo rong 1: Gui nhieu thong diep POST lien tiep")
    parser.add_argument("--interval", type=float, default=3.0, help="Khoang thoi gian (giay) giua cac lan gui trong che do loop (mac dinh: 3.0s)")
    parser.add_argument("--verify-cache", action="store_true", help="Goi y mo rong 2: Gui GET lai sau POST de kiem tra Server tra ve message vua gui")
    parser.add_argument("--test-404", action="store_true", help="Goi y mo rong 3: Thu nghiem truy cap tai nguyen khong ton tai (kiem tra 4.04 Not Found)")
    args = parser.parse_args()

    target_uri = f"coap://{args.host}:{args.port}{RESOURCE_PATH}"
    client_context = await aiocoap.Context.create_client_context()

    print("=" * 60)
    print("CoAP Client")
    print(f"Sinh vien: {STUDENT_NAME} - MSV: {STUDENT_ID}")
    print("=" * 60)

    try:
        # Gợi ý mở rộng 3: Thử nghiệm truy cập URI không tồn tại
        if args.test_404:
            invalid_uri = f"coap://{args.host}:{args.port}/iot/lab/invalid_resource"
            print(f"[GỢI Ý MỞ RỘNG 3 - TEST TÀI NGUYÊN KHÔNG TỒN TẠI]: {invalid_uri}")
            await send_get_request(client_context, invalid_uri)
            return

        # 1. Gửi yêu cầu GET lần đầu
        get_res = await send_get_request(client_context, target_uri)
        if get_res is None:
            return

        print()

        # 2. Gửi yêu cầu POST
        default_payload = f"Xin chao tu CoAP Client - {STUDENT_ID} - {STUDENT_NAME}"

        if not args.loop:
            # Gửi 1 thông điệp POST tiêu chuẩn
            await send_post_request(client_context, target_uri, default_payload)

            # Gợi ý mở rộng 2: Gửi lại yêu cầu GET để kiểm chứng Server lưu và trả về thông điệp vừa gửi
            if args.verify_cache:
                print()
                print("-" * 60)
                print("[GỢI Ý MỞ RỘNG 2 - KIỂM CHỨNG SERVER LƯU THÔNG ĐIỆP GẦN NHẤT]")
                print("Gửi lại yêu cầu GET để kiểm tra payload phản hồi từ Server:")
                await send_get_request(client_context, target_uri)
                print("-" * 60)
        else:
            # Gợi ý mở rộng 1: Chế độ gửi nhiều thông điệp liên tiếp
            print(f"[GỢI Ý MỞ RỘNG 1] Gui lien tuc moi {args.interval}s (Nhan Ctrl+C de dung)...")
            count = 1
            while True:
                msg = f"{default_payload} (Lan {count})"
                await send_post_request(client_context, target_uri, msg)
                count += 1
                await asyncio.sleep(args.interval)
                print("-" * 40)

    finally:
        await client_context.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Da dung CoAP Client.")
        sys.exit(0)
