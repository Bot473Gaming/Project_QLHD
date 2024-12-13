import customtkinter as ctk

class CreateOrder(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Phần heading
        heading_frame = ctk.CTkFrame(self)
        heading_frame.pack(fill="x", pady=10)

        label = ctk.CTkLabel(
            heading_frame, 
            text="Đây là Trang tạo hóa đơn hàng 234567", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label.pack(pady=10)

        # Dòng kẻ ngăn cách heading và nội dung
        separator_heading = ctk.CTkFrame(self, height=2, fg_color="gray")
        separator_heading.pack(fill="x", pady=10)

        # Frame content chứa 2 phần
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True)

        # Cấu hình grid cho content_frame
        content_frame.columnconfigure(0, weight=3)  # Phần danh sách bên trái chiếm nhiều không gian
        content_frame.columnconfigure(1, weight=0)  # Dòng kẻ phân cách (không chiếm thêm không gian)
        content_frame.columnconfigure(2, weight=1)  # Phần menu bên phải chiếm ít không gian
        content_frame.rowconfigure(0, weight=1)     # Đảm bảo chiếm hết chiều cao

        # Phần bên trái - danh sách
        self.list_frame = ctk.CTkFrame(content_frame)
        self.list_frame.grid(row=0, column=0, sticky="nsew")

        # Sử dụng CTkScrollableFrame để có thể cuộn
        self.scrollable_frame = ctk.CTkScrollableFrame(self.list_frame)
        self.scrollable_frame.pack(fill="both", expand=True)

        # Nội dung danh sách
        self.items_frame = ctk.CTkFrame(self.scrollable_frame)
        self.items_frame.pack(fill="both", expand=True)

        # Dòng kẻ ngăn cách
        separator = ctk.CTkFrame(content_frame, width=2, fg_color="gray")  # Dòng kẻ mỏng với màu xám
        separator.grid(row=0, column=1, sticky="ns")                      # Kéo dài theo chiều dọc

        # Phần bên phải - menu
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=0, column=2, sticky="nsew")

        # Menu bên phải
        button1 = ctk.CTkButton(right_frame, text="Thêm sản phẩm", command=self.add_item)
        button1.pack(pady=10)

        button2 = ctk.CTkButton(right_frame, text="Xóa tất cả", command=self.clear_list)
        button2.pack(pady=10)

        # Footer
        footer_frame = ctk.CTkFrame(self)
        footer_frame.pack(fill="x")

        # Dòng kẻ trên Footer
        separator_footer = ctk.CTkFrame(footer_frame, height=2, fg_color="gray")
        separator_footer.pack(fill="x", side="top")

        footer_content_frame = ctk.CTkFrame(footer_frame, height=40)
        footer_content_frame.pack(fill="x")

        self.footer_label = ctk.CTkLabel(footer_content_frame, text="Tổng tiền: 0, Tổng số sản phẩm: 0", font=ctk.CTkFont(size=14))
        self.footer_label.pack(side="left", padx=10)

        pay_button = ctk.CTkButton(footer_content_frame, text="Thanh toán", command=self.payment, width=100)
        pay_button.pack(side="right", padx=10)

    def add_item(self):
        # Tạo một hàng mới trong danh sách
        row_frame = ctk.CTkFrame(self.items_frame)
        row_frame.pack(fill="x", pady=5)

        # Cột 1: Ảnh sản phẩm
        img_label = ctk.CTkLabel(row_frame, text="[Ảnh]", width=60, height=60)  # Chiều rộng bằng chiều cao
        img_label.grid(row=0, column=0, padx=5, pady=5)

        # Cột 2: Chi tiết sản phẩm
        detail_frame = ctk.CTkFrame(row_frame)
        detail_frame.grid(row=0, column=1, sticky="w", padx=5)

        product_name = ctk.CTkLabel(detail_frame, text="Tên sản phẩm", font=ctk.CTkFont(size=14, weight="bold"))
        product_name.grid(row=0, column=0, sticky="w")

        # Dòng hiển thị giá và số lượng
        price_label = ctk.CTkLabel(detail_frame, text="100 x", font=ctk.CTkFont(size=12))
        price_label.grid(row=1, column=0, sticky="w")

        # Nút giảm, số lượng và nút tăng
        self.quantity = 1  # Số lượng mặc định
        minus_button = ctk.CTkButton(detail_frame, text="-", width=30, command=lambda: self.update_quantity(-1, price_label))
        minus_button.grid(row=1, column=1)

        quantity_label = ctk.CTkLabel(detail_frame, text=f"{self.quantity}", font=ctk.CTkFont(size=12), width=30)
        quantity_label.grid(row=1, column=2, padx=10)

        plus_button = ctk.CTkButton(detail_frame, text="+", width=30, command=lambda: self.update_quantity(1, price_label))
        plus_button.grid(row=1, column=3)

        total_label = ctk.CTkLabel(detail_frame, text=" = 100", font=ctk.CTkFont(size=12))
        total_label.grid(row=1, column=4, sticky="w")

        # Cột 3: Nút xóa
        delete_button = ctk.CTkButton(row_frame, text="Xóa", command=lambda: self.remove_item(row_frame))
        delete_button.grid(row=0, column=2, padx=10)

        # Điều chỉnh cột của grid cho các phần tử trong danh sách
        row_frame.grid_columnconfigure(0, weight=1)  # Cột 1 chiếm không gian vừa phải
        row_frame.grid_columnconfigure(1, weight=3)  # Cột 2 chiếm nhiều không gian
        row_frame.grid_columnconfigure(2, weight=0)  # Cột 3 chiếm ít không gian (nút xóa)

        self.update_footer()

    def update_quantity(self, change, price_label):
        # Cập nhật số lượng khi nhấn nút "+" hoặc "-"
        self.quantity += change
        if self.quantity < 1:
            self.quantity = 1  # Đảm bảo số lượng không nhỏ hơn 1
        # Cập nhật số lượng và tính lại tổng tiền
        quantity_label = price_label.master.winfo_children()[2]  # Lấy label hiển thị số lượng
        quantity_label.configure(text=f"{self.quantity}")
        
        total_label = price_label.master.winfo_children()[4]
        total_price = self.quantity * 100  # Assuming unit price is 100
        total_label.configure(text=f" = {total_price}")

        self.update_footer()

    def remove_item(self, row_frame):
        # Xóa sản phẩm
        row_frame.destroy()
        self.update_footer()

    def clear_list(self):
        # Xóa toàn bộ sản phẩm
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        self.update_footer()

    def update_footer(self):
        # Cập nhật tổng số sản phẩm và tổng tiền
        total_items = len(self.items_frame.winfo_children())
        total_money = 0
        for item in self.items_frame.winfo_children():
            # Lấy thông tin tổng tiền từ label
            price_label = item.winfo_children()[1].winfo_children()[4]  # label tổng tiền
            price_text = price_label.cget("text")
            total_money += int(price_text.split(" = ")[1])

        self.footer_label.configure(text=f"Tổng tiền: {total_money}, Tổng số sản phẩm: {total_items}")

    def payment(self):
        # Xử lý thanh toán
        print("Thanh toán thành công")
        self.clear_list()

