import customtkinter as ctk
from PIL import Image, ImageTk 
from tkinter import messagebox
import datetime
import json

class CreateOrder(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Dữ liệu sản phẩm JSON
        self.orders_file = "../Project_QLHD/assets/data/orders.json"
        self.product_data = self.load_product_data("../Project_QLHD/assets/data/products.json")

        # Phần heading
        heading_frame = ctk.CTkFrame(self, fg_color="transparent")
        heading_frame.pack(fill="x", pady=10)

        label = ctk.CTkLabel(
            heading_frame, 
            text="Tạo đơn hàng", 
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
        self.scrollable_frame = ctk.CTkScrollableFrame(self.list_frame, height=400)  # Giới hạn chiều cao
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

        # Tạo thanh tìm kiếm
        search_label = ctk.CTkLabel(right_frame, text="Tìm kiếm sản phẩm", font=ctk.CTkFont(size=14))
        search_label.pack(pady=10)

        self.search_entry = ctk.CTkEntry(right_frame, placeholder_text="Nhập tên sản phẩm...")
        self.search_entry.pack(pady=5, padx=10)
        self.search_entry.bind("<KeyRelease>", self.update_search_results)

        # Danh sách gợi ý sản phẩm
        self.scrollable_frame_2 = ctk.CTkScrollableFrame(right_frame, height=300)  # Giới hạn chiều cao
        self.scrollable_frame_2.pack(fill="both", expand=True)
        
        self.suggestion_frame = ctk.CTkFrame(self.scrollable_frame_2)
        self.suggestion_frame.pack(fill="both", pady=5, padx=10)

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

        # Khởi tạo danh sách sản phẩm trong giỏ hàng
        self.cart = {}  # Lưu trữ sản phẩm trong giỏ hàng với key là product_id và value là số lượng

        # Hiển thị sản phẩm ban đầu (8 sản phẩm)
        self.update_search_results()

    def update_search_results(self, event=None):
        # Xóa kết quả tìm kiếm cũ
        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

        search_query = self.search_entry.get().lower()

        # Tìm kiếm các sản phẩm phù hợp
        if search_query == "":  # Nếu không có từ khóa tìm kiếm, hiển thị tất cả sản phẩm
            filtered_products = self.product_data  # Hiển thị tất cả sản phẩm trong danh sách
        else:
            filtered_products = [
                product for product in self.product_data if search_query in product["name"].lower()
            ]

        # Hiển thị gợi ý tìm kiếm
        for product in filtered_products:
            suggestion_frame = ctk.CTkFrame(self.suggestion_frame)
            suggestion_frame.pack(fill="x", pady=5)

            # Ảnh sản phẩm (Fixed kích thước hình vuông)
            img = Image.open(product["img"])  # Đọc ảnh từ đường dẫn (product["img"])
            img = img.resize((100, 100))  # Đảm bảo ảnh có kích thước 60x60
            img_tk = ImageTk.PhotoImage(img)  # Chuyển ảnh thành đối tượng có thể hiển thị trên Tkinter

            img_label = ctk.CTkLabel(suggestion_frame,text="", image=img_tk, width=60, height=60)
            img_label.grid(row=0, column=0, padx=5, pady=5)

            # Cột 2: Tên sản phẩm, Giá sản phẩm, và Nút thêm
            detail_frame = ctk.CTkFrame(suggestion_frame, fg_color="transparent")
            detail_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")

            # Dòng 1: Tên sản phẩm
            name_label = ctk.CTkLabel(detail_frame, text=product["name"], font=ctk.CTkFont(size=14))
            name_label.grid(row=0, column=0, sticky="w", padx=0)

            # Dòng 2: Giá sản phẩm
            price_label = ctk.CTkLabel(detail_frame, text=f"{product['price']:,} VND", font=ctk.CTkFont(size=12))
            price_label.grid(row=1, column=0, sticky="w", padx=0)

            # Dòng 3: Nút thêm sản phẩm vào giỏ hàng
            add_button = ctk.CTkButton(detail_frame, text="Thêm vào giỏ", command=lambda p=product: self.add_item(p))
            add_button.grid(row=2, column=0, pady=5)

            # Lưu lại đối tượng ảnh để tránh việc ảnh bị garbage collected
            img_label.image = img_tk


    def add_item(self, product):
        # Kiểm tra nếu sản phẩm đã có trong giỏ hàng
        if product["id"] in self.cart:
            # Nếu có, tăng số lượng của sản phẩm
            self.cart[product["id"]]["quantity"] += 1
            self.update_item_in_cart(product["id"])
        else:
            # Nếu chưa có, thêm sản phẩm mới vào giỏ hàng
            self.cart[product["id"]] = {"product": product, "quantity": 1}
            self.create_item_in_cart(product)

        self.update_footer()



    def create_item_in_cart(self, product):
        # Tạo một hàng mới trong danh sách giỏ hàng
        row_frame = ctk.CTkFrame(self.items_frame)
        row_frame.pack(fill="x", pady=5)

        # Cột 1: Ảnh sản phẩm
        img = Image.open(product["img"])  # Đọc ảnh từ đường dẫn (product["img"])
        img = img.resize((100, 100))  # Đảm bảo ảnh có kích thước 60x60
        img_tk = ImageTk.PhotoImage(img)
        img_label = ctk.CTkLabel(row_frame, text="", image=img_tk, width=100, height=100, fg_color="gray")  # Chiều rộng bằng chiều cao và không có màu nền
        img_label.grid(row=0, column=0, padx=5, pady=5)
        # Để hiển thị ảnh thật, bạn có thể thay bằng hình ảnh thực tế, ví dụ dùng img_label.configure(image=product["img"])

        # Cột 2: Chi tiết sản phẩm
        detail_frame = ctk.CTkFrame(row_frame, fg_color="transparent")  # Không có màu nền
        detail_frame.grid(row=0, column=1, sticky="w", padx=5)

        # Tên sản phẩm
        product_name = ctk.CTkLabel(detail_frame, text=product["name"], font=ctk.CTkFont(size=15, weight="bold"))
        product_name.grid(row=0, column=0, sticky="w")

        # Dòng hiển thị giá
        price_label = ctk.CTkLabel(detail_frame, text=f"{product['price']:,} x", font=ctk.CTkFont(size=14))
        price_label.grid(row=1, column=0, padx=(0, 5), sticky="w")

        # Số lượng trong giỏ hàng
        quantity = self.cart[product["id"]]["quantity"]  # Lấy số lượng từ giỏ hàng
        quantity_label = ctk.CTkLabel(detail_frame, text=f"{quantity}", font=ctk.CTkFont(size=14), width=30)
        quantity_label.grid(row=1, column=2, padx=10)

        def update_quantity(change):
            # Cập nhật số lượng và tổng tiền khi nhấn nút "+" hoặc "-"
            quantity = self.cart[product["id"]]["quantity"]
            quantity += change
            if quantity < 1:
                quantity = 1  # Đảm bảo số lượng không nhỏ hơn 1
            quantity_label.configure(text=f"{quantity}")
            
            total_price = quantity * product["price"]  # Tính tổng tiền
            total_label.configure(text=f" = {total_price:,} VND")
            
            # Cập nhật giỏ hàng
            self.cart[product["id"]]["quantity"] = quantity
            self.update_footer()

        minus_button = ctk.CTkButton(detail_frame, text="-", width=30, command=lambda: update_quantity(-1))
        minus_button.grid(row=1, column=1)

        plus_button = ctk.CTkButton(detail_frame, text="+", width=30, command=lambda: update_quantity(1))
        plus_button.grid(row=1, column=3)

        total_label = ctk.CTkLabel(detail_frame, text=f" = {product['price']:,} VND", font=ctk.CTkFont(size=14), width=60)
        total_label.grid(row=1, column=4, padx=10, sticky="w")

        # Cột 3: Nút xóa
        delete_button = ctk.CTkButton(row_frame, text="Xóa", width=34, command=lambda: self.remove_item(row_frame))
        delete_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")  # sticky="e" để căn sát bên phải


        # Điều chỉnh cột của grid cho các phần tử trong danh sách
        # row_frame.grid_columnconfigure(0, weight=1)  # Cột 1 chiếm không gian vừa phải
        row_frame.grid_columnconfigure(1, weight=3)  # Cột 2 chiếm nhiều không gian
        row_frame.grid_columnconfigure(2, weight=0)  # Cột 3 chiếm ít không gian (nút xóa)



    def update_item_in_cart(self, product_id):
        # Cập nhật số lượng của sản phẩm trong giỏ hàng
        product = self.cart[product_id]["product"]
        quantity = self.cart[product_id]["quantity"]
        
        # Cập nhật lại số lượng trong giỏ hàng
        for widget in self.items_frame.winfo_children():
            row_frame = widget
            product_name_label = row_frame.winfo_children()[1].winfo_children()[0]  # Label tên sản phẩm
            if product_name_label.cget("text") == product["name"]:
                quantity_label = row_frame.winfo_children()[1].winfo_children()[2]  # Label số lượng
                quantity_label.configure(text=f"{quantity}")
                total_label = row_frame.winfo_children()[1].winfo_children()[5]  # Label tổng tiền
                total_label.configure(text=f" = {quantity * product['price']:,} VND")
                break

        self.update_footer()

    def update_footer(self):
        total_quantity = sum(item["quantity"] for item in self.cart.values())
        total_amount = sum(item["quantity"] * item["product"]["price"] for item in self.cart.values())

        self.quantity_value_label.configure(text=str(total_quantity))
        self.total_value_label.configure(text=f"{total_amount:,} VND")

    def remove_item(self, row_frame):
        # Lấy tên sản phẩm từ row_frame
        product_name = row_frame.winfo_children()[1].winfo_children()[0].cget("text")
        
        # Tìm ID sản phẩm từ dữ liệu sản phẩm
        product_id = None
        for product in self.product_data:
            if product["name"] == product_name:
                product_id = product["id"]
                break
        
        if product_id is not None:
            # Xóa sản phẩm khỏi giỏ hàng
            del self.cart[product_id]
        
        # Xóa widget khỏi giao diện
        row_frame.destroy()

        # Cập nhật lại thông tin giỏ hàng ở footer
        self.update_footer()

    def load_product_data(self, file_path):
        # Đọc và trả về dữ liệu từ file JSON
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def payment(self):
        if not self.cart:
            messagebox.showinfo("Thông báo", "Giỏ hàng trống, không thể thanh toán.")
            return

        # Đọc dữ liệu từ file orders.json
        try:
            with open(self.orders_file, "r", encoding="utf-8") as file:
                orders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            orders = []

        # Xóa tất cả sản phẩm trong danh sách orders

        # Lấy ngày hiện tại với định dạng dd-mm-yyyy
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")

        # Tạo đơn hàng mới
        new_order = {
            "id": len(orders) + 1,
            "date": current_date,
            "products": [
                {
                    "id": item["product"]["id"],
                    "quantity": item["quantity"]
                } for item in self.cart.values()
            ],
            "total_quantity": sum(item["quantity"] for item in self.cart.values()),
            "total_cost": sum(item["product"]["price"] * item["quantity"] for item in self.cart.values())
        }
        orders.append(new_order)

        # Ghi dữ liệu mới vào file orders.json
        try:
            with open(self.orders_file, "w", encoding="utf-8") as file:
                json.dump(orders, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể ghi vào file: {e}")
            return

        # Làm trống giỏ hàng
        self.cart.clear()

        # Cập nhật lại footer và danh sách hiển thị giỏ hàng
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        self.update_footer()

        # Hiển thị thông báo thành công
        messagebox.showinfo("Thông báo", "Thanh toán thành công!")
        print("Đơn hàng mới:", new_order)