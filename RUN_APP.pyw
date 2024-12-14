import subprocess
import sys

# Danh sách các thư viện cần thiết
required_libraries = [
    "customtkinter",
    "pillow",
    "matplotlib"
]

def install_and_check_libraries():
    for library in required_libraries:
        try:
            # Kiểm tra xem thư viện đã được cài đặt chưa
            __import__(library)
        except ImportError:
            print(f"Thư viện '{library}' chưa được cài đặt. Đang cài đặt...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])

def run_main_file():
    print("Tất cả các thư viện đã được cài đặt. Chạy file main.py...")
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    install_and_check_libraries()
    run_main_file()
