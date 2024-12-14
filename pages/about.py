import customtkinter as ctk

class About(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Heading
        heading_frame = ctk.CTkFrame(self, fg_color="transparent")
        heading_frame.pack(fill="x", pady=10)

        label = ctk.CTkLabel(
            heading_frame, 
            text="Giới thiệu", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label.pack(pady=10)

        # Separator
        separator_heading = ctk.CTkFrame(self, height=2, fg_color="gray")
        separator_heading.pack(fill="x", pady=10)

        # Content Frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, pady=10, padx=10)

        # Content Text
        about_text = (
            "Chào mừng bạn đến với ứng dụng quản lý hóa đơn! Với mục tiêu mang đến trải nghiệm "
            "quản lý hiệu quả, ứng dụng này được thiết kế nhằm đơn giản hóa quy trình theo dõi "
            "đơn hàng, quản lý sản phẩm, và tạo báo cáo chi tiết. Giao diện thân thiện và "
            "trực quan sẽ giúp bạn dễ dàng sử dụng, tiết kiệm thời gian, và tập trung vào những "
            "điều quan trọng nhất cho doanh nghiệp của bạn."
        )

        text_label = ctk.CTkLabel(
            content_frame, 
            text=about_text, 
            font=ctk.CTkFont(size=14), 
            wraplength=400, 
            justify="center"
        )
        text_label.pack(anchor="center", pady=10)

        # Team Information Header
        team_frame = ctk.CTkFrame(content_frame, fg_color="transparent", corner_radius=10)
        team_frame.pack(pady=10, padx=20)

        team_header = ctk.CTkLabel(
            team_frame, 
            text="Đội Ngũ Phát Triển:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            justify="center"
        )
        team_header.pack(anchor="center", pady=10)

        # Team Table
        table_frame = ctk.CTkFrame(team_frame, fg_color="transparent")
        table_frame.pack(pady=5, padx=10)

        # Table Header
        name_header = ctk.CTkLabel(
            table_frame, 
            text="Tên", 
            font=ctk.CTkFont(size=14, weight="bold"),
            width=200,
            anchor="w"
        )
        name_header.grid(row=0, column=0, padx=5, pady=5)

        role_header = ctk.CTkLabel(
            table_frame, 
            text="Chức vụ", 
            font=ctk.CTkFont(size=14, weight="bold"),
            width=200,
            anchor="w"
        )
        role_header.grid(row=0, column=1, padx=5, pady=5)

        # Table Content
        members = [
            ("Nguyễn Tùng Dương", "Leader & Full-stack Developer"),
            ("Đặng Công Minh", "Developer"),
            ("Nguyễn Khắc Bảo", "Developer")
        ]

        for i, (name, role) in enumerate(members):
            name_label = ctk.CTkLabel(
                table_frame, 
                text=name, 
                font=ctk.CTkFont(size=14),
                width=200,
                anchor="w"
            )
            name_label.grid(row=i+1, column=0, padx=5, pady=2)

            role_label = ctk.CTkLabel(
                table_frame, 
                text=role, 
                font=ctk.CTkFont(size=14),
                width=200,
                anchor="w"
            )
            role_label.grid(row=i+1, column=1, padx=5, pady=2)