import customtkinter as ctk
class ManagerProducts(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Đây là Trang Sản Phẩm", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)