import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json
import shutil
import uuid
import os

class ManagerProducts(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        heading_frame = ctk.CTkFrame(self, fg_color="transparent")
        heading_frame.pack(fill="x", pady=10)

        label = ctk.CTkLabel(
            heading_frame, 
            text="Quản lý sản phẩm", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label.pack(pady=10)

        # Dòng kẻ ngăn cách heading và nội dung
        separator_heading = ctk.CTkFrame(self, height=2, fg_color="gray")
        separator_heading.pack(fill="x", pady=0)

        # Frame content chứa 2 phần
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True)

        # Cấu hình grid cho content_frame
        content_frame.columnconfigure(0, weight=3)  # Phần danh sách bên trái chiếm nhiều không gian
        content_frame.columnconfigure(1, weight=0)  # Dòng kẻ phân cách (không chiếm thêm không gian)
        content_frame.columnconfigure(2, weight=1)  # Phần menu bên phải chiếm ít không gian
        content_frame.rowconfigure(0, weight=1)     # Đảm bảo chiếm hết chiều cao

        # Phần bên trái - danh sách sản phẩm
        self.scrollable_frame = ctk.CTkScrollableFrame(content_frame)
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Phần bên phải - menu
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=0, pady=0)
        separator = ctk.CTkFrame(content_frame, width=2, fg_color="gray")  # Dòng kẻ mỏng với màu xám
        separator.grid(row=0, column=1, sticky="ns")   
        # Nút chọn ảnh
        self.selected_image = None
        self.preview_label = ctk.CTkLabel(right_frame, text="", width=150, height=150, fg_color="lightgray")
        self.preview_label.pack(pady=10)

        self.select_image_button = ctk.CTkButton(right_frame, text="Chọn ảnh", command=self.select_image)
        self.select_image_button.pack(pady=10)

        # Entry cho tên sản phẩm và giá
        self.product_name_entry = ctk.CTkEntry(right_frame, placeholder_text="Tên sản phẩm")
        self.product_name_entry.pack(pady=5)

        self.product_price_entry = ctk.CTkEntry(right_frame, placeholder_text="Giá sản phẩm")
        self.product_price_entry.pack(pady=5)

        # Menu bên phải
        button1 = ctk.CTkButton(right_frame, text="Thêm sản phẩm", command=self.add_item)
        button1.pack(pady=10)

        # Nút cập nhật
        update_button = ctk.CTkButton(right_frame, text="Cập nhật", command=self.update_products, width=100)
        update_button.pack(pady=10)

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

        # Khởi tạo danh sách sản phẩm
        self.product_list = []

        # Đọc dữ liệu từ file products.json và hiển thị lên giao diện
        self.load_products()

    def load_products(self):
        """Đọc sản phẩm từ tệp products.json và hiển thị chúng vào giao diện."""
        for product in self.product_list:
            product["frame"].destroy()
        self.product_list.clear()

        try:
            with open("../Project_QLHD/assets/data/products.json", "r", encoding="utf-8") as file:
                products = json.load(file)

            for product in products:
                self.display_product(product)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Lỗi khi đọc file sản phẩm: {e}")

    def update_products(self):
        """Lưu danh sách sản phẩm vào tệp products.json và thông báo cập nhật thành công."""
        self.save_products()
        messagebox.showinfo("Cập nhật", "Cập nhật danh sách sản phẩm thành công!")

    def save_products(self):
        """Lưu danh sách sản phẩm vào tệp products.json."""
        try:
            # Đảm bảo thư mục chứa tệp đã tồn tại
            if not os.path.exists("../Project_QLHD/assets/data"):
                os.makedirs("../Project_QLHD/assets/data")
            if not os.path.exists("../Project_QLHD/assets/imgs"):
                os.makedirs("../Project_QLHD/assets/imgs")

            # Chuyển đổi danh sách sản phẩm thành định dạng phù hợp với JSON
            products_to_save = [{
                "id": product["id"],
                "name": product["name"],
                "price": int(product["price"]),
                "img": product["image"]  # Đường dẫn ảnh mới sẽ là tên ảnh
            } for product in self.product_list]

            with open("../Project_QLHD/assets/data/products.json", "w", encoding="utf-8") as file:
                json.dump(products_to_save, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Lỗi khi lưu sản phẩm vào tệp: {e}")

    def display_product(self, product):
        """Hiển thị sản phẩm vào giao diện."""
        product_frame = ctk.CTkFrame(self.scrollable_frame)
        product_frame.pack(fill="x", pady=5)

        # Hiển thị ảnh sản phẩm
        image = Image.open(product["img"])
        image = image.resize((100, 100))  # Resize ảnh cho vừa
        photo = ImageTk.PhotoImage(image)
        img_label = ctk.CTkLabel(product_frame, text="", image=photo, width=100, height=100, fg_color="transparent")
        img_label.image = photo  # Giữ tham chiếu ảnh
        img_label.pack(side="left", padx=10)

        # Hiển thị tên sản phẩm
        name_label = ctk.CTkLabel(product_frame, text=product["name"], font=ctk.CTkFont(size=18), anchor="w")
        name_label.pack(anchor="w")

        # Hiển thị giá sản phẩm
        price_label = ctk.CTkLabel(product_frame, text=f"{product['price']:,} VND", anchor="w")
        price_label.pack(anchor="w")

        # Tạo nút xóa cho sản phẩm
        delete_button = ctk.CTkButton(product_frame, text="Xóa", command=lambda: self.remove_specific_item(product_frame))
        delete_button.pack(side="right", padx=10)

        # Thêm sản phẩm vào danh sách
        self.product_list.append({
            "id" : uuid.uuid4() ,
            "name": product["name"],
            "price": int(product["price"]),
            "image": product["img"],
            "frame": product_frame  # Lưu lại frame của sản phẩm
        })

        # Cập nhật footer
        self.update_footer()

    def select_image(self):
        """Mở hộp thoại để chọn ảnh."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.selected_image = file_path
            # Hiển thị ảnh preview
            image = Image.open(self.selected_image)
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo  # Giữ tham chiếu ảnh

    def add_item(self):
        """Thêm sản phẩm vào danh sách."""
        product_name = self.product_name_entry.get()
        product_price = int(self.product_price_entry.get())

        if product_name and product_price and self.selected_image:
            # Tạo ID duy nhất cho ảnh
            image_id = str(len(self.product_list))  # Tạo ID duy nhất cho ảnh
            image_extension = self.selected_image.split('.')[-1]  # Lấy phần mở rộng của ảnh
            new_image_path = f"../Project_QLHD/assets/imgs/{image_id}.png"  # Đặt tên mới cho ảnh

            # Sao chép ảnh vào thư mục imgs
            try:
                shutil.copy(self.selected_image, new_image_path)
            except Exception as e:
                print(f"Lỗi khi sao chép ảnh: {e}")
                return

            # Tạo khung cho sản phẩm
            product_frame = ctk.CTkFrame(self.scrollable_frame)
            product_frame.pack(fill="x", pady=5)

            # Hiển thị ảnh sản phẩm
            image = Image.open(new_image_path)
            image = image.resize((100, 100))  # Resize ảnh cho vừa
            photo = ImageTk.PhotoImage(image)
            img_label = ctk.CTkLabel(product_frame, text="", image=photo, width=100, height=100, fg_color="transparent")
            img_label.image = photo  # Giữ tham chiếu ảnh
            img_label.pack(side="left", padx=10)

            # Hiển thị tên sản phẩm
            name_label = ctk.CTkLabel(product_frame, text=product_name, font=ctk.CTkFont(size=18), anchor="w")
            name_label.pack(anchor="w")

            # Hiển thị giá sản phẩm
            price_label = ctk.CTkLabel(product_frame, text=f"{product_price:,} VND", anchor="w")
            price_label.pack(anchor="w")

            # Tạo nút xóa cho sản phẩm
            delete_button = ctk.CTkButton(product_frame, text="Xóa", command=lambda: self.remove_specific_item(product_frame))
            delete_button.pack(side="right", padx=10)

            # Thêm sản phẩm vào danh sách
            self.product_list.append({
                "id" : uuid.uuid4() ,
                "name": product_name,
                "price": int(product_price),
                "image": new_image_path,  # Lưu đường dẫn ảnh mới
                "frame": product_frame  # Lưu lại frame của sản phẩm
            })

            # Cập nhật footer
            self.update_footer()

            # Reset các trường nhập
            self.product_name_entry.delete(0, "end")
            self.product_price_entry.delete(0, "end")
            self.selected_image = None

            # Xóa ảnh preview
            self.preview_label.configure(image=None, text="", fg_color="lightgray")
            self.preview_label.image = None
        else:
            print("Vui lòng nhập đầy đủ thông tin sản phẩm và chọn ảnh.")

    def remove_specific_item(self, product_frame):
        """Xóa sản phẩm khỏi danh sách."""
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sản phẩm này?")
        if confirm:
            for product in self.product_list:
                if product["frame"] == product_frame:
                    self.product_list.remove(product)
                    break

            # Xóa frame của sản phẩm từ giao diện
            product_frame.destroy()

            # Cập nhật footer
            self.update_footer()

    def update_footer(self):
        """Cập nhật tổng số sản phẩm và lưu vào file."""
        total_items = len(self.product_list)
        self.footer_label.configure(text=f"Tổng số sản phẩm: {total_items}")
