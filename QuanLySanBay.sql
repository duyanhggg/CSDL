CREATE DATABASE QuanLySanBay;
USE QuanLySanBay;

CREATE TABLE HANG_HANG_KHONG (
    MaHang VARCHAR(10) PRIMARY KEY,
    TenHang VARCHAR(100) NOT NULL,
    QuocGia VARCHAR(50) NOT NULL,
    SoDienThoai VARCHAR(15),
    Email VARCHAR(100)
);

CREATE TABLE SAN_BAY (
    MaSanBay CHAR(3) PRIMARY KEY,
    TenSanBay VARCHAR(100) NOT NULL,
    ThanhPho VARCHAR(100) NOT NULL,
    QuocGia VARCHAR(50) NOT NULL
);

CREATE TABLE MAY_BAY (
    MaMayBay VARCHAR(20) PRIMARY KEY,
    LoaiMayBay VARCHAR(50) NOT NULL,
    SucChua INT NOT NULL CHECK (SucChua > 0),
    NamSanXuat YEAR,
    MaHang VARCHAR(10) NOT NULL,
    FOREIGN KEY (MaHang) REFERENCES HANG_HANG_KHONG(MaHang)
);

CREATE TABLE CUA_BAY (
    MaCuaBay VARCHAR(10) PRIMARY KEY,
    TenCuaBay VARCHAR(20) NOT NULL,
    MaSanBay CHAR(3) NOT NULL,
    TrangThai ENUM('Available','Occupied') DEFAULT 'Available',
    FOREIGN KEY (MaSanBay) REFERENCES SAN_BAY(MaSanBay)
);

CREATE TABLE CHUYEN_BAY (
    MaChuyenBay VARCHAR(10) PRIMARY KEY,
    MaHang VARCHAR(10) NOT NULL,
    MaSanBayDi CHAR(3) NOT NULL,
    MaSanBayDen CHAR(3) NOT NULL,
    ThoiGianBayDuKien INT NOT NULL,
    FOREIGN KEY (MaHang) REFERENCES HANG_HANG_KHONG(MaHang),
    FOREIGN KEY (MaSanBayDi) REFERENCES SAN_BAY(MaSanBay),
    FOREIGN KEY (MaSanBayDen) REFERENCES SAN_BAY(MaSanBay)
);

CREATE TABLE LICH_CHUYEN_BAY (
    MaLichBay INT AUTO_INCREMENT PRIMARY KEY,
    MaChuyenBay VARCHAR(10) NOT NULL,
    NgayBay DATE NOT NULL,
    GioKhoiHanh TIME NOT NULL,
    GioDenDuKien TIME NOT NULL,
    MaMayBay VARCHAR(20) NOT NULL,
    MaCuaBay VARCHAR(10) NOT NULL,
    TrangThai ENUM('Scheduled','Delayed','Departed','Arrived','Cancelled') DEFAULT 'Scheduled',
    FOREIGN KEY (MaChuyenBay) REFERENCES CHUYEN_BAY(MaChuyenBay),
    FOREIGN KEY (MaMayBay) REFERENCES MAY_BAY(MaMayBay),
    FOREIGN KEY (MaCuaBay) REFERENCES CUA_BAY(MaCuaBay)
);

CREATE TABLE HANH_KHACH (
    MaHanhKhach VARCHAR(15) PRIMARY KEY,
    HoTen VARCHAR(100) NOT NULL,
    NgaySinh DATE,
    GioiTinh ENUM('Nam','Nu','Khac'),
    CCCD VARCHAR(20) UNIQUE,
    SoDienThoai VARCHAR(15),
    Email VARCHAR(100),
    DiaChi VARCHAR(255)
);

CREATE TABLE NHAN_VIEN (
    MaNhanVien VARCHAR(10) PRIMARY KEY,
    HoTen VARCHAR(100) NOT NULL,
    NgaySinh DATE,
    GioiTinh ENUM('Nam','Nu'),
    SoDienThoai VARCHAR(15),
    Email VARCHAR(100),
    ChucVu ENUM('CoTruong','CoPho','TiepVien','NhanVienSanBay') NOT NULL,
    BangCap VARCHAR(100),
    MaHang VARCHAR(10),
    FOREIGN KEY (MaHang) REFERENCES HANG_HANG_KHONG(MaHang)
);

CREATE TABLE VE (
    MaVe VARCHAR(20) PRIMARY KEY,
    MaHanhKhach VARCHAR(15) NOT NULL,
    MaLichBay INT NOT NULL,
    SoGhe VARCHAR(10),
    GiaVe DECIMAL(12,2) NOT NULL,
    TrangThaiVe ENUM('Booked','CheckedIn','Cancelled') DEFAULT 'Booked',
    FOREIGN KEY (MaHanhKhach) REFERENCES HANH_KHACH(MaHanhKhach),
    FOREIGN KEY (MaLichBay) REFERENCES LICH_CHUYEN_BAY(MaLichBay)
);

CREATE TABLE PHAN_CONG_CHUYEN_BAY (
    MaPhanCong INT AUTO_INCREMENT PRIMARY KEY,
    MaNhanVien VARCHAR(10) NOT NULL,
    MaLichBay INT NOT NULL,
    VaiTro VARCHAR(50),
    FOREIGN KEY (MaNhanVien) REFERENCES NHAN_VIEN(MaNhanVien),
    FOREIGN KEY (MaLichBay) REFERENCES LICH_CHUYEN_BAY(MaLichBay)
);
