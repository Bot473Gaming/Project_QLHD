import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

class ManagerProducts(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Phần heading
        heading_frame = ctk.CTkFrame(self)
        heading_frame.pack(fill="x")  # Chiếm toàn bộ chiều ngang

        label = ctk.CTkLabel(
            heading_frame, 
            text="Trang Quản Lý Sản Phẩm", 
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

        # Phần bên trái - danh sách sản phẩm
        self.product_frame = ctk.CTkFrame(content_frame)
        self.product_frame.grid(row=0, column=0, sticky="nsew")

        # Phần bên phải - menu
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.grid(row=0, column=2, sticky="nsew")

        # Menu bên phải
        button1 = ctk.CTkButton(right_frame, text="Thêm sản phẩm", command=self.add_item)
        button1.pack(pady=10)

        # Nút chọn ảnh
        self.selected_image = None
        self.select_image_button = ctk.CTkButton(right_frame, text="Chọn ảnh", command=self.select_image)
        self.select_image_button.pack(pady=10)

        # Entry cho tên sản phẩm và giá
        self.product_name_entry = ctk.CTkEntry(right_frame, placeholder_text="Tên sản phẩm")
        self.product_name_entry.pack(pady=5)

        self.product_price_entry = ctk.CTkEntry(right_frame, placeholder_text="Giá sản phẩm")
        self.product_price_entry.pack(pady=5)

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

        # Khởi tạo danh sách sản phẩm
        self.product_list = []

    def select_image(self):
        # Mở hộp thoại để chọn ảnh
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.selected_image = file_path

    def add_item(self):
        # Lấy tên sản phẩm và giá từ entry
        product_name = self.product_name_entry.get()
        product_price = self.product_price_entry.get()

        if product_name and product_price and self.selected_image:
            # Tạo khung cho sản phẩm
            product_frame = ctk.CTkFrame(self.product_frame)
            product_frame.pack(fill="x", pady=5)

            # Hiển thị ảnh sản phẩm bằng CTkImage
            image = Image.open(self.selected_image)
            photo = ctk.CTkImage(image, size=(100, 100))  # Đặt kích thước mong muốn
            img_label = ctk.CTkLabel(product_frame, text="", image=photo, width=100, height=100, fg_color="transparent")
            img_label.image = photo  # Giữ tham chiếu ảnh để không bị xóa
            img_label.pack(side="left", padx=10)

            # Hiển thị tên sản phẩm
            name_label = ctk.CTkLabel(product_frame, text=product_name)
            name_label.pack(side="left", padx=10)

            # Hiển thị giá sản phẩm
            price_label = ctk.CTkLabel(product_frame, text=f"{product_price} VND")
            price_label.pack(side="left", padx=10)

            # Tạo nút xóa cho sản phẩm
            delete_button = ctk.CTkButton(product_frame, text="Xóa", command=lambda: self.remove_specific_item(product_frame))
            delete_button.pack(side="right", padx=10)

            # Thêm sản phẩm vào danh sách
            self.product_list.append({
                "name": product_name,
                "price": product_price,
                "image": self.selected_image,
                "frame": product_frame  # Lưu lại frame của sản phẩm
            })

            # Cập nhật footer
            self.update_footer()

            # Reset các trường nhập
            self.product_name_entry.delete(0, "end")
            self.product_price_entry.delete(0, "end")
            self.selected_image = None
        else:
            print("Vui lòng nhập đầy đủ thông tin sản phẩm và chọn ảnh.")

    def remove_specific_item(self, product_frame):
        # Xóa sản phẩm khỏi danh sách
        for product in self.product_list:
            if product["frame"] == product_frame:
                self.product_list.remove(product)
                break
        
        # Xóa frame của sản phẩm từ giao diện
        product_frame.destroy()

        # Cập nhật footer
        self.update_footer()

    def update_footer(self):
        # Cập nhật tổng số sản phẩm
        total_items = len(self.product_list)
        self.footer_label.configure(text=f"Tổng số sản phẩm: {total_items}")

if __name__ == "__main__":
    app = ctk.CTk()
    frame = ManagerProducts(app, None)
    frame.pack(fill="both", expand=True)
    app.mainloop()
