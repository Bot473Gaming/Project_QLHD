import customtkinter as ctk
class ReportDT(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Đây là Trang Bao cao doanh thu", font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(pady=20)

