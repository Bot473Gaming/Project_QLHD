import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import json
import shutil
import uuid
import os

class ProductManagement(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.products_file = self.get_path("assets", "data", "products.json")
        # print(self.BASE_DIR,"BASE_DIR")
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
        self.preview_label = ctk.CTkLabel(right_frame, text="", width=200, height=200, fg_color="lightgray")
        self.preview_label.pack(pady=10)

        self.select_image_button = ctk.CTkButton(right_frame, text="Chọn ảnh", width=200, command=self.select_image)
        self.select_image_button.pack(pady=10)

        # Entry cho tên sản phẩm và giá
        self.product_name_entry = ctk.CTkEntry(right_frame, placeholder_text="Tên sản phẩm", width=200, font=ctk.CTkFont(size=18))
        self.product_name_entry.pack(pady=5)

        self.product_price_entry = ctk.CTkEntry(right_frame, placeholder_text="Giá sản phẩm", width=200, font=ctk.CTkFont(size=18))
        self.product_price_entry.pack(pady=5)
    
        # Menu bên phải
        self.editing_product = None  # Lưu ID sản phẩm đang sửa
        # Nút sửa và hủy sẽ xuất hiện trong chế độ chỉnh sửa
        self.save_button = ctk.CTkButton(right_frame, text="Lưu", width=200, command=self.save_edited_item, state="disabled")
        self.cancel_button = ctk.CTkButton(right_frame, text="Hủy", width=200, command=self.cancel_edit, state="disabled")
        self.save_button.pack_forget()
        self.cancel_button.pack_forget()
        # Nút Thêm 
        self.add_new_button = ctk.CTkButton(right_frame, text="Thêm sản phẩm", width=200, command=self.add_item)
        self.add_new_button.pack(pady=10)

        # Nút cập nhật
        update_button = ctk.CTkButton(right_frame, text="Cập nhật", width=200, command=self.update_products)
        update_button.pack(pady=50, side="bottom")

        # Footer
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x")

        # Dòng kẻ trên Footer
        separator_footer = ctk.CTkFrame(footer_frame, height=2, fg_color="gray")
        separator_footer.pack(fill="x", side="top")

        footer_content_frame = ctk.CTkFrame(footer_frame, height=40)
        footer_content_frame.pack(fill="x")

        self.footer_label = ctk.CTkLabel(footer_content_frame, text="Tổng số sản phẩm: 0", font=ctk.CTkFont(size=18))
        self.footer_label.pack(side="left", padx=10, pady=24)

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
            with open(self.products_file, "r", encoding="utf-8") as file:
                products = json.load(file)

            for product in products:
                self.display_product(product)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showinfo("Lỗi khi đọc file sản phẩm", e)
            print(f"Lỗi khi đọc file sản phẩm: {e}")

    def update_products(self):
        """Lưu danh sách sản phẩm vào tệp products.json và thông báo cập nhật thành công."""
        self.save_products()
        messagebox.showinfo("Cập nhật", "Cập nhật danh sách sản phẩm thành công!")

    def save_products(self):
        """Lưu danh sách sản phẩm vào tệp products.json."""
        try:
            # Đảm bảo thư mục chứa tệp đã tồn tại
            # if not os.path.exists("../Project_QLHD/assets/data"):
            #     os.makedirs("../Project_QLHD/assets/data")
            # if not os.path.exists("../Project_QLHD/assets/imgs"):
            #     os.makedirs("../Project_QLHD/assets/imgs")

            # Chuyển đổi danh sách sản phẩm thành định dạng phù hợp với JSON
            products_to_save = [{
                "id": product["id"],
                "name": product["name"],
                "price": int(product["price"]),
                "img": product["img"]  # Đường dẫn ảnh mới sẽ là tên ảnh
            } for product in self.product_list]
            print("================================")
            print(products_to_save)
            print("================================")
            with open(self.products_file, "w", encoding="utf-8") as file:
                json.dump(products_to_save, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showinfo("Lỗi khi lưu sản phẩm vào tệp", e)
            print(f"Lỗi khi lưu sản phẩm vào tệp: {e}")

    def display_product(self, product):
        """Hiển thị sản phẩm vào giao diện (có nút sửa)."""
        product_frame = ctk.CTkFrame(self.scrollable_frame)
        product_frame.pack(fill="x", pady=5)

        # Hiển thị ảnh sản phẩm
        image_path = self.get_path("assets", "imgs", product["img"])
        image = Image.open(image_path)
        image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(image)
        
        img_label = ctk.CTkLabel(product_frame, text="", image=photo, width=100, height=100, fg_color="transparent")
        img_label.image = photo  # Giữ tham chiếu ảnh
        img_label.grid(row=0, column=0, padx=0, pady=0)

        detail_frame = ctk.CTkFrame(product_frame, fg_color="transparent")
        detail_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        # Hiển thị tên sản phẩm
        name_label = ctk.CTkLabel(detail_frame, text=product["name"], font=ctk.CTkFont(size=18))
        name_label.grid(row=0, column=0, sticky="w", padx=0)

        # Dòng 2: Giá sản phẩm
        price_label = ctk.CTkLabel(detail_frame, text=f"{product['price']:,} VND", font=ctk.CTkFont(size=16))
        price_label.grid(row=1, column=0, sticky="w", padx=0)

        # Frame chứa các nút "Sửa" và "Xóa"
        
        button_frame = ctk.CTkFrame(product_frame, fg_color="transparent")
        button_frame.grid(row=0, column=2, padx=15, pady=0, sticky="e")  # Đặt ở góc phải của sản phẩm
        
        # product_frame.columnconfigure(0, weight=1)  # Phần danh sách bên trái chiếm nhiều không gian
        product_frame.columnconfigure(1, weight=2)  # Dòng kẻ phân cách (không chiếm thêm không gian)
        product_frame.columnconfigure(2, weight=1)

        # Nút "Sửa"
        edit_button = ctk.CTkButton(
            button_frame,
            text="Sửa",
            command=lambda: self.enable_edit_mode(product),
            width=50,  # Kích thước nhỏ hơn
            font=ctk.CTkFont(size=14)  # Font nhỏ hơn
        )
        edit_button.grid(row=0, column=0, sticky="e", pady=(0, 2))  # Căn phải và cách nút dưới một khoảng

        # Nút "Xóa"
        delete_button = ctk.CTkButton(
            button_frame,
            text="Xóa",
            command=lambda: self.remove_specific_item(product_frame),
            width=50,  # Kích thước nhỏ hơn
            font=ctk.CTkFont(size=14)  # Font nhỏ hơn
        )
        delete_button.grid(row=1, column=0, sticky="e", pady=(2, 0))  # Căn phải và cách nút trên một khoảng

        # Thêm sản phẩm vào danh sách
        self.product_list.append({
            "id": product["id"],
            "name": product["name"],
            "price": int(product["price"]),
            "img": product["img"],
            "frame": product_frame
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
        product_price = (self.product_price_entry.get())
        if product_price == '' or product_name == '':
            messagebox.showinfo("Lỗi không có thông tin về sản phẩm", "Lỗi không có thông tin về sản phẩm")
            return
        product_price = int(product_price)
        
        if product_name and product_price and self.selected_image:
            # Tạo ID duy nhất cho ảnh
            image_id = str(uuid.uuid4())  # Tạo ID duy nhất cho ảnh
            image_extension = self.selected_image.split('.')[-1]  # Lấy phần mở rộng của ảnh# Đặt tên mới cho ảnh
            new_image_path = self.get_path("assets", "imgs", f"{image_id}.png") # Đặt tên mới cho ảnh

            # Sao chép ảnh vào thư mục imgs
            try:
                shutil.copy(self.selected_image, new_image_path)
            except Exception as e:
                messagebox.showinfo("Lỗi khi sao chép ảnh:", e)
                print(f"Lỗi khi sao chép ảnh: {e}")
                return

            # Thêm sản phẩm vào danh sách
            new_product = {
                "id" : str(uuid.uuid4()) ,
                "name": product_name,
                "price":int(product_price),
                "img": f"{image_id}.png",  # Lưu đường dẫn ảnh mới
            }
            self.display_product(new_product)
            # Cập nhật footer
            self.update_footer()

            # Reset các trường nhập
            self.product_name_entry.delete(0, "end")
            self.product_price_entry.delete(0, "end")
            self.selected_image = ""

            # Xóa ảnh preview
            self.preview_label.configure(image="", text="", fg_color="lightgray")
            self.preview_label.image = ""
        else:
            messagebox.showinfo("Lỗi", "Vui lòng nhập đầy đủ thông tin sản phẩm và chọn ảnh.")
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
            self.cancel_edit()
            # Cập nhật footer
            self.update_footer()


    # EDIT PRODUCT
    def enable_edit_mode(self, product):
        """Kích hoạt chế độ sửa sản phẩm."""
        self.editing_product = product["id"]

        # Hiển thị thông tin sản phẩm vào các trường nhập liệu
        self.product_name_entry.delete(0, "end")
        self.product_name_entry.insert(0, product["name"])
        self.product_price_entry.delete(0, "end")
        self.product_price_entry.insert(0, str(product["price"]))

        # Hiển thị ảnh preview
        image_path = self.get_path("assets", "imgs", product["img"])
        image = Image.open(image_path)
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)
        self.preview_label.configure(image=photo, text="")
        self.preview_label.image = photo  # Giữ tham chiếu ảnh

        # Ẩn nút "Thêm sản phẩm" và hiển thị nút "Lưu" và "Hủy"
        self.select_image_button.pack(pady=0)  # Hiển thị lại nút chọn ảnh
        self.save_button.configure(state="normal")
        self.cancel_button.configure(state="normal")
        self.save_button.pack(pady=10)
        self.cancel_button.pack(pady=10)
        self.add_new_button.configure(state="disabled")
        self.add_new_button.pack_forget()
        
    
    def cancel_edit(self):
        """Hủy chế độ chỉnh sửa."""
        self.editing_product = None

        # Reset các trường nhập liệu
        self.product_name_entry.delete(0, "end")
        self.product_price_entry.delete(0, "end")
        self.preview_label.configure(image="", text="", fg_color="lightgray")
        self.preview_label.image = ""

        # Ẩn nút "Lưu" và "Hủy", hiển thị lại nút "Thêm sản phẩm"
        self.save_button.pack_forget()
        self.cancel_button.pack_forget()
        self.add_new_button.pack(pady=10)
        self.add_new_button.configure(state="normal")
        
    def save_edited_item(self):
        """Lưu thông tin sản phẩm đã chỉnh sửa."""
        if not self.editing_product:
            return
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn sửa sản phẩm này?")
        if not confirm:
            return
        product_name = self.product_name_entry.get()
        product_price = int(self.product_price_entry.get())

        # Tìm sản phẩm trong danh sách
        for product in self.product_list:
            if product["id"] == self.editing_product:
                product["name"] = product_name
                product["price"] = product_price

                # Nếu có ảnh mới, cập nhật ảnh
                if self.selected_image:
                    image_id = str(uuid.uuid4()) + ".png"
                    new_image_path = self.get_path("assets", "imgs", image_id)
                    shutil.copy(self.selected_image, new_image_path)
                    product["img"] = image_id
                    self.selected_image = None

                # Cập nhật giao diện hiển thị
                self.update_frame_item(product)
                self.cancel_edit()
                break
        
    def update_frame_item(self, product):
        img_label = product["frame"].winfo_children()[0]
        detail_product = product["frame"].winfo_children()[1]
        name_label = detail_product.winfo_children()[0]
        price_label = detail_product.winfo_children()[1]
        image_path = self.get_path("assets", "imgs", product["img"])
        image = Image.open(image_path)
        image = image.resize((100, 100))
        photo = ImageTk.PhotoImage(image)
        img_label.configure(image=photo)
        
        name_label.configure(text=product["name"])
        price_label.configure(text=f"{product['price']:,} VND")
        
        
    def update_footer(self):
        """Cập nhật tổng số sản phẩm và lưu vào file."""
        total_items = len(self.product_list)
        self.footer_label.configure(text=f"Tổng số sản phẩm: {total_items}")
    def get_path(self, *path_parts):
        return os.path.join(self.BASE_DIR, *path_parts)
