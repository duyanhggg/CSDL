USE QuanLySanBay;

INSERT INTO HANG_HANG_KHONG (MaHang, TenHang, QuocGia, SoDienThoai, Email) VALUES
('VNA', 'Vietnam Airlines', 'Vietnam', '19005566', 'info@vietnamairlines.com'),
('VJC', 'VietJet Air', 'Vietnam', '19001886', 'support@vietjetair.com'),
('BAV', 'Bamboo Airways', 'Vietnam', '19001166', 'info@bambooairways.com'),
('QTR', 'Qatar Airways', 'Qatar', '+97440230000', 'info@qatarairways.com'),
('EMA', 'Emirates', 'UAE', '+971600555555', 'eksupport@emirates.com');

INSERT INTO SAN_BAY (MaSanBay, TenSanBay, ThanhPho, QuocGia) VALUES
('HAN','San bay Quoc te Noi Bai','Ha Noi','Vietnam'),
('SGN','San bay Quoc te Tan Son Nhat','TP. Ho Chi Minh','Vietnam'),
('DAD','San bay Quoc te Da Nang','Da Nang','Vietnam'),
('SIN','San bay Changi','Singapore','Singapore'),
('ICN','San bay Incheon','Seoul','South Korea');

INSERT INTO MAY_BAY (MaMayBay, LoaiMayBay, SucChua, NamSanXuat, MaHang) VALUES
('VN-A321','Airbus A321',220,2018,'VNA'),
('VN-B789','Boeing 787-9',300,2020,'VNA'),
('VJ-A320','Airbus A320',180,2019,'VJC'),
('QR-A380','Airbus A380',489,2015,'QTR'),
('EK-B777','Boeing 777-300ER',354,2019,'EMA');

INSERT INTO HANH_KHACH (MaHanhKhach, HoTen, NgaySinh, GioiTinh, CCCD, SoDienThoai, Email, DiaChi) VALUES
('HK00001','Nguyen Van An','1995-03-15','Nam','012345678901','0987123456','an@email.com','Ha Noi'),
('HK00002','Tran Thi Binh','1998-07-22','Nu','098765432109','0912345678','binh@email.com','TP. HCM'),
('HK00003','Le Minh Cuong','1990-11-05','Nam','112233445566','0978123456','cuong@email.com','Da Nang');

INSERT INTO VE (MaVe, MaHanhKhach, MaLichBay, SoGhe, GiaVe, TrangThaiVe) VALUES
('VE00001','HK00001',1,'12A',1850000.00,'Booked'),
('VE00002','HK00002',2,'15B',2100000.00,'CheckedIn'),
('VE00003','HK00003',3,'08C',1350000.00,'Booked');
