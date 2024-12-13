import customtkinter as ctk
from CTkListbox import CTkListbox  # Import CTkListbox từ module riêng

class CreateOrder(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Phần heading
        heading_frame = ctk.CTkFrame(self)
        heading_frame.pack(fill="x")  # Chiếm toàn bộ chiều ngang

        label = ctk.CTkLabel(
            heading_frame, 
            text="Đây là Trang tạo hóa đơn hàng 234567", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label.pack(pady=10)

        # Dòng kẻ ngăn cách heading và nội dung
        separator_heading = ctk.CTkFrame(self, height=2, fg_color="gray")
        separator_heading.pack(fill="x")

        # Frame content chứa 2 phần
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True)

        # Cấu hình grid cho content_frame
        content_frame.columnconfigure(0, weight=3)  # Phần danh sách bên trái chiếm nhiều không gian
        content_frame.columnconfigure(1, weight=0)  # Dòng kẻ phân cách (không chiếm thêm không gian)
        content_frame.columnconfigure(2, weight=1)  # Phần menu bên phải chiếm ít không gian
        content_frame.rowconfigure(0, weight=1)     # Đảm bảo chiếm hết chiều cao

        # Phần bên trái - danh sách
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Sử dụng CTkListbox cho danh sách
        self.listbox = CTkListbox(left_frame)
        self.listbox.pack(fill="both", expand=True)

        # Dòng kẻ ngăn cách
        separator = ctk.CTkFrame(content_frame, width=2, fg_color="gray")  # Dòng kẻ mỏng với màu xám
        separator.grid(row=0, column=1, sticky="ns")                      # Kéo dài theo chiều dọc

        # Phần bên phải - menu
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=0, column=2, sticky="nsew")

        # Menu bên phải
        button1 = ctk.CTkButton(right_frame, text="Thêm sản phẩm", command=self.add_item)
        button1.pack(pady=10)

        button2 = ctk.CTkButton(right_frame, text="Xóa sản phẩm", command=self.remove_item)
        button2.pack(pady=10)

        button3 = ctk.CTkButton(right_frame, text="Lưu hóa đơn", command=self.save_order)
        button3.pack(pady=10)

        # Footer
        footer_frame = ctk.CTkFrame(self)
        footer_frame.pack(fill="x")

        # Dòng kẻ trên Footer
        separator_footer = ctk.CTkFrame(footer_frame, height=2, fg_color="gray")
        separator_footer.pack(fill="x", side="top")

        footer_content_frame = ctk.CTkFrame(footer_frame, fg_color="lightgray", height=40)
        footer_content_frame.pack(fill="x")

        self.footer_label = ctk.CTkLabel(footer_content_frame, text="Tổng số sản phẩm: 0", font=ctk.CTkFont(size=14))
        self.footer_label.pack(side="left", padx=10)

        update_button = ctk.CTkButton(footer_content_frame, text="Cập nhật", command=self.update_footer, width=100)
        update_button.pack(side="right", padx=10)

    def add_item(self):
        # Xử lý thêm mục vào danh sách
        self.listbox.insert("end", "Sản phẩm mới")
        self.update_footer()

    def remove_item(self):
        # Xử lý xóa mục từ danh sách
        try:
            self.listbox.delete(self.listbox.curselection())
        except:
            pass
        self.update_footer()

    def save_order(self):
        # Xử lý lưu hóa đơn
        print("Hóa đơn đã được lưu")

    def update_footer(self):
        # Cập nhật tổng số sản phẩm
        total_items = self.listbox.size()
        self.footer_label.configure(text=f"Tổng số sản phẩm: {total_items}")
