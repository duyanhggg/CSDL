import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

def db():
    try:
        return mysql.connector.connect(
            host="localhost", user="root", password="17052007",
            database="baitaplondb", charset="utf8mb4"
        )
    except Exception as e:
        messagebox.showerror("Lỗi Kết nối", str(e))
        return None

# Mapping tên tab → tên bảng SQL (fix lỗi tiếng Việt có dấu)
TABLE_MAP = {
    "Sân Bay":           "san_bay",
    "Hãng Hàng Không":  "hang_hang_khong",
    "Máy Bay":           "may_bay",
    "Cửa Bay":           "cua_bay",
    "Chuyến Bay":        "chuyen_bay",
    "Lịch Chuyến Bay":  "lich_chuyen_bay",
    "Hành Khách":        "hanh_khach",
    "Nhân Viên":         "nhan_vien",
    "Vé Máy Bay":        "ve",
    "Phân Công CB":      "phan_cong_chuyen_bay",
}


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Đăng Nhập")
        self.root.geometry("460x320")
        self.root.configure(bg="#f8fafc")
        self.root.resizable(False, False)

        tk.Label(self.root, text="✈️ AIRPORT MANAGEMENT SYSTEM",
                 font=("Segoe UI", 16, "bold"), bg="#f8fafc", fg="#4f46e5").pack(pady=30)

        tk.Label(self.root, text="Username", bg="#f8fafc", fg="#334155", font=("Segoe UI", 11)).pack(anchor="w", padx=80)
        self.un = tk.Entry(self.root, width=30, bg="white", fg="#1e2937", font=("Segoe UI", 11), relief="solid", bd=1)
        self.un.pack(pady=5)
        self.un.insert(0, "admin")

        tk.Label(self.root, text="Password", bg="#f8fafc", fg="#334155", font=("Segoe UI", 11)).pack(anchor="w", padx=80)
        self.pw = tk.Entry(self.root, width=30, bg="white", fg="#1e2937", font=("Segoe UI", 11), show="•", relief="solid", bd=1)
        self.pw.pack(pady=5)
        self.pw.insert(0, "123456")

        tk.Button(self.root, text="ĐĂNG NHẬP", bg="#4f46e5", fg="white",
                  font=("Segoe UI", 12, "bold"), width=20, height=2, command=self.login).pack(pady=30)

        self.root.mainloop()

    def login(self):
        if self.un.get() == "admin" and self.pw.get() == "123456":
            self.root.destroy()
            AirportManagementSystem()
        else:
            messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")


class AirportManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("✈️ Airport Management System")
        self.root.geometry("1720x980")
        self.root.configure(bg="#f1f5f9")
        self.root.state('zoomed')

        self.style_setup()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self.trees = {}
        self.queries = {}
        self.search_vars = {}
        self._all_rows = {}  # cache dữ liệu gốc để lọc

        self.create_dashboard()
        self.create_all_data_tabs()
        self.create_booking_tab()
        self.create_report_tab()

        self.root.mainloop()

    def style_setup(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#f1f5f9")
        style.configure("TNotebook.Tab", padding=[18, 12], font=("Segoe UI", 10, "bold"),
                        background="#e2e8f0", foreground="#475569")
        style.map("TNotebook.Tab", background=[("selected", "#4f46e5")], foreground=[("selected", "white")])

        style.configure("Treeview", background="white", foreground="#1e2937",
                        fieldbackground="white", rowheight=36, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#4f46e5", foreground="white",
                        font=("Segoe UI", 10, "bold"))

    def create_dashboard(self):
        dash = tk.Frame(self.notebook, bg="#f1f5f9")
        self.notebook.add(dash, text="🏠 Dashboard")

        tk.Label(dash, text="✈️ AIRPORT MANAGEMENT SYSTEM", font=("Segoe UI", 38, "bold"),
                 bg="#f1f5f9", fg="#4f46e5").pack(pady=60)
        tk.Label(dash, text="Hệ thống quản lý sân bay – Sân bay Nội Bài",
                 font=("Segoe UI", 16), bg="#f1f5f9", fg="#64748b").pack()

        # Ô thống kê nhanh
        stat_frame = tk.Frame(dash, bg="#f1f5f9")
        stat_frame.pack(pady=40)
        stats = [
            ("🛫 Chuyến Bay", "SELECT COUNT(*) FROM chuyen_bay", "#4f46e5"),
            ("📅 Lịch Bay", "SELECT COUNT(*) FROM lich_chuyen_bay", "#0ea5e9"),
            ("👤 Hành Khách", "SELECT COUNT(*) FROM hanh_khach", "#10b981"),
            ("🎟️ Vé Đã Bán", "SELECT COUNT(*) FROM ve WHERE TrangThaiVe='Booked'", "#f59e0b"),
            ("👨‍✈️ Nhân Viên", "SELECT COUNT(*) FROM nhan_vien", "#8b5cf6"),
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
            tk.Label(card, text=str(val), font=("Segoe UI", 32, "bold"), bg=color, fg="white").pack(pady=12)
            tk.Label(card, text=label, font=("Segoe UI", 11), bg=color, fg="white").pack()
        if conn:
            conn.close()

    # ==================== TẤT CẢ TAB DỮ LIỆU ====================
    def create_all_data_tabs(self):
        tabs_config = [
            # (Tên hiển thị, [cột], query SQL, primary key)
            ("Sân Bay",
             ["MaSanBay", "TenSanBay", "ThanhPho", "QuocGia"],
             "SELECT * FROM san_bay", "MaSanBay"),

            ("Hãng Hàng Không",
             ["MaHang", "TenHang", "QuocGia", "SoDienThoai", "Email"],
             "SELECT * FROM hang_hang_khong", "MaHang"),

            ("Máy Bay",
             ["MaMayBay", "LoaiMayBay", "SucChua", "NamSanXuat", "MaHang"],
             "SELECT * FROM may_bay", "MaMayBay"),

            # ── Bổ sung: Cửa Bay ──
            ("Cửa Bay",
             ["MaCuaBay", "TenCuaBay", "MaSanBay", "TrangThai"],
             "SELECT * FROM cua_bay", "MaCuaBay"),

            # ── Bổ sung: Chuyến Bay ──
            ("Chuyến Bay",
             ["MaChuyenBay", "MaHang", "MaSanBayDi", "MaSanBayDen", "ThoiGianBayDuKien"],
             "SELECT * FROM chuyen_bay", "MaChuyenBay"),

            # ── Bổ sung: Lịch Chuyến Bay ──
            ("Lịch Chuyến Bay",
             ["MaLichBay", "MaChuyenBay", "NgayBay", "GioKhoiHanh",
              "GioDenDuKien", "MaMayBay", "MaCuaBay", "TrangThai"],
             "SELECT * FROM lich_chuyen_bay", "MaLichBay"),

            ("Hành Khách",
             ["MaHanhKhach", "HoTen", "NgaySinh", "GioiTinh",
              "CCCD", "SoDienThoai", "Email", "DiaChi"],
             "SELECT * FROM hanh_khach", "MaHanhKhach"),

            # ── Bổ sung: Nhân Viên ──
            ("Nhân Viên",
             ["MaNhanVien", "HoTen", "NgaySinh", "GioiTinh",
              "SoDienThoai", "Email", "ChucVu", "BangCap", "MaHang"],
             "SELECT * FROM nhan_vien", "MaNhanVien"),

            ("Vé Máy Bay",
             ["MaVe", "MaHanhKhach", "MaLichBay", "SoGhe", "GiaVe", "TrangThaiVe"],
             "SELECT * FROM ve", "MaVe"),

            # ── Bổ sung: Phân Công Chuyến Bay ──
            ("Phân Công CB",
             ["MaPhanCong", "MaNhanVien", "MaLichBay", "VaiTro"],
             "SELECT * FROM phan_cong_chuyen_bay", "MaPhanCong"),
        ]

        for name, cols, query, pk in tabs_config:
            tab = tk.Frame(self.notebook, bg="#f1f5f9")
            self.notebook.add(tab, text=name)
            self.queries[name] = query

            # Thanh tìm kiếm
            sf = tk.Frame(tab, bg="#f1f5f9")
            sf.pack(fill="x", padx=20, pady=12)
            tk.Label(sf, text="🔍 Tìm kiếm:", bg="#f1f5f9", fg="#334155",
                     font=("Segoe UI", 11, "bold")).pack(side="left")
            search_var = tk.StringVar()
            self.search_vars[name] = search_var
            entry = tk.Entry(sf, textvariable=search_var, width=60, font=("Segoe UI", 11),
                             bg="white", fg="#1e2937", relief="solid", bd=1)
            entry.pack(side="left", padx=10)
            entry.bind("<KeyRelease>", lambda e, n=name: self.filter_tree(n))

            container = tk.Frame(tab, bg="white")
            container.pack(fill="both", expand=True, padx=20, pady=5)

            tree = ttk.Treeview(container, columns=cols, show="headings", height=20)
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=160, anchor="center")

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
            tk.Button(btnf, text="🔄 Làm Mới", bg="#4f46e5", fg="white", width=14,
                      command=lambda n=name: self.refresh_tab(n)).pack(side="left", padx=5)
            tk.Button(btnf, text="➕ Thêm", bg="#10b981", fg="white", width=12,
                      command=lambda t=tree, n=name: self.add_record(t, n)).pack(side="left", padx=5)
            tk.Button(btnf, text="✏️ Sửa", bg="#eab308", fg="black", width=12,
                      command=lambda t=tree, n=name: self.edit_record(t, n)).pack(side="left", padx=5)
            tk.Button(btnf, text="🗑️ Xóa", bg="#ef4444", fg="white", width=12,
                      command=lambda t=tree, n=name: self.delete_record(t, n)).pack(side="left", padx=5)

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

    # ====================== FORM THÊM MỚI ======================
    def add_record(self, tree, tab_name):
        cols = tree["columns"]
        pk_col = self.trees[tab_name][1]
        tbl = TABLE_MAP.get(tab_name, tab_name)

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Thêm {tab_name}")
        dialog.geometry("700x620")
        dialog.configure(bg="#f8fafc")
        dialog.grab_set()

        tk.Label(dialog, text=f"THÊM {tab_name.upper()}", font=("Segoe UI", 14, "bold"),
                 bg="#f8fafc", fg="#4f46e5").grid(row=0, column=0, columnspan=2, pady=20)

        entries = {}
        for i, col in enumerate(cols):
            tk.Label(dialog, text=col + ":", bg="#f8fafc", fg="#334155",
                     font=("Segoe UI", 11, "bold")).grid(row=i+1, column=0, sticky="w", padx=20, pady=8)
            e = tk.Entry(dialog, width=55, font=("Segoe UI", 11), bg="white", relief="solid", bd=1)
            e.grid(row=i+1, column=1, padx=20, pady=8)
            entries[col] = e

        def save():
            vals = [entries[col].get().strip() for col in cols]
            if not vals[0]:
                messagebox.showwarning("Lỗi", f"Vui lòng nhập {pk_col}!", parent=dialog)
                return
            conn = db()
            try:
                cursor = conn.cursor()
                placeholders = ", ".join(["%s"] * len(cols))
                col_names = ", ".join([f"`{c}`" for c in cols])
                sql = f"INSERT INTO `{tbl}` ({col_names}) VALUES ({placeholders})"
                cursor.execute(sql, vals)
                conn.commit()
                messagebox.showinfo("Thành công", "Thêm dữ liệu thành công!", parent=dialog)
                dialog.destroy()
                self.refresh_tab(tab_name)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e), parent=dialog)
            finally:
                if conn:
                    conn.close()

        tk.Button(dialog, text="➕ THÊM MỚI", bg="#10b981", fg="white",
                  font=("Segoe UI", 12, "bold"), width=20, command=save).grid(
                  row=len(cols)+2, column=1, pady=25)

    # ====================== FORM SỬA ======================
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

        tk.Label(dialog, text=f"SỬA {tab_name.upper()}", font=("Segoe UI", 14, "bold"),
                 bg="#f8fafc", fg="#eab308").grid(row=0, column=0, columnspan=2, pady=20)

        entries = {}
        for i, col in enumerate(cols):
            tk.Label(dialog, text=col + ":", bg="#f8fafc", fg="#334155",
                     font=("Segoe UI", 11, "bold")).grid(row=i+1, column=0, sticky="w", padx=20, pady=8)
            e = tk.Entry(dialog, width=55, font=("Segoe UI", 11), bg="white", relief="solid", bd=1)
            e.grid(row=i+1, column=1, padx=20, pady=8)
            e.insert(0, values[i])
            # Khóa chính không cho sửa
            if col == pk_col:
                e.configure(state="readonly", bg="#e2e8f0")
            entries[col] = e

        def save():
            new_values = [entries[col].get().strip() for col in cols]
            conn = db()
            try:
                cursor = conn.cursor()
                set_clause = ", ".join([f"`{col}` = %s" for col in cols])
                sql = f"UPDATE `{tbl}` SET {set_clause} WHERE `{pk_col}` = %s"
                cursor.execute(sql, (*new_values, pk_value))
                conn.commit()
                messagebox.showinfo("Thành công", "Cập nhật dữ liệu thành công!", parent=dialog)
                dialog.destroy()
                self.refresh_tab(tab_name)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e), parent=dialog)
            finally:
                if conn:
                    conn.close()

        tk.Button(dialog, text="💾 LƯU THAY ĐỔI", bg="#10b981", fg="white",
                  font=("Segoe UI", 12, "bold"), width=20, command=save).grid(
                  row=len(cols)+2, column=1, pady=25)

    # ====================== XÓA BẢN GHI (BỔ SUNG) ======================
    def delete_record(self, tree, tab_name):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chú ý", "Vui lòng chọn dòng cần xóa!")
            return

        values = tree.item(selected[0])["values"]
        pk_col = self.trees[tab_name][1]
        pk_value = values[0]
        tbl = TABLE_MAP.get(tab_name, tab_name)

        confirm = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa bản ghi [{pk_col} = {pk_value}]?\nHành động này không thể hoàn tác!"
        )
        if not confirm:
            return

        conn = db()
        try:
            cursor = conn.cursor()
            sql = f"DELETE FROM `{tbl}` WHERE `{pk_col}` = %s"
            cursor.execute(sql, (pk_value,))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã xóa bản ghi {pk_value} thành công!")
            self.refresh_tab(tab_name)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa:\n{str(e)}\n\n(Có thể do ràng buộc khóa ngoại)")
        finally:
            if conn:
                conn.close()

    # ====================== FORM ĐẶT VÉ ======================
    def create_booking_tab(self):
        tab = tk.Frame(self.notebook, bg="#f1f5f9")
        self.notebook.add(tab, text="🎟️ Đặt Vé")

        main = tk.Frame(tab, bg="white", padx=60, pady=40)
        main.pack(pady=30, fill="both", expand=True)

        tk.Label(main, text="ĐẶT VÉ MÁY BAY", font=("Segoe UI", 24, "bold"),
                 bg="white", fg="#4f46e5").pack(pady=20)

        fields = ["Mã Vé", "Mã Hành Khách", "Mã Lịch Bay", "Số Ghế"]
        self.booking_entries = {}

        form = tk.Frame(main, bg="white")
        form.pack()

        for i, f in enumerate(fields):
            tk.Label(form, text=f + ":", bg="white", fg="#334155",
                     font=("Segoe UI", 12, "bold")).grid(row=i, column=0, sticky="w", pady=12, padx=20)
            e = tk.Entry(form, width=45, font=("Segoe UI", 11), bg="#f8fafc", relief="solid", bd=1)
            e.grid(row=i, column=1, pady=12, padx=20)
            self.booking_entries[f] = e

        # Hạng vé
        tk.Label(form, text="Hạng Vé:", bg="white", fg="#334155",
                 font=("Segoe UI", 12, "bold")).grid(row=4, column=0, sticky="w", pady=12, padx=20)
        self.class_var = tk.StringVar(value="Economy")
        class_frame = tk.Frame(form, bg="white")
        class_frame.grid(row=4, column=1, sticky="w", padx=20)
        for c in ["Economy", "Business", "First Class"]:
            tk.Radiobutton(class_frame, text=c, variable=self.class_var, value=c,
                           bg="white", font=("Segoe UI", 11), command=self.calculate_price).pack(side="left", padx=10)

        # Giá vé
        tk.Label(form, text="Giá Vé (VND):", bg="white", fg="#334155",
                 font=("Segoe UI", 12, "bold")).grid(row=5, column=0, sticky="w", pady=12, padx=20)
        self.price_entry = tk.Entry(form, width=45, font=("Segoe UI", 11),
                                    bg="#f8fafc", fg="#10b981", relief="solid", bd=1)
        self.price_entry.grid(row=5, column=1, pady=12, padx=20)

        tk.Button(form, text="Tính Giá Theo Hạng", bg="#eab308", fg="black",
                  font=("Segoe UI", 10, "bold"), command=self.calculate_price).grid(
                  row=6, column=1, sticky="w", padx=20, pady=10)

        tk.Button(tab, text="✅ XÁC NHẬN ĐẶT VÉ", width=25, height=3,
                  bg="#10b981", fg="white", font=("Segoe UI", 14, "bold"),
                  command=self.book_ticket).pack(pady=30)

    def calculate_price(self):
        multipliers = {"Economy": 1.0, "Business": 2.3, "First Class": 3.8}
        base = 1_800_000
        price = int(base * multipliers[self.class_var.get()])
        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, f"{price:,}")

    def book_ticket(self):
        try:
            data = {k: v.get().strip() for k, v in self.booking_entries.items()}
            price = self.price_entry.get().strip().replace(",", "")

            if not all(data.values()) or not price:
                messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ!")
                return

            conn = db()
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM hanh_khach WHERE MaHanhKhach = %s", (data["Mã Hành Khách"],))
            if not cursor.fetchone():
                raise Exception("Mã hành khách không tồn tại!")

            cursor.execute("SELECT 1 FROM lich_chuyen_bay WHERE MaLichBay = %s", (data["Mã Lịch Bay"],))
            if not cursor.fetchone():
                raise Exception("Mã lịch bay không tồn tại!")

            # Kiểm tra trùng mã vé
            cursor.execute("SELECT 1 FROM ve WHERE MaVe = %s", (data["Mã Vé"],))
            if cursor.fetchone():
                raise Exception("Mã vé đã tồn tại, vui lòng dùng mã khác!")

            sql = """INSERT INTO ve (MaVe, MaHanhKhach, MaLichBay, SoGhe, GiaVe, TrangThaiVe)
                     VALUES (%s, %s, %s, %s, %s, 'Booked')"""
            cursor.execute(sql, (data["Mã Vé"], data["Mã Hành Khách"], data["Mã Lịch Bay"],
                                 data["Số Ghế"], price))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đặt vé {data['Mã Vé']} ({self.class_var.get()}) thành công!")

            # Clear form
            for e in self.booking_entries.values():
                e.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)

            if "Vé Máy Bay" in self.trees:
                self.refresh_tab("Vé Máy Bay")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    # ====================== BÁO CÁO (FIX + MỞ RỘNG) ======================
    def create_report_tab(self):
        tab = tk.Frame(self.notebook, bg="#f1f5f9")
        self.notebook.add(tab, text="💰 Báo Cáo")

        tk.Label(tab, text="BÁO CÁO & THỐNG KÊ", font=("Segoe UI", 26, "bold"),
                 bg="#f1f5f9", fg="#4f46e5").pack(pady=30)

        # Hàng 1: doanh thu
        row1 = tk.Frame(tab, bg="#f1f5f9")
        row1.pack(pady=6)
        tk.Button(row1, text="💰 Doanh Thu Hôm Nay", bg="#10b981", fg="white", width=22,
                  font=("Segoe UI", 11, "bold"),
                  command=lambda: self.show_revenue("today")).pack(side="left", padx=8)
        tk.Button(row1, text="💰 Tổng Doanh Thu", bg="#4f46e5", fg="white", width=22,
                  font=("Segoe UI", 11, "bold"),
                  command=lambda: self.show_revenue("total")).pack(side="left", padx=8)
        tk.Button(row1, text="📊 Doanh Thu Theo Hãng", bg="#8b5cf6", fg="white", width=22,
                  font=("Segoe UI", 11, "bold"),
                  command=self.show_revenue_by_airline).pack(side="left", padx=8)

        # Hàng 2: thống kê chuyến bay
        row2 = tk.Frame(tab, bg="#f1f5f9")
        row2.pack(pady=6)
        tk.Button(row2, text="🛫 Lịch Bay Hôm Nay", bg="#0ea5e9", fg="white", width=22,
                  font=("Segoe UI", 11, "bold"),
                  command=self.show_flights_today).pack(side="left", padx=8)
        tk.Button(row2, text="⚠️ Chuyến Bay Bị Delay", bg="#f59e0b", fg="white", width=22,
                  font=("Segoe UI", 11, "bold"),
                  command=self.show_delayed_flights).pack(side="left", padx=8)
        tk.Button(row2, text="🏆 Top 5 Hành Khách VIP", bg="#ef4444", fg="white", width=22,
                  font=("Segoe UI", 11, "bold"),
                  command=self.show_top_passengers).pack(side="left", padx=8)

        # Bảng kết quả
        result_frame = tk.Frame(tab, bg="white")
        result_frame.pack(fill="both", expand=True, padx=30, pady=20)

        self.report_tree = ttk.Treeview(result_frame, show="headings", height=20)
        rvsb = ttk.Scrollbar(result_frame, orient="vertical", command=self.report_tree.yview)
        rhsb = ttk.Scrollbar(result_frame, orient="horizontal", command=self.report_tree.xview)
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
                # Fix: lọc vé theo ngày bay hôm nay (join với lịch bay)
                cursor.execute("""
                    SELECT COUNT(v.MaVe), COALESCE(SUM(v.GiaVe), 0)
                    FROM ve v
                    JOIN lich_chuyen_bay l ON v.MaLichBay = l.MaLichBay
                    WHERE l.NgayBay = %s AND v.TrangThaiVe != 'Cancelled'
                """, (today,))
                label = f"Hôm nay ({today})"
            else:
                cursor.execute("SELECT COUNT(*), COALESCE(SUM(GiaVe), 0) FROM ve WHERE TrangThaiVe != 'Cancelled'")
                label = "Tổng cộng"

            count, total = cursor.fetchone()
            cols = ["Kỳ", "Số Vé", "Doanh Thu (VND)"]
            self._show_report(cols, [(label, count, f"{total:,.0f}")])
            messagebox.showinfo("Doanh Thu", f"{label}\nSố vé: {count}\nDoanh thu: {total:,.0f} VND")
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
                WHERE v.TrangThaiVe != 'Cancelled'
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
            cursor.execute("""
                SELECT l.MaLichBay, c.MaChuyenBay, s1.TenSanBay, s2.TenSanBay,
                       l.GioKhoiHanh, l.GioDenDuKien, l.TrangThai, h.TenHang
                FROM lich_chuyen_bay l
                JOIN chuyen_bay c ON l.MaChuyenBay = c.MaChuyenBay
                JOIN san_bay s1 ON c.MaSanBayDi = s1.MaSanBay
                JOIN san_bay s2 ON c.MaSanBayDen = s2.MaSanBay
                JOIN hang_hang_khong h ON c.MaHang = h.MaHang
                WHERE l.NgayBay = %s
                ORDER BY l.GioKhoiHanh
            """, (today,))
            rows = cursor.fetchall()
            cols = ["MaLich", "MaChuyenBay", "Điểm Đi", "Điểm Đến",
                    "Giờ Đi", "Giờ Đến", "Trạng Thái", "Hãng Bay"]
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
            cols = ["MaLich", "MaChuyenBay", "Ngày Bay", "Từ", "Đến", "Giờ Dự Kiến", "Hãng"]
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
                WHERE v.TrangThaiVe != 'Cancelled'
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
