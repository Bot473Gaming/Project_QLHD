import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from datetime import datetime

class ReportDT(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.orders_file = "../Project_QLHD/assets/data/orders.json"
        
        self.data = self.load_data()
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year

        # Heading
        heading_frame = ctk.CTkFrame(self, fg_color="transparent")
        heading_frame.pack(fill="x", pady=10)

        label = ctk.CTkLabel(
            heading_frame, 
            text="Báo cáo doanh thu", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label.pack(pady=10)

        # Separator
        separator_heading = ctk.CTkFrame(self, height=2, fg_color="gray")
        separator_heading.pack(fill="x", pady=10)

        # Content Frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="x", pady=10)

        # Doanh thu năm
        self.annual_revenue_label = ctk.CTkLabel(
            content_frame, 
            text=f"Doanh thu năm: {self.get_annual_revenue():,} VND", 
            font=ctk.CTkFont(size=14)
        )
        self.annual_revenue_label.grid(row=0, column=0, padx=20, pady=5)

        # Doanh thu tháng
        self.monthly_revenue_label = ctk.CTkLabel(
            content_frame, 
            text=f"Doanh thu tháng: {self.get_monthly_revenue():,} VND", 
            font=ctk.CTkFont(size=14)
        )
        self.monthly_revenue_label.grid(row=0, column=1, padx=20, pady=5)

        # Doanh số tháng
        self.monthly_sales_label = ctk.CTkLabel(
            content_frame, 
            text=f"Doanh số tháng: {self.get_monthly_sales():,} sản phẩm", 
            font=ctk.CTkFont(size=14)
        )
        self.monthly_sales_label.grid(row=0, column=2, padx=20, pady=5)

        # Nút Cập nhật
        self.update_button = ctk.CTkButton(
            content_frame, text="Cập nhật", command=self.update_data
        )
        self.update_button.grid(row=0, column=3, padx=20, pady=5, sticky="e")

        # Separator
        separator_content = ctk.CTkFrame(self, height=2, fg_color="gray")
        separator_content.pack(fill="x", pady=10)

        # Chart
        self.chart_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_frame.pack(fill="both", expand=True, pady=10)
        self.create_chart()

    def load_data(self):
        """Tải dữ liệu từ file JSON."""
        try:
            with open(self.orders_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def update_data(self):
        """Cập nhật dữ liệu và làm mới biểu đồ."""
        # Tải lại dữ liệu từ file
        self.data = self.load_data()

        # Cập nhật các nhãn
        self.annual_revenue_label.configure(text=f"Doanh thu năm: {self.get_annual_revenue():,} VND")
        self.monthly_revenue_label.configure(text=f"Doanh thu tháng: {self.get_monthly_revenue():,} VND")
        self.monthly_sales_label.configure(text=f"Doanh số tháng: {self.get_monthly_sales():,} sản phẩm")

        # Vẽ lại biểu đồ
        self.create_chart()

    def get_annual_revenue(self):
        """Tính tổng doanh thu năm."""
        return sum(order["total_cost"] for order in self.data if self.is_in_year(order["date"]))

    def get_monthly_revenue(self):
        """Tính tổng doanh thu tháng hiện tại."""
        return sum(order["total_cost"] for order in self.data if self.is_in_month(order["date"]))

    def get_monthly_sales(self):
        """Tính tổng doanh số tháng hiện tại."""
        return sum(order["total_quantity"] for order in self.data if self.is_in_month(order["date"]))

    def is_in_month(self, date_str):
        """Kiểm tra đơn hàng có nằm trong tháng hiện tại không."""
        order_date = datetime.strptime(date_str, "%d-%m-%Y")
        return order_date.month == self.current_month and order_date.year == self.current_year

    def is_in_year(self, date_str):
        """Kiểm tra đơn hàng có nằm trong năm hiện tại không."""
        order_date = datetime.strptime(date_str, "%d-%m-%Y")
        return order_date.year == self.current_year

    def create_chart(self):
        """Tạo biểu đồ doanh thu theo tháng."""
        months = list(range(1, 13))
        revenues = [self.get_month_revenue(month) for month in months]

        figure = Figure(figsize=(6, 3), dpi=100)
        ax = figure.add_subplot(111)
        ax.plot(months, revenues, marker="o", linestyle="-", color="blue")
        ax.set_title("Doanh thu theo tháng", fontsize=14)
        ax.set_xlabel("Tháng")
        ax.set_ylabel("Doanh thu (VND)")
        ax.set_xticks(months)

        # Xóa biểu đồ cũ trước khi vẽ lại
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, self.chart_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def get_month_revenue(self, month):
        """Tính tổng doanh thu của một tháng cụ thể."""
        return sum(
            order["total_cost"]
            for order in self.data
            if datetime.strptime(order["date"], "%d-%m-%Y").month == month
        )
