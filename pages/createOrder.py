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
        footer_frame.pack(fill="x", pady=10)

        footer_content_frame = ctk.CTkFrame(footer_frame, height=80)  # Tăng chiều cao footer
        footer_content_frame.pack(fill="x")

        # Tạo một frame chứa số lượng và tổng tiền với độ rộng tối thiểu và căn phải
        footer_left_frame = ctk.CTkFrame(footer_content_frame, fg_color="transparent", width=300)
        footer_left_frame.pack(side="left", padx=20, anchor="w")

        # Hiển thị số lượng và tổng tiền bên phải
        self.quantity_label = ctk.CTkLabel(footer_left_frame, text="Số lượng:", font=ctk.CTkFont(size=16))
        self.quantity_label.pack(side="left", anchor="w", padx=5)

        self.quantity_value_label = ctk.CTkLabel(footer_left_frame, text="0", font=ctk.CTkFont(size=16))
        self.quantity_value_label.pack(side="left", anchor="e", padx=5)

        self.total_label = ctk.CTkLabel(footer_left_frame, text="Tổng tiền:", font=ctk.CTkFont(size=16))
        self.total_label.pack(side="left", anchor="w", padx=5)

        self.total_value_label = ctk.CTkLabel(footer_left_frame, text="0 VND", font=ctk.CTkFont(size=16))
        self.total_value_label.pack(side="left", anchor="e", padx=5)

        # Tạo frame bên phải để căn giữa nút thanh toán
        footer_right_frame = ctk.CTkFrame(footer_content_frame, fg_color="transparent")
        footer_right_frame.pack(side="right", padx=20)

        # Nút thanh toán căn giữa
        pay_button = ctk.CTkButton(footer_right_frame, text="Thanh toán", command=self.payment, width=120)
        pay_button.pack(pady=10)

    def add_item(self):
        # Tạo một hàng mới trong danh sách
        row_frame = ctk.CTkFrame(self.items_frame)
        row_frame.pack(fill="x", pady=5)

        # Cột 1: Ảnh sản phẩm
        img_label = ctk.CTkLabel(row_frame, text="[Ảnh]", width=60, height=60, fg_color="transparent")  # Chiều rộng bằng chiều cao và không có màu nền
        img_label.grid(row=0, column=0, padx=5, pady=5)

        # Cột 2: Chi tiết sản phẩm
        detail_frame = ctk.CTkFrame(row_frame, fg_color="transparent")  # Không có màu nền
        detail_frame.grid(row=0, column=1, sticky="w", padx=5)

        product_name = ctk.CTkLabel(detail_frame, text="Tên sản phẩm", font=ctk.CTkFont(size=14, weight="bold"))
        product_name.grid(row=0, column=0, sticky="w")

        # Dòng hiển thị giá và số lượng
        price_label = ctk.CTkLabel(detail_frame, text="100 x", font=ctk.CTkFont(size=12))
        price_label.grid(row=1, column=0, sticky="w")

        # Nút giảm, số lượng và nút tăng
        quantity = 1  # Mỗi sản phẩm có số lượng riêng biệt
        quantity_label = ctk.CTkLabel(detail_frame, text=f"{quantity}", font=ctk.CTkFont(size=12), width=30)
        quantity_label.grid(row=1, column=2, padx=10)

        def update_quantity(change):
            # Cập nhật số lượng và tổng tiền khi nhấn nút "+" hoặc "-"
            nonlocal quantity
            quantity += change
            if quantity < 1:
                quantity = 1  # Đảm bảo số lượng không nhỏ hơn 1
            quantity_label.configure(text=f"{quantity}")
            
            total_price = quantity * 100  # Tính tổng tiền (giả sử giá đơn vị là 100)
            total_label.configure(text=f" = {total_price} VND")
            self.update_footer()

        minus_button = ctk.CTkButton(detail_frame, text="-", width=30, command=lambda: update_quantity(-1))
        minus_button.grid(row=1, column=1)

        plus_button = ctk.CTkButton(detail_frame, text="+", width=30, command=lambda: update_quantity(1))
        plus_button.grid(row=1, column=3)

        total_label = ctk.CTkLabel(detail_frame, text=" = 100 VND", font=ctk.CTkFont(size=12))  # Thêm "VND"
        total_label.grid(row=1, column=4, sticky="w")

        # Cột 3: Nút xóa
        delete_button = ctk.CTkButton(row_frame, text="Xóa", command=lambda: self.remove_item(row_frame))
        delete_button.grid(row=0, column=2, padx=10)

        # Điều chỉnh cột của grid cho các phần tử trong danh sách
        row_frame.grid_columnconfigure(0, weight=1)  # Cột 1 chiếm không gian vừa phải
        row_frame.grid_columnconfigure(1, weight=3)  # Cột 2 chiếm nhiều không gian
        row_frame.grid_columnconfigure(2, weight=0)  # Cột 3 chiếm ít không gian (nút xóa)

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
        total_items = 0  # Tổng số lượng sản phẩm
        total_money = 0  # Tổng tiền

        for item in self.items_frame.winfo_children():
            # Tìm label số lượng của mỗi sản phẩm (nó nằm trong phần chi tiết sản phẩm)
            quantity_label = item.winfo_children()[1].winfo_children()[2]
            quantity = int(quantity_label.cget("text"))
            total_items += quantity

            # Tìm label tổng tiền của mỗi sản phẩm
            price_label = item.winfo_children()[1].winfo_children()[5]  # label tổng tiền
            price_text = price_label.cget("text")
            total_money += int(price_text.split(" = ")[1].replace(" VND", ""))

        # Cập nhật giá trị số lượng và tổng tiền trên footer
        self.quantity_value_label.configure(text=f"{total_items}")
        self.total_value_label.configure(text=f"{total_money} VND")

    def payment(self):
        # Xử lý thanh toán
        print("Thanh toán thành công")
        self.clear_list()
