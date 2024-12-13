import customtkinter as ctk
from pages.createOrder import *
from pages.managerProducts import *
from pages.reportDT import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1200x1000")
        self.title("Quản lí đơn hàng")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Tạo menu bên trái
        self.menu_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, sticky="ns")
        self.menu_frame.grid_rowconfigure(4, weight=1)

        menu_label = ctk.CTkLabel(self.menu_frame, text="Menu", font=ctk.CTkFont(size=20, weight="bold"))
        menu_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        home_button = ctk.CTkButton(self.menu_frame, text="Tạo hoá đơn", command=lambda: self.show_frame(CreateOrder))
        home_button.grid(row=1, column=0, padx=20, pady=10)

        products_button = ctk.CTkButton(self.menu_frame, text="Sản Phẩm", command=lambda: self.show_frame(ManagerProducts))
        products_button.grid(row=2, column=0, padx=20, pady=10)

        customers_button = ctk.CTkButton(self.menu_frame, text="Báo cáo doanh thu", command=lambda: self.show_frame(ReportDT))
        customers_button.grid(row=3, column=0, padx=20, pady=10)


        # Tạo frame chứa nội dung
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)  # Flexible height
        self.content_frame.grid_columnconfigure(0, weight=1)  # Flexible width

        # Tạo viền bên trái cho menu
        self.left_border = ctk.CTkFrame(self, width=5, corner_radius=0, fg_color="gray")  # Viền bên trái của menu
        self.left_border.grid(row=0, column=1, sticky="nsw", padx=0, pady=0)  # Gắn viền vào lề trái của menu
        # Khởi tạo các trang
        self.frames = {}
        for F in (CreateOrder, ManagerProducts, ReportDT):
            frame = F(self.content_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(CreateOrder)  # Show the first page

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        # Auto-update when switching to ReportDT page
        if isinstance(frame, ReportDT):
            frame.update_data()
        elif isinstance(frame, CreateOrder):
            frame.update_search_results()
        elif isinstance(frame, ManagerProducts):
            frame.load_products()

if __name__ == "__main__":
    app = App()
    app.mainloop()
