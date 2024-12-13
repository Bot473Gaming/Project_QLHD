import customtkinter as ctk
class CreateOrder(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Đây là Trang tao hoa don hang 234567", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)
        