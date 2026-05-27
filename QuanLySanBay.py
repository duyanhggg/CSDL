import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
import uuid
import random
import mysql.connector
import os

# ============================================================
# 🔒 CONFIG - Lấy từ environment hoặc default
# ============================================================
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "17052007")  # ⚠️ Nên lấy từ env variable
DB_NAME = os.getenv("DB_NAME", "baitaplondb")


def db():
    """Connect to MySQL database"""
    try:
        return mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
        )
    except Exception as e:
        messagebox.showerror("Lỗi Kết nối", f"Không kết nối được database:\n{str(e)}")
        return None


# Mapping tên tab → tên bảng SQL (fix lỗi tiếng Việt có dấu)
TABLE_MAP = {
    "Sân Bay": "san_bay",
    "Hãng Hàng Không": "hang_hang_khong",
    "Máy Bay": "may_bay",
    "Cửa Bay": "cua_bay",
    "Chuyến Bay": "chuyen_bay",
    "Lịch Chuyến Bay": "lich_chuyen_bay",
    "Hành Khách": "hanh_khach",
    "Nhân Viên": "nhan_vien",
    "Vé Máy Bay": "ve",
    "Phân Công CB": "phan_cong_chuyen_bay",
}


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Đăng Nhập")
        self.root.geometry("460x320")
        self.root.configure(bg="#f8fafc")
        self.root.resizable(False, False)

        tk.Label(
            self.root,
            text="✈️ AIRPORT MANAGEMENT SYSTEM",
            font=("Segoe UI", 16, "bold"),
            bg="#f8fafc",
            fg="#4f46e5",
        ).pack(pady=30)

        tk.Label(
            self.root,
            text="Username",
            bg="#f8fafc",
            fg="#334155",
            font=("Segoe UI", 11),
        ).pack(anchor="w", padx=80)
        self.un = tk.Entry(
            self.root,
            width=30,
            bg="white",
            fg="#1e2937",
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
        )
        self.un.pack(pady=5)
        self.un.insert(0, "admin")

        tk.Label(
            self.root,
            text="Password",
            bg="#f8fafc",
            fg="#334155",
            font=("Segoe UI", 11),
        ).pack(anchor="w", padx=80)
        self.pw = tk.Entry(
            self.root,
            width=30,
            bg="white",
            fg="#1e2937",
            font=("Segoe UI", 11),
            show="•",
            relief="solid",
            bd=1,
        )
        self.pw.pack(pady=5)
        self.pw.insert(0, "123456")

        tk.Button(
            self.root,
            text="ĐĂNG NHẬP",
            bg="#4f46e5",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=20,
            height=2,
            command=self.login,
        ).pack(pady=30)

        self.root.mainloop()

    def login(self):
        """Validate credentials and initialize main application UI."""
        username = self.un.get().strip()
        password = self.pw.get().strip()
        if not username or not password:
            messagebox.showwarning(
                "Thiếu thông tin", "Vui lòng nhập username và password!"
            )
            return

        # Simple local validation: default admin/123456 works; otherwise allow but warn
        if username != "admin" or password != "123456":
            if not messagebox.askyesno(
                "Xác nhận",
                "Thông tin đăng nhập không phải admin mặc định. Tiếp tục đăng nhập?",
            ):
                return

        # Clear login UI and initialize main application
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title("Airport Management System")
        self.root.geometry("1200x800")

        # Initialize state containers used by other methods
        self.trees = {}
        self.queries = {}
        self.search_vars = {}
        self._all_rows = {}

        # Create main notebook
        main_frame = tk.Frame(self.root, bg="#f1f5f9")
        main_frame.pack(fill="both", expand=True)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=6)

        # Build UI tabs
        try:
            self.create_dashboard()
            self.create_all_data_tabs()
            self.create_booking_tab()
            self.create_report_tab()
        except Exception as e:
            messagebox.showerror("Lỗi khởi tạo", str(e))
            return

        messagebox.showinfo("Đăng nhập", "Đăng nhập thành công!")

    def create_dashboard(self):
        dash = tk.Frame(self.notebook, bg="#f1f5f9")
        self.notebook.add(dash, text="🏠 Dashboard")

        tk.Label(
            dash,
            text="✈️ AIRPORT MANAGEMENT SYSTEM",
            font=("Segoe UI", 38, "bold"),
            bg="#f1f5f9",
            fg="#4f46e5",
        ).pack(pady=60)
        tk.Label(
            dash,
            text="Hệ thống quản lý sân bay – Sân bay Nội Bài",
            font=("Segoe UI", 16),
            bg="#f1f5f9",
            fg="#64748b",
        ).pack()

        stat_frame = tk.Frame(dash, bg="#f1f5f9")
        stat_frame.pack(pady=40)
        stats = [
            (
                "🛫 Chuyến Bay",
                "SELECT COUNT(*) FROM chuyen_bay WHERE TrangThai='Active'",
                "#4f46e5",
            ),
            (
                "📅 Lịch Bay",
                "SELECT COUNT(*) FROM lich_chuyen_bay WHERE TrangThai!='Cancelled'",
                "#0ea5e9",
            ),
            (
                "👤 Hành Khách",
                "SELECT COUNT(*) FROM hanh_khach WHERE TrangThai='Active'",
                "#10b981",
            ),
            (
                "🎟️ Vé Đã Bán",
                "SELECT COUNT(*) FROM ve WHERE TrangThaiVe='Booked' AND TrangThai='Active'",
                "#f59e0b",
            ),
            (
                "👨‍✈️ Nhân Viên",
                "SELECT COUNT(*) FROM nhan_vien WHERE TrangThai='Active'",
                "#8b5cf6",
            ),
        ]
        conn = db()
        for label, query, color in stats:
            val = "?"
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute(query)
                    val = cur.fetchone()[0]
                except Exception:
                    pass
            card = tk.Frame(stat_frame, bg=color, width=170, height=110, relief="flat")
            card.pack(side="left", padx=15)
            card.pack_propagate(False)
            tk.Label(
                card, text=str(val), font=("Segoe UI", 32, "bold"), bg=color, fg="white"
            ).pack(pady=12)
            tk.Label(
                card, text=label, font=("Segoe UI", 11), bg=color, fg="white"
            ).pack()
        if conn:
            conn.close()

    # ====================== TẤT CẢ TAB DỮ LIỆU (SỬA: Thêm TrangThai + Filter Active) ======================
    def create_all_data_tabs(self):
        tabs_config = [
            # (Tên hiển thị, [cột], query SQL, primary key)
            (
                "Sân Bay",
                ["MaSanBay", "TenSanBay", "ThanhPho", "QuocGia", "TrangThai"],
                "SELECT * FROM san_bay",
                "MaSanBay",
            ),
            (
                "Hãng Hàng Không",
                ["MaHang", "TenHang", "QuocGia", "SoDienThoai", "Email", "TrangThai"],
                "SELECT * FROM hang_hang_khong",
                "MaHang",
            ),
            (
                "Máy Bay",
                [
                    "MaMayBay",
                    "LoaiMayBay",
                    "SucChua",
                    "NamSanXuat",
                    "MaHang",
                    "TrangThai",
                ],
                "SELECT * FROM may_bay",
                "MaMayBay",
            ),
            (
                "Cửa Bay",
                ["MaCuaBay", "TenCuaBay", "MaSanBay", "TrangThai"],
                "SELECT * FROM cua_bay",
                "MaCuaBay",
            ),
            (
                "Chuyến Bay",
                [
                    "MaChuyenBay",
                    "MaHang",
                    "MaSanBayDi",
                    "MaSanBayDen",
                    "ThoiGianBayDuKien",
                    "TrangThai",
                ],
                "SELECT * FROM chuyen_bay",
                "MaChuyenBay",
            ),
            (
                "Lịch Chuyến Bay",
                [
                    "MaLichBay",
                    "MaChuyenBay",
                    "NgayBay",
                    "GioKhoiHanh",
                    "GioDenDuKien",
                    "MaMayBay",
                    "MaCuaBay",
                    "TrangThai",
                ],
                "SELECT * FROM lich_chuyen_bay",
                "MaLichBay",
            ),
            (
                "Hành Khách",
                [
                    "MaHanhKhach",
                    "HoTen",
                    "NgaySinh",
                    "GioiTinh",
                    "CCCD",
                    "SoDienThoai",
                    "Email",
                    "DiaChi",
                    "TrangThai",
                ],
                "SELECT * FROM hanh_khach WHERE TrangThai='Active'",
                "MaHanhKhach",
            ),
            (
                "Nhân Viên",
                [
                    "MaNhanVien",
                    "HoTen",
                    "NgaySinh",
                    "GioiTinh",
                    "SoDienThoai",
                    "Email",
                    "ChucVu",
                    "BangCap",
                    "MaHang",
                    "TrangThai",
                ],
                "SELECT * FROM nhan_vien WHERE TrangThai='Active'",
                "MaNhanVien",
            ),
            (
                "Vé Máy Bay",
                [
                    "MaVe",
                    "MaHanhKhach",
                    "MaLichBay",
                    "SoGhe",
                    "GiaVe",
                    "TrangThaiVe",
                    "TrangThai",
                ],
                "SELECT * FROM ve WHERE TrangThai='Active'",
                "MaVe",
            ),
            (
                "Phân Công CB",
                ["MaPhanCong", "MaNhanVien", "MaLichBay", "VaiTro", "TrangThai"],
                "SELECT * FROM phan_cong_chuyen_bay WHERE TrangThai='Active'",
                "MaPhanCong",
            ),
        ]

        for name, cols, query, pk in tabs_config:
            tab = tk.Frame(self.notebook, bg="#f1f5f9")
            self.notebook.add(tab, text=name)
            self.queries[name] = query

            # Thanh tìm kiếm
            sf = tk.Frame(tab, bg="#f1f5f9")
            sf.pack(fill="x", padx=20, pady=12)
            tk.Label(
                sf,
                text="🔍 Tìm kiếm:",
                bg="#f1f5f9",
                fg="#334155",
                font=("Segoe UI", 11, "bold"),
            ).pack(side="left")
            search_var = tk.StringVar()
            self.search_vars[name] = search_var
            entry = tk.Entry(
                sf,
                textvariable=search_var,
                width=60,
                font=("Segoe UI", 11),
                bg="white",
                fg="#1e2937",
                relief="solid",
                bd=1,
            )
            entry.pack(side="left", padx=10)
            entry.bind("<KeyRelease>", lambda e, n=name: self.filter_tree(n))

            container = tk.Frame(tab, bg="white")
            container.pack(fill="both", expand=True, padx=20, pady=5)

            tree = ttk.Treeview(container, columns=cols, show="headings", height=20)
            for col in cols:
                tree.heading(col, text=col)
                # Dynamic width
                widths = {
                    "Email": 200,
                    "DiaChi": 250,
                    "TenSanBay": 200,
                    "LoaiMayBay": 200,
                    "TenHang": 200,
                    "HoTen": 200,
                }
                tree.column(col, width=widths.get(col, 120), anchor="w")

            vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
            hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
            tree.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            hsb.grid(row=1, column=0, sticky="ew")
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            self.trees[name] = (tree, pk)
            self.load_data(tree, query, name)

            # Nút thao tác
            btnf = tk.Frame(tab, bg="#f1f5f9")
            btnf.pack(pady=12)
            tk.Button(
                btnf,
                text="🔄 Làm Mới",
                bg="#4f46e5",
                fg="white",
                width=14,
                command=lambda n=name: self.refresh_tab(n),
            ).pack(side="left", padx=5)
            tk.Button(
                btnf,
                text="➕ Thêm",
                bg="#10b981",
                fg="white",
                width=12,
                command=lambda t=tree, n=name: self.add_record(t, n),
            ).pack(side="left", padx=5)
            tk.Button(
                btnf,
                text="✏️ Sửa",
                bg="#eab308",
                fg="black",
                width=12,
                command=lambda t=tree, n=name: self.edit_record(t, n),
            ).pack(side="left", padx=5)
            tk.Button(
                btnf,
                text="⛔ Inactive",
                bg="#ef4444",
                fg="white",
                width=12,
                command=lambda t=tree, n=name: self.soft_delete_record(t, n),
            ).pack(side="left", padx=5)

    def load_data(self, tree, query, tab_name=None):
        tree.delete(*tree.get_children())
        conn = db()
        if not conn:
            return
        rows = []
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
                rows.append(row)
        finally:
            conn.close()
        if tab_name:
            self._all_rows[tab_name] = rows

    def refresh_tab(self, tab_name):
        self.search_vars[tab_name].set("")
        tree = self.trees[tab_name][0]
        query = self.queries[tab_name]
        self.load_data(tree, query, tab_name)

    def filter_tree(self, tab_name):
        tree = self.trees[tab_name][0]
        search_text = self.search_vars[tab_name].get().lower().strip()
        tree.delete(*tree.get_children())
        all_rows = self._all_rows.get(tab_name, [])
        for row in all_rows:
            if search_text in " ".join(str(v).lower() for v in row):
                tree.insert("", tk.END, values=row)

    # ====================== FORM THÊM MỚI (SỬA: Default TrangThai) ======================
    def add_record(self, tree, tab_name):
        cols = tree["columns"]
        pk_col = self.trees[tab_name][1]
        tbl = TABLE_MAP.get(tab_name, tab_name)

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Thêm {tab_name}")
        dialog.geometry("700x620")
        dialog.configure(bg="#f8fafc")
        dialog.grab_set()

        tk.Label(
            dialog,
            text=f"THÊM {tab_name.upper()}",
            font=("Segoe UI", 14, "bold"),
            bg="#f8fafc",
            fg="#4f46e5",
        ).grid(row=0, column=0, columnspan=2, pady=20)

        entries = {}
        for i, col in enumerate(cols):
            tk.Label(
                dialog,
                text=col + ":",
                bg="#f8fafc",
                fg="#334155",
                font=("Segoe UI", 11, "bold"),
            ).grid(row=i + 1, column=0, sticky="w", padx=20, pady=8)
            e = tk.Entry(
                dialog,
                width=55,
                font=("Segoe UI", 11),
                bg="white",
                relief="solid",
                bd=1,
            )
            e.grid(row=i + 1, column=1, padx=20, pady=8)

            # Default TrangThai = 'Active'
            if col == "TrangThai":
                e.insert(0, "Active")

            entries[col] = e

        def save():
            # Build list of (col, value) and skip empty values so auto-increment PKs can be omitted
            col_values = [(col, entries[col].get().strip()) for col in cols]

            # If user provided PK explicitly, include it; otherwise omit PK column to allow AUTO_INCREMENT
            insert_cols = [c for c, v in col_values if not (c == pk_col and v == "")]
            insert_vals = [v for c, v in col_values if not (c == pk_col and v == "")]

            if not insert_cols:
                messagebox.showwarning("Lỗi", "Vui lòng nhập dữ liệu!", parent=dialog)
                return

            conn = db()
            if not conn:
                return
            try:
                cursor = conn.cursor()
                placeholders = ", ".join(["%s"] * len(insert_cols))
                col_names = ", ".join([f"`{c}`" for c in insert_cols])
                sql = f"INSERT INTO `{tbl}` ({col_names}) VALUES ({placeholders})"
                cursor.execute(sql, insert_vals)
                conn.commit()
                messagebox.showinfo(
                    "Thành công", "Thêm dữ liệu thành công!", parent=dialog
                )
                dialog.destroy()
                self.refresh_tab(tab_name)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e), parent=dialog)
            finally:
                conn.close()

        tk.Button(
            dialog,
            text="➕ THÊM MỚI",
            bg="#10b981",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=20,
            command=save,
        ).grid(row=len(cols) + 2, column=1, pady=25)

    # ====================== FORM SỬA (FIX: Không update PK) ======================
    def edit_record(self, tree, tab_name):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn dòng cần sửa!")
            return

        values = tree.item(selected[0])["values"]
        cols = tree["columns"]
        pk_col = self.trees[tab_name][1]
        pk_value = values[0]
        tbl = TABLE_MAP.get(tab_name, tab_name)

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Sửa {tab_name}")
        dialog.geometry("700x620")
        dialog.configure(bg="#f8fafc")
        dialog.grab_set()

        tk.Label(
            dialog,
            text=f"SỬA {tab_name.upper()}",
            font=("Segoe UI", 14, "bold"),
            bg="#f8fafc",
            fg="#eab308",
        ).grid(row=0, column=0, columnspan=2, pady=20)

        entries = {}
        for i, col in enumerate(cols):
            tk.Label(
                dialog,
                text=col + ":",
                bg="#f8fafc",
                fg="#334155",
                font=("Segoe UI", 11, "bold"),
            ).grid(row=i + 1, column=0, sticky="w", padx=20, pady=8)
            e = tk.Entry(
                dialog,
                width=55,
                font=("Segoe UI", 11),
                bg="white",
                relief="solid",
                bd=1,
            )
            e.grid(row=i + 1, column=1, padx=20, pady=8)
            e.insert(0, values[i])
            # Khóa chính không cho sửa
            if col == pk_col:
                e.configure(state="readonly", bg="#e2e8f0")
            entries[col] = e

        def save():
            # FIX: Chỉ cập nhật cột không phải PK
            update_cols = [c for c in cols if c != pk_col]
            set_clause = ", ".join([f"`{col}` = %s" for col in update_cols])
            update_vals = [entries[c].get().strip() for c in update_cols]

            conn = db()
            if not conn:
                return
            try:
                cursor = conn.cursor()
                sql = f"UPDATE `{tbl}` SET {set_clause} WHERE `{pk_col}` = %s"
                cursor.execute(sql, (*update_vals, pk_value))
                conn.commit()
                messagebox.showinfo(
                    "Thành công", "Cập nhật dữ liệu thành công!", parent=dialog
                )
                dialog.destroy()
                self.refresh_tab(tab_name)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e), parent=dialog)
            finally:
                conn.close()

        tk.Button(
            dialog,
            text="💾 LƯU THAY ĐỔI",
            bg="#10b981",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=20,
            command=save,
        ).grid(row=len(cols) + 2, column=1, pady=25)

    # ====================== SOFT DELETE (FIX: Thay UPDATE thay DELETE) ======================
    def soft_delete_record(self, tree, tab_name):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn dòng cần vô hiệu hóa!")
            return

        values = tree.item(selected[0])["values"]
        pk_col = self.trees[tab_name][1]
        pk_value = values[0]
        tbl = TABLE_MAP.get(tab_name, tab_name)

        confirm = messagebox.askyesno(
            "Xác nhận vô hiệu hóa",
            f"Bạn có chắc muốn vô hiệu hóa [{pk_col} = {pk_value}]?\n(Dữ liệu sẽ được giữ, chỉ đánh dấu là Inactive)",
        )
        if not confirm:
            return

        conn = db()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            # SOFT DELETE: Chỉ cập nhật TrangThai thành Inactive
            sql = f"UPDATE `{tbl}` SET `TrangThai` = 'Inactive' WHERE `{pk_col}` = %s"
            cursor.execute(sql, (pk_value,))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã vô hiệu hóa {pk_value} thành công!")
            self.refresh_tab(tab_name)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể vô hiệu hóa:\n{str(e)}")
        finally:
            conn.close()

    # ====================== FORM ĐẶT VÉ (SỬA + MỞ RỘNG VALIDATION) ======================
    def create_booking_tab(self):
        tab = tk.Frame(self.notebook, bg="#eef4fb")
        self.notebook.add(tab, text="🎟️ Đặt Vé")

        self.booking_entries = {}

        hero = tk.Frame(tab, bg="#0a2a66", height=150)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        hero_left = tk.Frame(hero, bg="#0a2a66")
        hero_left.pack(side="left", fill="both", expand=True, padx=28, pady=20)
        tk.Label(
            hero_left,
            text="ĐẶT VÉ",
            bg="#0a2a66",
            fg="#f4c542",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w")
        tk.Label(
            hero_left,
            text="Đặt vé máy bay",
            bg="#0a2a66",
            fg="white",
            font=("Segoe UI", 28, "bold"),
        ).pack(anchor="w", pady=(6, 0))
        tk.Label(
            hero_left,
            text="Chọn lịch bay, hạng ghế và nhận giá tự động ngay trên màn hình.",
            bg="#0a2a66",
            fg="#dbeafe",
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(8, 0))

        hero_right = tk.Frame(hero, bg="#123a86", width=260)
        hero_right.pack(side="right", fill="y")
        hero_right.pack_propagate(False)
        tk.Label(
            hero_right,
            text="Tổng quan",
            bg="#123a86",
            fg="#f4c542",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(16, 6))
        self.hero_price_label = tk.Label(
            hero_right,
            text="0 VND",
            bg="#123a86",
            fg="white",
            font=("Segoe UI", 26, "bold"),
        )
        self.hero_price_label.pack(anchor="w", padx=16)
        tk.Label(
            hero_right,
            text="Mã vé và mã khách sẽ được tự động sinh nếu để trống.",
            bg="#123a86",
            fg="#dbeafe",
            justify="left",
            wraplength=220,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=16, pady=(8, 0))

        body = tk.Frame(tab, bg="#eef4fb", padx=22, pady=18)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=3)
        body.grid_columnconfigure(1, weight=2)
        body.grid_rowconfigure(0, weight=1)

        booking_card = tk.Frame(
            body, bg="white", bd=0, highlightthickness=1, highlightbackground="#dbe7f5"
        )
        booking_card.grid(row=0, column=0, sticky="nsew", padx=(0, 14), pady=6)
        booking_card.grid_columnconfigure(0, weight=1)
        booking_card.grid_columnconfigure(1, weight=1)

        tk.Label(
            booking_card,
            text="Thông tin đặt vé",
            bg="white",
            fg="#0a2a66",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=22, pady=(18, 6))
        tk.Label(
            booking_card,
            text="Điền theo thứ tự từ trái sang phải. CCCD sẽ dùng để tra hoặc tạo khách mới.",
            bg="white",
            fg="#64748b",
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=22, pady=(0, 12))

        def add_field(parent, row, label, entry, span=1, pady=8):
            tk.Label(
                parent,
                text=label,
                bg="white",
                fg="#334155",
                font=("Segoe UI", 11, "bold"),
            ).grid(row=row, column=0, sticky="w", padx=22, pady=pady)
            entry.grid(
                row=row, column=1, columnspan=span, sticky="ew", padx=22, pady=pady
            )

        mv_e = tk.Entry(
            booking_card, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1
        )
        self.booking_entries["Mã Vé"] = mv_e
        add_field(booking_card, 2, "Mã Vé", mv_e)
        tk.Label(
            booking_card,
            text="Để trống để tự sinh VEXXXXX",
            bg="white",
            fg="#94a3b8",
            font=("Segoe UI", 9),
        ).grid(row=3, column=1, sticky="w", padx=22, pady=(0, 4))

        name_e = tk.Entry(
            booking_card, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1
        )
        self.booking_entries["Họ Tên"] = name_e
        add_field(booking_card, 4, "Họ Tên", name_e)

        cccd_e = tk.Entry(
            booking_card, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1
        )
        self.booking_entries["CCCD"] = cccd_e
        add_field(booking_card, 5, "CCCD", cccd_e)

        ngay_frame = tk.Frame(booking_card, bg="white")
        ngay_entry = tk.Entry(
            ngay_frame,
            width=20,
            font=("Segoe UI", 11),
            bg="#f8fafc",
            relief="solid",
            bd=1,
        )
        ngay_entry.pack(side="left", fill="x", expand=True)
        tk.Button(
            ngay_frame,
            text="Tìm lịch còn chỗ",
            bg="#0a2a66",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            command=lambda: self.populate_schedules_for_date(ngay_entry.get()),
        ).pack(side="left", padx=10)
        self.booking_entries["Ngày Bay"] = ngay_entry
        tk.Label(
            booking_card,
            text="Ngày Bay",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=6, column=0, sticky="w", padx=22, pady=8)
        ngay_frame.grid(row=6, column=1, sticky="ew", padx=22, pady=8)
        booking_card.grid_columnconfigure(1, weight=1)

        lich_frame = tk.Frame(booking_card, bg="white")
        self.lich_combobox = ttk.Combobox(
            lich_frame, font=("Segoe UI", 11), state="readonly"
        )
        self.lich_combobox.pack(side="left", fill="x", expand=True)
        self.lich_combobox.bind(
            "<<ComboboxSelected>>", lambda e: self.calculate_price()
        )
        tk.Button(
            lich_frame,
            text="Chọn",
            bg="#f4c542",
            fg="#0a2a66",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            command=self.calculate_price,
        ).pack(side="left", padx=10)
        self.booking_entries["Mã Lịch Bay"] = self.lich_combobox
        tk.Label(
            booking_card,
            text="Mã Lịch Bay",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=7, column=0, sticky="w", padx=22, pady=8)
        lich_frame.grid(row=7, column=1, sticky="ew", padx=22, pady=8)

        seat_e = tk.Entry(
            booking_card, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1
        )
        self.booking_entries["Số Ghế"] = seat_e
        seat_e.bind("<KeyRelease>", lambda e: self.calculate_price())
        add_field(booking_card, 8, "Số Ghế", seat_e)
        tk.Label(
            booking_card,
            text="Ví dụ: 12A, 5B",
            bg="white",
            fg="#94a3b8",
            font=("Segoe UI", 9),
        ).grid(row=9, column=1, sticky="w", padx=22, pady=(0, 4))

        tk.Label(
            booking_card,
            text="Hạng vé",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=10, column=0, sticky="w", padx=22, pady=8)
        self.class_var = tk.StringVar(value="Economy")
        class_frame = tk.Frame(booking_card, bg="white")
        class_frame.grid(row=10, column=1, sticky="w", padx=22, pady=8)
        for c in ["Economy", "Business", "First Class"]:
            tk.Radiobutton(
                class_frame,
                text=c,
                variable=self.class_var,
                value=c,
                bg="white",
                fg="#0f172a",
                selectcolor="#dbeafe",
                activebackground="white",
                font=("Segoe UI", 11),
                command=self.calculate_price,
            ).pack(side="left", padx=(0, 14))

        tk.Label(
            booking_card,
            text="Giá vé",
            bg="white",
            fg="#334155",
            font=("Segoe UI", 11, "bold"),
        ).grid(row=11, column=0, sticky="w", padx=22, pady=8)
        self.price_entry = tk.Entry(
            booking_card,
            font=("Segoe UI", 11, "bold"),
            bg="#f8fafc",
            fg="#0a2a66",
            relief="solid",
            bd=1,
            state="readonly",
        )
        self.price_entry.grid(row=11, column=1, sticky="ew", padx=22, pady=8)

        action_row = tk.Frame(booking_card, bg="white")
        action_row.grid(
            row=12, column=0, columnspan=2, sticky="ew", padx=22, pady=(12, 18)
        )
        tk.Button(
            action_row,
            text="Đặt vé ngay",
            bg="#0a2a66",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=18,
            height=2,
            relief="flat",
            command=self.book_ticket,
        ).pack(side="left")
        tk.Label(
            action_row,
            text="Trạng thái vé mặc định: Booked",
            bg="white",
            fg="#64748b",
            font=("Segoe UI", 10, "italic"),
        ).pack(side="left", padx=16)

        side = tk.Frame(body, bg="#eef4fb")
        side.grid(row=0, column=1, sticky="nsew", pady=6)
        side.grid_columnconfigure(0, weight=1)

        availability_card = tk.Frame(
            side, bg="white", highlightthickness=1, highlightbackground="#dbe7f5"
        )
        availability_card.pack(fill="both", expand=True)
        tk.Label(
            availability_card,
            text="Ngày bay còn chỗ",
            bg="white",
            fg="#0a2a66",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 4))
        tk.Label(
            availability_card,
            text="Chọn một dòng để đồng bộ mã lịch bay và cập nhật giá.",
            bg="white",
            fg="#64748b",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=18, pady=(0, 12))

        table_frame = tk.Frame(availability_card, bg="white")
        table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        schedule_cols = (
            "NgayBay",
            "MaLichBay",
            "MaChuyenBay",
            "GioKhoiHanh",
            "SoDaDat",
            "ConCho",
        )
        self.schedule_tree = ttk.Treeview(
            table_frame, columns=schedule_cols, show="headings", height=11
        )
        for col, width in [
            ("NgayBay", 108),
            ("MaLichBay", 110),
            ("MaChuyenBay", 116),
            ("GioKhoiHanh", 108),
            ("SoDaDat", 80),
            ("ConCho", 80),
        ]:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=width, anchor="w")
        schedule_vsb = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.schedule_tree.yview
        )
        self.schedule_tree.configure(yscrollcommand=schedule_vsb.set)
        self.schedule_tree.grid(row=0, column=0, sticky="nsew")
        schedule_vsb.grid(row=0, column=1, sticky="ns")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        self.schedule_tree.bind("<<TreeviewSelect>>", self._on_schedule_selected)

    def populate_schedules_for_date(self, date_str: str):
        """Query lich_chuyen_bay for given date and populate table + combobox with readable options."""
        date_str = date_str.strip()
        if not date_str:
            messagebox.showwarning(
                "Thiếu thông tin", "Vui lòng nhập Ngày Bay (YYYY-MM-DD)!"
            )
            return
        conn = db()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT l.MaLichBay, l.MaChuyenBay, l.GioKhoiHanh, l.MaMayBay, m.SucChua
                FROM lich_chuyen_bay l
                JOIN may_bay m ON l.MaMayBay = m.MaMayBay
                WHERE l.NgayBay = %s AND l.TrangThai != 'Cancelled'
                ORDER BY l.GioKhoiHanh
                """,
                (date_str,),
            )
            rows = cursor.fetchall()
            if not rows:
                messagebox.showinfo(
                    "Kết quả", f"Hiện chưa có lịch ngày {date_str}"
                )
                self.lich_combobox["values"] = []
                if hasattr(self, "schedule_tree"):
                    self.schedule_tree.delete(*self.schedule_tree.get_children())
                return
            self._schedule_map = {}
            self._schedule_rows = {}
            display = []
            if hasattr(self, "schedule_tree"):
                self.schedule_tree.delete(*self.schedule_tree.get_children())
            for ma_lich, ma_chuyen_bay, gio_khoi_hanh, ma_may_bay, suc_chua in rows:
                cursor.execute(
                    "SELECT COUNT(*) FROM ve WHERE MaLichBay = %s AND TrangThaiVe != 'Cancelled' AND TrangThai = 'Active'",
                    (ma_lich,),
                )
                sold = cursor.fetchone()[0]
                con_cho = max(int(suc_chua or 0) - int(sold), 0)
                display_text = f"{ma_lich} | {ma_chuyen_bay} | {gio_khoi_hanh}"
                display.append(display_text)
                self._schedule_map[display_text] = ma_lich
                self._schedule_rows[ma_lich] = {
                    "NgayBay": date_str,
                    "MaLichBay": ma_lich,
                    "MaChuyenBay": ma_chuyen_bay,
                    "GioKhoiHanh": gio_khoi_hanh,
                    "MaMayBay": ma_may_bay,
                    "SucChua": int(suc_chua or 0),
                    "SoDaDat": int(sold),
                    "ConCho": con_cho,
                }
                if hasattr(self, "schedule_tree"):
                    self.schedule_tree.insert(
                        "",
                        tk.END,
                        iid=ma_lich,
                        values=(
                            date_str,
                            ma_lich,
                            ma_chuyen_bay,
                            gio_khoi_hanh,
                            sold,
                            con_cho,
                        ),
                    )
            self.lich_combobox["values"] = display
            if display:
                self.lich_combobox.set(display[0])
                self.calculate_price()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def _on_schedule_selected(self, _event=None):
        selected = self.schedule_tree.selection()
        if not selected:
            return
        ma_lich = selected[0]
        display = None
        for text, value in getattr(self, "_schedule_map", {}).items():
            if value == ma_lich:
                display = text
                break
        if display:
            self.lich_combobox.set(display)
            self.calculate_price()

    def _compute_price_for_schedule(self, ma_lich: str, seat_class: str):
        """Compute dynamic price based on days until flight and seat class."""
        base = 1_800_000
        multipliers = {"Economy": 1.0, "Business": 2.3, "First Class": 3.8}
        if not ma_lich:
            return int(base * multipliers.get(seat_class, 1.0))
        conn = db()
        if not conn:
            return int(base * multipliers.get(seat_class, 1.0))
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT NgayBay FROM lich_chuyen_bay WHERE MaLichBay = %s", (ma_lich,)
            )
            r = cursor.fetchone()
            if not r:
                days = 0
            else:
                ngay = r[0]
                if isinstance(ngay, str):
                    ngay = datetime.strptime(ngay, "%Y-%m-%d").date()
                days = (ngay - datetime.now().date()).days
            # discounts / surcharges
            if days >= 30:
                time_factor = 0.8
            elif days < 7:
                time_factor = 1.2
            else:
                time_factor = 1.0
            price = int(base * multipliers.get(seat_class, 1.0) * time_factor)
            return price
        finally:
            conn.close()

    def _prompt_create_passenger(self, name: str, default_cccd: str = ""):
        """Open dialog to collect passenger info and create hanh_khach record. Returns MaHanhKhach."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Tạo Hành Khách Mới")
        dialog.geometry("520x420")
        dialog.grab_set()

        tk.Label(
            dialog,
            text="TẠO HÀNH KHÁCH MỚI",
            font=("Segoe UI", 12, "bold"),
            bg="#f8fafc",
        ).pack(pady=10)
        frame = tk.Frame(dialog)
        frame.pack(padx=18, pady=6)

        labels = [
            "Họ Tên",
            "CCCD",
            "Ngày Sinh (YYYY-MM-DD)",
            "Giới Tính (Nam/Nu/Khac)",
            "Số Điện Thoại",
            "Email",
            "Địa Chỉ",
        ]
        entries = {}
        defaults = [name, default_cccd, "", "Nam", "", "", ""]
        for i, lab in enumerate(labels):
            tk.Label(frame, text=lab + ":", anchor="w", width=20).grid(
                row=i, column=0, sticky="w", pady=6
            )
            e = tk.Entry(frame, width=36)
            e.grid(row=i, column=1, pady=6)
            e.insert(0, defaults[i])
            entries[lab] = e

        result = {"ma": None}

        def create_and_close():
            ho_ten = entries["Họ Tên"].get().strip()
            cccd = entries["CCCD"].get().strip()
            if not ho_ten or not cccd:
                messagebox.showwarning(
                    "Thiếu thông tin", "Vui lòng nhập Họ Tên và CCCD!"
                )
                return
            ma = self._generate_code("HK", 5, "hanh_khach", "MaHanhKhach")
            ngay_sinh = entries["Ngày Sinh (YYYY-MM-DD)"].get().strip() or None
            gioi_tinh = entries["Giới Tính (Nam/Nu/Khac)"].get().strip() or None
            sdt = entries["Số Điện Thoại"].get().strip() or None
            email = entries["Email"].get().strip() or None
            diachi = entries["Địa Chỉ"].get().strip() or None

            conn = db()
            if not conn:
                return
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO hanh_khach (MaHanhKhach, HoTen, NgaySinh, GioiTinh, CCCD, SoDienThoai, Email, DiaChi, TrangThai) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'Active')"
                cursor.execute(
                    sql, (ma, ho_ten, ngay_sinh, gioi_tinh, cccd, sdt, email, diachi)
                )
                conn.commit()
                result["ma"] = ma
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Lỗi tạo hành khách", str(e))
            finally:
                conn.close()

        tk.Button(
            dialog, text="Tạo", bg="#10b981", fg="white", command=create_and_close
        ).pack(pady=12)
        dialog.wait_window()
        return result["ma"]

    def _generate_code(self, prefix: str, length: int, table: str, column: str):
        """Generate a unique code like VEXXXXX or HKXXXXX."""
        conn = db()
        if not conn:
            raise Exception("Không kết nối được database!")
        try:
            cursor = conn.cursor()
            for _ in range(200):
                suffix = str(random.randint(0, 10**length - 1)).zfill(length)
                code = f"{prefix}{suffix}"
                cursor.execute(
                    f"SELECT 1 FROM `{table}` WHERE `{column}` = %s", (code,)
                )
                if not cursor.fetchone():
                    return code
            raise Exception(f"Không thể tạo mã {prefix} duy nhất!")
        finally:
            conn.close()

    def calculate_price(self):
        # Calculate using selected schedule if available
        try:
            selected = None
            if hasattr(self, "lich_combobox"):
                sel = self.lich_combobox.get().strip()
                # map to MaLichBay if we populated via populate_schedules_for_date
                if hasattr(self, "_schedule_map") and sel in getattr(
                    self, "_schedule_map"
                ):
                    selected = getattr(self, "_schedule_map")[sel]
                else:
                    # if sel looks like an ID
                    selected = sel.split("|")[0].strip() if sel else None
            if selected:
                price = self._compute_price_for_schedule(selected, self.class_var.get())
            else:
                base = 1_800_000
                multipliers = {"Economy": 1.0, "Business": 2.3, "First Class": 3.8}
                price = int(base * multipliers.get(self.class_var.get(), 1.0))
        except Exception:
            base = 1_800_000
            multipliers = {"Economy": 1.0, "Business": 2.3, "First Class": 3.8}
            price = int(base * multipliers.get(self.class_var.get(), 1.0))
        self.price_entry.configure(state="normal")
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, f"{price:,}")
        self.price_entry.configure(state="readonly")
        # Update hero price summary if present
        try:
            if hasattr(self, "hero_price_label") and self.hero_price_label:
                self.hero_price_label.config(text=f"{int(price):,} VND")
        except Exception:
            pass

    def book_ticket(self):
        try:
            data = {k: v.get().strip() for k, v in self.booking_entries.items()}
            if not data.get("Họ Tên"):
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Họ Tên!")
                return
            if not data.get("CCCD"):
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập CCCD!")
                return
            if not data.get("Mã Lịch Bay"):
                messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn Mã Lịch Bay!")
                return
            if not data.get("Số Ghế"):
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Số Ghế!")
                return

            seat = data["Số Ghế"].upper()
            if not re.match(r"^[0-9]{1,2}[A-Z]$", seat):
                messagebox.showwarning(
                    "Số ghế không hợp lệ", "Định dạng ghế phải như 12A hoặc 5B."
                )
                return

            ma_lich = self._schedule_map.get(
                data["Mã Lịch Bay"], data["Mã Lịch Bay"].split("|")[0].strip()
            )
            if not ma_lich:
                messagebox.showwarning(
                    "Thiếu thông tin", "Không xác định được mã lịch bay!"
                )
                return

            price = self._compute_price_for_schedule(ma_lich, self.class_var.get())

            conn = db()
            if not conn:
                return
            cursor = conn.cursor()

            # Lookup passenger by CCCD; create if not found
            cursor.execute(
                "SELECT MaHanhKhach, HoTen FROM hanh_khach WHERE CCCD = %s AND TrangThai='Active'",
                (data["CCCD"],),
            )
            passenger = cursor.fetchone()
            if passenger:
                ma_hk = passenger[0]
                if not data["Họ Tên"]:
                    data["Họ Tên"] = passenger[1] or ""
            else:
                if not data["Họ Tên"]:
                    messagebox.showwarning(
                        "Thiếu thông tin",
                        "CCCD chưa tồn tại, vui lòng nhập Họ Tên để tạo hành khách mới!",
                    )
                    return
                extra_ma_hk = self._prompt_create_passenger(
                    data["Họ Tên"], data["CCCD"]
                )
                if not extra_ma_hk:
                    raise Exception("Cần tạo hành khách trước khi đặt vé.")
                ma_hk = extra_ma_hk

            # Check lịch bay and get MaMayBay and NgayBay
            cursor.execute(
                "SELECT MaMayBay, NgayBay, TrangThai FROM lich_chuyen_bay WHERE MaLichBay = %s",
                (ma_lich,),
            )
            lb = cursor.fetchone()
            if not lb:
                raise Exception("Mã lịch bay không tồn tại!")
            ma_may_bay, ngay_bay, trang_thai_lich = lb[0], lb[1], lb[2]
            today = datetime.now().date()
            if trang_thai_lich == "Cancelled":
                raise Exception("Không thể đặt vé cho lịch bay đã bị hủy!")
            if isinstance(ngay_bay, str):
                ngay_bay = datetime.strptime(ngay_bay, "%Y-%m-%d").date()
            if ngay_bay < today:
                raise Exception(
                    "Không thể đặt vé cho chuyến bay đã khởi hành (ngày bay đã qua)!"
                )

            if hasattr(self, "_schedule_rows") and ma_lich in self._schedule_rows:
                if int(self._schedule_rows[ma_lich]["ConCho"]) <= 0:
                    raise Exception("Chuyến bay này đã hết chỗ!")

            # Generate MaVe in the requested format VEXXXXX
            ma_ve = data.get("Mã Vé") or self._generate_code("VE", 5, "ve", "MaVe")
            if not re.match(r"^VE\d{5}$", ma_ve):
                raise Exception("Mã vé phải có dạng VEXXXXX (VD: VE00001).")

            # Check trùng mã vé
            cursor.execute("SELECT 1 FROM ve WHERE MaVe = %s", (ma_ve,))
            if cursor.fetchone():
                raise Exception("Mã vé đã tồn tại, vui lòng dùng mã khác!")

            # Check ghế trùng trong lịch bay
            cursor.execute(
                """
                SELECT COUNT(*) FROM ve
                WHERE MaLichBay = %s AND SoGhe = %s AND TrangThaiVe != 'Cancelled' AND TrangThai = 'Active'
            """,
                (ma_lich, seat),
            )
            if cursor.fetchone()[0] > 0:
                raise Exception(f"Ghế {seat} đã được bán cho chuyến bay này!")

            # Transactional seat & capacity check with row lock
            try:
                conn.start_transaction()
                # Lock aircraft row to avoid race conditions
                cursor.execute(
                    "SELECT SucChua FROM may_bay WHERE MaMayBay = %s FOR UPDATE",
                    (ma_may_bay,),
                )
                mb = cursor.fetchone()
                suc_chua = int(mb[0]) if mb and mb[0] else None

                # Re-check seat availability inside transaction
                cursor.execute(
                    "SELECT COUNT(*) FROM ve WHERE MaLichBay = %s AND SoGhe = %s AND TrangThaiVe != 'Cancelled' AND TrangThai = 'Active'",
                    (ma_lich, seat),
                )
                if cursor.fetchone()[0] > 0:
                    raise Exception(f"Ghế {seat} đã được bán cho chuyến bay này!")

                # Re-count sold
                cursor.execute(
                    "SELECT COUNT(*) FROM ve WHERE MaLichBay = %s AND TrangThaiVe != 'Cancelled' AND TrangThai = 'Active'",
                    (ma_lich,),
                )
                sold = cursor.fetchone()[0]
                if suc_chua is not None and sold >= suc_chua:
                    raise Exception("Chuyến bay đã hết chỗ!")

                # Insert ticket with guaranteed 'Booked' status
                sql = """INSERT INTO ve (MaVe, MaHanhKhach, MaLichBay, SoGhe, GiaVe, TrangThaiVe, TrangThai)
                         VALUES (%s, %s, %s, %s, %s, 'Booked', 'Active')"""
                cursor.execute(
                    sql,
                    (
                        ma_ve,
                        ma_hk,
                        ma_lich,
                        seat,
                        price,
                    ),
                )
                conn.commit()
            except Exception:
                try:
                    conn.rollback()
                except Exception:
                    pass
                raise

            messagebox.showinfo(
                "Thành công",
                f"Đặt vé {ma_ve} ({self.class_var.get()}) thành công!\nGiá vé: {int(price):,} VND",
            )

            # Clear form
            for key, e in self.booking_entries.items():
                e.delete(0, tk.END)
            self.price_entry.configure(state="normal")
            self.price_entry.delete(0, tk.END)
            self.price_entry.configure(state="readonly")
            self.class_var.set("Economy")
            if hasattr(self, "schedule_tree"):
                self.schedule_tree.delete(*self.schedule_tree.get_children())
            if hasattr(self, "lich_combobox"):
                self.lich_combobox.set("")

            if "Vé Máy Bay" in self.trees:
                self.refresh_tab("Vé Máy Bay")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if "conn" in locals() and conn:
                conn.close()

    # ====================== BÁO CÁO (FIX + MỞ RỘNG) ======================
    def create_report_tab(self):
        tab = tk.Frame(self.notebook, bg="#f1f5f9")
        self.notebook.add(tab, text="💰 Báo Cáo")

        tk.Label(
            tab,
            text="BÁO CÁO & THỐNG KÊ",
            font=("Segoe UI", 26, "bold"),
            bg="#f1f5f9",
            fg="#4f46e5",
        ).pack(pady=30)

        # Hàng 1: doanh thu
        row1 = tk.Frame(tab, bg="#f1f5f9")
        row1.pack(pady=6)
        tk.Button(
            row1,
            text="💰 Doanh Thu Hôm Nay",
            bg="#10b981",
            fg="white",
            width=22,
            font=("Segoe UI", 11, "bold"),
            command=lambda: self.show_revenue("today"),
        ).pack(side="left", padx=8)
        tk.Button(
            row1,
            text="💰 Tổng Doanh Thu",
            bg="#4f46e5",
            fg="white",
            width=22,
            font=("Segoe UI", 11, "bold"),
            command=lambda: self.show_revenue("total"),
        ).pack(side="left", padx=8)
        tk.Button(
            row1,
            text="📊 Doanh Thu Theo Hãng",
            bg="#8b5cf6",
            fg="white",
            width=22,
            font=("Segoe UI", 11, "bold"),
            command=self.show_revenue_by_airline,
        ).pack(side="left", padx=8)

        # Hàng 2: thống kê chuyến bay
        row2 = tk.Frame(tab, bg="#f1f5f9")
        row2.pack(pady=6)
        tk.Button(
            row2,
            text="🛫 Lịch Bay Hôm Nay",
            bg="#0ea5e9",
            fg="white",
            width=22,
            font=("Segoe UI", 11, "bold"),
            command=self.show_flights_today,
        ).pack(side="left", padx=8)
        tk.Button(
            row2,
            text="⚠️ Chuyến Bay Bị Delay",
            bg="#f59e0b",
            fg="white",
            width=22,
            font=("Segoe UI", 11, "bold"),
            command=self.show_delayed_flights,
        ).pack(side="left", padx=8)
        tk.Button(
            row2,
            text="🏆 Top 5 Hành Khách VIP",
            bg="#ef4444",
            fg="white",
            width=22,
            font=("Segoe UI", 11, "bold"),
            command=self.show_top_passengers,
        ).pack(side="left", padx=8)

        # Bảng kết quả
        result_frame = tk.Frame(tab, bg="white")
        result_frame.pack(fill="both", expand=True, padx=30, pady=20)

        self.report_tree = ttk.Treeview(result_frame, show="headings", height=20)
        rvsb = ttk.Scrollbar(
            result_frame, orient="vertical", command=self.report_tree.yview
        )
        rhsb = ttk.Scrollbar(
            result_frame, orient="horizontal", command=self.report_tree.xview
        )
        self.report_tree.configure(yscrollcommand=rvsb.set, xscrollcommand=rhsb.set)
        self.report_tree.grid(row=0, column=0, sticky="nsew")
        rvsb.grid(row=0, column=1, sticky="ns")
        rhsb.grid(row=1, column=0, sticky="ew")
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

    def _show_report(self, cols, rows, title="Kết quả"):
        self.report_tree.delete(*self.report_tree.get_children())
        self.report_tree["columns"] = cols
        for col in cols:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=200, anchor="center")
        for row in rows:
            self.report_tree.insert("", tk.END, values=row)

    def show_revenue(self, mode):
        conn = db()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            if mode == "today":
                cursor.execute(
                    """
                    SELECT COUNT(v.MaVe), COALESCE(SUM(v.GiaVe), 0)
                    FROM ve v
                    JOIN lich_chuyen_bay l ON v.MaLichBay = l.MaLichBay
                    WHERE l.NgayBay = %s AND v.TrangThaiVe != 'Cancelled' AND v.TrangThai = 'Active'
                """,
                    (today,),
                )
                label = f"Hôm nay ({today})"
            else:
                cursor.execute(
                    "SELECT COUNT(*), COALESCE(SUM(GiaVe), 0) FROM ve WHERE TrangThaiVe != 'Cancelled' AND TrangThai = 'Active'"
                )
                label = "Tổng cộng"

            count, total = cursor.fetchone()
            cols = ["Kỳ", "Số Vé", "Doanh Thu (VND)"]
            self._show_report(cols, [(label, count, f"{total:,.0f}")])
            messagebox.showinfo(
                "Doanh Thu", f"{label}\nSố vé: {count}\nDoanh thu: {total:,.0f} VND"
            )
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def show_revenue_by_airline(self):
        conn = db()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.TenHang, COUNT(v.MaVe) AS SoVe, COALESCE(SUM(v.GiaVe), 0) AS DoanhThu
                FROM ve v
                JOIN lich_chuyen_bay l ON v.MaLichBay = l.MaLichBay
                JOIN chuyen_bay c ON l.MaChuyenBay = c.MaChuyenBay
                JOIN hang_hang_khong h ON c.MaHang = h.MaHang
                WHERE v.TrangThaiVe != 'Cancelled' AND v.TrangThai = 'Active' AND h.TrangThai = 'Active'
                GROUP BY h.MaHang, h.TenHang
                ORDER BY DoanhThu DESC
            """)
            rows = [(r[0], r[1], f"{r[2]:,.0f}") for r in cursor.fetchall()]
            self._show_report(["Hãng Hàng Không", "Số Vé", "Doanh Thu (VND)"], rows)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def show_flights_today(self):
        conn = db()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                """
                SELECT l.MaLichBay, c.MaChuyenBay, s1.TenSanBay, s2.TenSanBay,
                       l.GioKhoiHanh, l.GioDenDuKien, l.TrangThai, h.TenHang
                FROM lich_chuyen_bay l
                JOIN chuyen_bay c ON l.MaChuyenBay = c.MaChuyenBay
                JOIN san_bay s1 ON c.MaSanBayDi = s1.MaSanBay
                JOIN san_bay s2 ON c.MaSanBayDen = s2.MaSanBay
                JOIN hang_hang_khong h ON c.MaHang = h.MaHang
                WHERE l.NgayBay = %s AND l.TrangThai != 'Cancelled'
                ORDER BY l.GioKhoiHanh
            """,
                (today,),
            )
            rows = cursor.fetchall()
            cols = [
                "MaLich",
                "MaChuyenBay",
                "Điểm Đi",
                "Điểm Đến",
                "Giờ Đi",
                "Giờ Đến",
                "Trạng Thái",
                "Hãng Bay",
            ]
            self._show_report(cols, rows)
            if not rows:
                messagebox.showinfo("Lịch Bay", f"Không có chuyến bay nào ngày {today}")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def show_delayed_flights(self):
        conn = db()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT l.MaLichBay, c.MaChuyenBay, l.NgayBay,
                       s1.ThanhPho, s2.ThanhPho, l.GioKhoiHanh, h.TenHang
                FROM lich_chuyen_bay l
                JOIN chuyen_bay c ON l.MaChuyenBay = c.MaChuyenBay
                JOIN san_bay s1 ON c.MaSanBayDi = s1.MaSanBay
                JOIN san_bay s2 ON c.MaSanBayDen = s2.MaSanBay
                JOIN hang_hang_khong h ON c.MaHang = h.MaHang
                WHERE l.TrangThai = 'Delayed'
                ORDER BY l.NgayBay, l.GioKhoiHanh
            """)
            rows = cursor.fetchall()
            cols = [
                "MaLich",
                "MaChuyenBay",
                "Ngày Bay",
                "Từ",
                "Đến",
                "Giờ Dự Kiến",
                "Hãng",
            ]
            self._show_report(cols, rows)
            if not rows:
                messagebox.showinfo("Delay", "Không có chuyến bay bị delay!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()

    def show_top_passengers(self):
        conn = db()
        if not conn:
            return
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT hk.HoTen, COUNT(v.MaVe) AS SoVe, COALESCE(SUM(v.GiaVe), 0) AS TongChiTieu
                FROM hanh_khach hk
                JOIN ve v ON hk.MaHanhKhach = v.MaHanhKhach
                WHERE v.TrangThaiVe != 'Cancelled' AND v.TrangThai = 'Active' AND hk.TrangThai = 'Active'
                GROUP BY hk.MaHanhKhach, hk.HoTen
                ORDER BY TongChiTieu DESC
                LIMIT 5
            """)
            rows = [(r[0], r[1], f"{r[2]:,.0f}") for r in cursor.fetchall()]
            self._show_report(["Họ Tên", "Số Vé", "Tổng Chi Tiêu (VND)"], rows)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            conn.close()


if __name__ == "__main__":
    LoginWindow()
