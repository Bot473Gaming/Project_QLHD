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
            print(f"Thư viện '{library}' đã được cài đặt.")
        except ImportError:
            print(f"Thư viện '{library}' chưa được cài đặt. Đang cài đặt...\n")
            try:
                # Cài đặt thư viện và hiển thị quá trình
                subprocess.check_call([sys.executable, "-m", "pip", "install", library], stdout=sys.stdout, stderr=sys.stderr)
                print(f"Thư viện '{library}' đã được cài đặt thành công.\n")
            except subprocess.CalledProcessError:
                print(f"Không thể cài đặt thư viện '{library}'. Hãy kiểm tra kết nối mạng hoặc cấu hình Python.")
                sys.exit(1)  # Thoát chương trình nếu cài đặt thất bại

def run_main_file():
    print("Tất cả các thư viện đã được cài đặt. Chạy file main.py...\n")
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    install_and_check_libraries()
    run_main_file()
