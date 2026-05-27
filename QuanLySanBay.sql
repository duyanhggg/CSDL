-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: baitaplondb
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chuyen_bay`
--

DROP TABLE IF EXISTS `chuyen_bay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chuyen_bay` (
  `MaChuyenBay` varchar(10) NOT NULL,
  `MaHang` varchar(10) NOT NULL,
  `MaSanBayDi` char(3) NOT NULL,
  `MaSanBayDen` char(3) NOT NULL,
  `ThoiGianBayDuKien` int NOT NULL,
  `TrangThai` enum('Active','Inactive') DEFAULT 'Active',
  PRIMARY KEY (`MaChuyenBay`),
  KEY `MaHang` (`MaHang`),
  KEY `MaSanBayDi` (`MaSanBayDi`),
  KEY `MaSanBayDen` (`MaSanBayDen`),
  CONSTRAINT `chuyen_bay_ibfk_1` FOREIGN KEY (`MaHang`) REFERENCES `hang_hang_khong` (`MaHang`),
  CONSTRAINT `chuyen_bay_ibfk_2` FOREIGN KEY (`MaSanBayDi`) REFERENCES `san_bay` (`MaSanBay`),
  CONSTRAINT `chuyen_bay_ibfk_3` FOREIGN KEY (`MaSanBayDen`) REFERENCES `san_bay` (`MaSanBay`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chuyen_bay`
--

LOCK TABLES `chuyen_bay` WRITE;
/*!40000 ALTER TABLE `chuyen_bay` DISABLE KEYS */;
INSERT INTO `chuyen_bay` VALUES ('BL303','PAS','SGN','DAD',85,'Active'),('EK602','EMA','SGN','DXB',680,'Active'),('JL802','JAL','HAN','NRT',350,'Active'),('KE100','KAL','HAN','ICN',240,'Active'),('QH101','BAV','HAN','CXR',110,'Active'),('QH509','BAV','HAN','BMV',95,'Active'),('QR501','QTR','HAN','DXB',720,'Active'),('SQ701','SIA','HAN','SIN',180,'Active'),('VJ408','VJC','DAD','SGN',80,'Active'),('VJ456','VJC','HAN','DAD',90,'Active'),('VJ789','VJC','SGN','HAN',130,'Active'),('VN123','VNA','HAN','SGN',120,'Active'),('VN224','VNA','SGN','HAN',125,'Active'),('VN305','VNA','HAN','HPH',45,'Active'),('VN612','VNA','SGN','BKK',95,'Active'),('VU202','VRA','HAN','PQC',135,'Active');
/*!40000 ALTER TABLE `chuyen_bay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cua_bay`
--

DROP TABLE IF EXISTS `cua_bay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cua_bay` (
  `MaCuaBay` varchar(10) NOT NULL,
  `TenCuaBay` varchar(20) NOT NULL,
  `MaSanBay` char(3) NOT NULL,
  `TrangThai` enum('Available','Occupied') DEFAULT 'Available',
  PRIMARY KEY (`MaCuaBay`),
  KEY `MaSanBay` (`MaSanBay`),
  CONSTRAINT `cua_bay_ibfk_1` FOREIGN KEY (`MaSanBay`) REFERENCES `san_bay` (`MaSanBay`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cua_bay`
--

LOCK TABLES `cua_bay` WRITE;
/*!40000 ALTER TABLE `cua_bay` DISABLE KEYS */;
INSERT INTO `cua_bay` VALUES ('DAD-08','Cổng 08','DAD','Available'),('SGN-12','Cổng 12','SGN','Available'),('SGN-25','Cổng 25','SGN','Occupied'),('T1-A1','Cổng A1','HAN','Available'),('T1-A2','Cổng A2','HAN','Available'),('T1-B3','Cổng B3','HAN','Occupied'),('T1-D7','Cổng D7','HAN','Available'),('T2-C5','Cổng C5','HAN','Available');
/*!40000 ALTER TABLE `cua_bay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hang_hang_khong`
--

DROP TABLE IF EXISTS `hang_hang_khong`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hang_hang_khong` (
  `MaHang` varchar(10) NOT NULL,
  `TenHang` varchar(100) NOT NULL,
  `QuocGia` varchar(50) NOT NULL,
  `SoDienThoai` varchar(30) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `TrangThai` enum('Active','Inactive') DEFAULT 'Active',
  PRIMARY KEY (`MaHang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hang_hang_khong`
--

LOCK TABLES `hang_hang_khong` WRITE;
/*!40000 ALTER TABLE `hang_hang_khong` DISABLE KEYS */;
INSERT INTO `hang_hang_khong` VALUES ('AFR','Air France','France','+33 1 43 17 20 00','contact@airfrance.fr','Active'),('BAV','Bamboo Airways','Vietnam','19001166','info@bambooairways.com','Active'),('BAV2','Bamboo Cargo','Vietnam','19001167','cargo@bambooairways.com','Active'),('EMA','Emirates','UAE','+971 600 555 555','eksupport@emirates.com','Active'),('EMA2','Emirates SkyCargo','UAE','+971 600 555 666','skycargo@emirates.com','Active'),('JAL','Japan Airlines','Japan','+81 3 5460 1111','info@jal.com','Active'),('JAL2','Japan Cargo','Japan','+81 3 5460 2222','cargo@jal.com','Active'),('KAL','Korean Air','South Korea','+82 2 1588 2001','info@koreanair.com','Active'),('PAS','Pacific Airlines','Vietnam','19009999','support@pacificairlines.com','Active'),('QTR','Qatar Airways','Qatar','+974 4023 0000','info@qatarairways.com','Active'),('QTR2','Qatar Cargo','Qatar','+974 4023 1111','cargo@qatarairways.com','Active'),('SIA','Singapore Airlines','Singapore','+65 6223 8888','contact@singaporeair.com','Active'),('SIA2','Singapore Cargo','Singapore','+65 6542 8888','cargo@singaporeair.com','Active'),('THY','Turkish Airlines','Turkey','+90 212 444 0849','info@thy.com','Active'),('VAS','VASCO','Vietnam','19009988','info@vasco.com.vn','Active'),('VJC','VietJet Air','Vietnam','19001886','support@vietjetair.com','Active'),('VJC2','VietJet Cargo','Vietnam','19001887','cargo@vietjetair.com','Active'),('VNA','Vietnam Airlines','Vietnam','19005566','info@vietnamairlines.com','Active'),('VNA2','Vietnam Airlines Cargo','Vietnam','19005567','cargo@vietnamairlines.com','Active'),('VRA','Vietravel Airlines','Vietnam','19001899','info@vietravelairlines.com','Active');
/*!40000 ALTER TABLE `hang_hang_khong` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hanh_khach`
--

DROP TABLE IF EXISTS `hanh_khach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hanh_khach` (
  `MaHanhKhach` varchar(15) NOT NULL,
  `HoTen` varchar(100) NOT NULL,
  `NgaySinh` date DEFAULT NULL,
  `GioiTinh` enum('Nam','Nu','Khac') DEFAULT NULL,
  `CCCD` varchar(20) DEFAULT NULL,
  `SoDienThoai` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `DiaChi` varchar(255) DEFAULT NULL,
  `TrangThai` enum('Active','Banned','Inactive') DEFAULT 'Active',
  `NgayCam` date DEFAULT NULL,
  `NgayHetCam` date DEFAULT NULL,
  `LyDoCam` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`MaHanhKhach`),
  UNIQUE KEY `CCCD` (`CCCD`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hanh_khach`
--

LOCK TABLES `hanh_khach` WRITE;
/*!40000 ALTER TABLE `hanh_khach` DISABLE KEYS */;
INSERT INTO `hanh_khach` VALUES ('HK00001','Nguyễn Văn An','1995-03-15','Nam','012345678901','0987123456','an.nguyen@email.com','Hà Nội','Active',NULL,NULL,NULL),('HK00002','Trần Thị Bình','1998-07-22','Nu','098765432109','0912345678','binh.tran@email.com','TP. Hồ Chí Minh','Active',NULL,NULL,NULL),('HK00003','Lê Minh Cường','1990-11-05','Nam','112233445566','0978123456','cuong.le@email.com','Đà Nẵng','Active',NULL,NULL,NULL),('HK00004','Phạm Thị Dung','2000-01-30','Nu','223344556677','0934567890','dung.pham@email.com','Hải Phòng','Active',NULL,NULL,NULL),('HK00005','Hoàng Văn Em','1988-09-12','Nam','334455667788','0967123456','em.hoang@email.com','Nha Trang','Active',NULL,NULL,NULL),('HK00006','Vũ Thị Hoa','1997-04-18','Nu','445566778899','0945123456','hoa.vu@email.com','Phú Quốc','Active',NULL,NULL,NULL),('HK00007','Đặng Minh Giang','1993-06-25','Nam','556677889900','0918123456','giang.dang@email.com','Huế','Active',NULL,NULL,NULL),('HK00008','Bùi Thị Hương','1999-12-10','Nu','667788990011','0989123456','huong.bui@email.com','Đà Lạt','Active',NULL,NULL,NULL),('HK00009','Phan Văn I','1992-02-28','Nam','778899001122','0973123456','i.phan@email.com','Hà Nội','Active',NULL,NULL,NULL),('HK00010','Ngô Thị Kim','1996-08-14','Nu','889900112233','0938123456','kim.ngo@email.com','TP. Hồ Chí Minh','Active',NULL,NULL,NULL),('HK00011','Trần Văn Long','1985-05-20','Nam','990011223344','0965123456','long.tran@email.com','Đà Nẵng','Active',NULL,NULL,NULL),('HK00012','Lê Thị Mai','2001-10-03','Nu','001122334455','0947123456','mai.le@email.com','Hải Phòng','Active',NULL,NULL,NULL),('HK00013','Nguyễn Minh Nam','1994-07-09','Nam','112233445577','0919123456','nam.nguyen@email.com','Nha Trang','Active',NULL,NULL,NULL),('HK00014','Phạm Thị Oanh','1997-03-27','Nu','223344556688','0983123456','oanh.pham@email.com','Phú Quốc','Active',NULL,NULL,NULL),('HK00015','Hoàng Văn Phong','1989-11-16','Nam','334455667799','0976123456','phong.hoang@email.com','Huế','Active',NULL,NULL,NULL),('HK00016','Vũ Thị Quỳnh','2002-01-05','Nu','445566778800','0932123456','quynh.vu@email.com','Đà Lạt','Active',NULL,NULL,NULL),('HK00017','Đặng Văn Sơn','1991-09-30','Nam','556677889911','0968123456','son.dang@email.com','Hà Nội','Active',NULL,NULL,NULL),('HK00018','Bùi Thị Thanh','1998-06-12','Nu','667788990022','0949123456','thanh.bui@email.com','TP. Hồ Chí Minh','Active',NULL,NULL,NULL),('HK00019','Phan Văn Uy','1995-04-22','Nam','778899001133','0917123456','uy.phan@email.com','Đà Nẵng','Active',NULL,NULL,NULL),('HK00020','Ngô Thị Vân','2000-08-08','Nu','889900112244','0982123456','van.ngo@email.com','Hải Phòng','Active',NULL,NULL,NULL);
/*!40000 ALTER TABLE `hanh_khach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lich_chuyen_bay`
--

DROP TABLE IF EXISTS `lich_chuyen_bay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lich_chuyen_bay` (
  `MaLichBay` int NOT NULL AUTO_INCREMENT,
  `MaChuyenBay` varchar(10) NOT NULL,
  `NgayBay` date NOT NULL,
  `GioKhoiHanh` time NOT NULL,
  `GioDenDuKien` time NOT NULL,
  `MaMayBay` varchar(20) NOT NULL,
  `MaCuaBay` varchar(10) NOT NULL,
  `TrangThai` enum('Scheduled','Delayed','Departed','Arrived','Cancelled','Inactive') DEFAULT 'Scheduled',
  PRIMARY KEY (`MaLichBay`),
  KEY `MaChuyenBay` (`MaChuyenBay`),
  KEY `MaMayBay` (`MaMayBay`),
  KEY `MaCuaBay` (`MaCuaBay`),
  CONSTRAINT `lich_chuyen_bay_ibfk_1` FOREIGN KEY (`MaChuyenBay`) REFERENCES `chuyen_bay` (`MaChuyenBay`),
  CONSTRAINT `lich_chuyen_bay_ibfk_2` FOREIGN KEY (`MaMayBay`) REFERENCES `may_bay` (`MaMayBay`),
  CONSTRAINT `lich_chuyen_bay_ibfk_3` FOREIGN KEY (`MaCuaBay`) REFERENCES `cua_bay` (`MaCuaBay`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lich_chuyen_bay`
--

LOCK TABLES `lich_chuyen_bay` WRITE;
/*!40000 ALTER TABLE `lich_chuyen_bay` DISABLE KEYS */;
INSERT INTO `lich_chuyen_bay` VALUES (59,'VN123','2026-04-10','08:00:00','10:00:00','VN-A321','T1-A1','Scheduled'),(60,'VN224','2026-04-10','14:30:00','16:35:00','VN-B789','T1-A2','Delayed'),(61,'VJ456','2026-04-11','07:15:00','08:45:00','VJ-A320','T1-B3','Scheduled'),(62,'VJ789','2026-04-11','19:00:00','21:10:00','VJ-B738','T2-C5','Scheduled'),(63,'QH101','2026-04-12','09:30:00','11:20:00','QH-A321','T1-D7','Departed'),(64,'VU202','2026-04-12','15:45:00','18:00:00','VU-A320','SGN-12','Scheduled'),(65,'QR501','2026-04-13','23:00:00','11:00:00','QR-A380','T1-A1','Scheduled'),(66,'EK602','2026-04-13','02:30:00','13:30:00','EK-B777','SGN-25','Scheduled'),(67,'SQ701','2026-04-14','10:45:00','13:45:00','SQ-A350','T2-C5','Arrived'),(68,'JL802','2026-04-14','22:15:00','04:05:00','JL-B787','T1-A2','Scheduled'),(69,'VN305','2026-04-15','06:30:00','07:15:00','VN-A350','T1-B3','Scheduled'),(70,'VJ408','2026-04-15','12:00:00','13:20:00','VJ-A321','DAD-08','Cancelled'),(71,'QH509','2026-04-16','08:00:00','09:35:00','BAV-B787','T1-D7','Scheduled'),(72,'VN612','2026-04-16','16:20:00','17:55:00','VN-A321','SGN-12','Scheduled'),(73,'KE100','2026-04-17','11:00:00','15:00:00','KE-B777','T1-A1','Scheduled'),(74,'VN123','2026-04-18','08:00:00','10:00:00','VN-B789','T1-A2','Scheduled'),(75,'VJ456','2026-04-18','07:15:00','08:45:00','VJ-A320','T1-B3','Delayed'),(76,'QH101','2026-04-19','09:30:00','11:20:00','QH-A321','T1-D7','Scheduled'),(77,'VU202','2026-04-19','15:45:00','18:00:00','VU-A320','SGN-12','Scheduled');
/*!40000 ALTER TABLE `lich_chuyen_bay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `may_bay`
--

DROP TABLE IF EXISTS `may_bay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `may_bay` (
  `MaMayBay` varchar(20) NOT NULL,
  `LoaiMayBay` varchar(50) NOT NULL,
  `SucChua` int NOT NULL,
  `NamSanXuat` year DEFAULT NULL,
  `MaHang` varchar(10) NOT NULL,
  `TrangThai` enum('Active','Inactive') DEFAULT 'Active',
  PRIMARY KEY (`MaMayBay`),
  KEY `MaHang` (`MaHang`),
  CONSTRAINT `may_bay_ibfk_1` FOREIGN KEY (`MaHang`) REFERENCES `hang_hang_khong` (`MaHang`),
  CONSTRAINT `may_bay_chk_1` CHECK ((`SucChua` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `may_bay`
--

LOCK TABLES `may_bay` WRITE;
/*!40000 ALTER TABLE `may_bay` DISABLE KEYS */;
INSERT INTO `may_bay` VALUES ('AF-A350','Airbus A350',280,2021,'AFR','Active'),('BAV-B787','Boeing 787',289,2020,'BAV','Active'),('BL-A320','Airbus A320',180,2016,'PAS','Active'),('EK-B777','Boeing 777-300ER',354,2019,'EMA','Active'),('JL-B787','Boeing 787',264,2018,'JAL','Active'),('KE-B777','Boeing 777',300,2016,'KAL','Active'),('QH-A321','Airbus A321',220,2021,'BAV','Active'),('QR-A380','Airbus A380',489,2015,'QTR','Active'),('SQ-A350','Airbus A350',253,2020,'SIA','Active'),('VJ-A320','Airbus A320',180,2019,'VJC','Active'),('VJ-A321','Airbus A321',220,2023,'VJC','Active'),('VJ-B738','Boeing 737-800',189,2017,'VJC','Active'),('VN-A321','Airbus A321',220,2018,'VNA','Active'),('VN-A350','Airbus A350',305,2022,'VNA','Active'),('VN-B789','Boeing 787-9',300,2020,'VNA','Active'),('VU-A320','Airbus A320',180,2022,'VRA','Active');
/*!40000 ALTER TABLE `may_bay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhan_vien`
--

DROP TABLE IF EXISTS `nhan_vien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhan_vien` (
  `MaNhanVien` varchar(10) NOT NULL,
  `HoTen` varchar(100) NOT NULL,
  `NgaySinh` date DEFAULT NULL,
  `GioiTinh` enum('Nam','Nu') DEFAULT NULL,
  `SoDienThoai` varchar(15) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `ChucVu` enum('CoTruong','CoPho','TiepVien','NhanVienSanBay') NOT NULL,
  `BangCap` varchar(100) DEFAULT NULL,
  `MaHang` varchar(10) DEFAULT NULL,
  `TrangThai` enum('Active','Inactive') DEFAULT 'Active',
  PRIMARY KEY (`MaNhanVien`),
  KEY `MaHang` (`MaHang`),
  CONSTRAINT `nhan_vien_ibfk_1` FOREIGN KEY (`MaHang`) REFERENCES `hang_hang_khong` (`MaHang`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhan_vien`
--

LOCK TABLES `nhan_vien` WRITE;
/*!40000 ALTER TABLE `nhan_vien` DISABLE KEYS */;
INSERT INTO `nhan_vien` VALUES ('NV001','Nguyễn Văn A','1980-05-10','Nam','0912345678','a.nguyen@vna.com','CoTruong','ATPL','VNA','Active'),('NV002','Trần Thị B','1985-12-15','Nu','0987654321','b.tran@vna.com','CoPho','CPL','VNA','Active'),('NV003','Lê Văn C','1978-03-20','Nam','0978123456','c.le@vjc.com','CoTruong','ATPL','VJC','Active'),('NV004','Phạm Thị D','1990-07-25','Nu','0934567890','d.pham@vjc.com','TiepVien','Cabin Crew','VJC','Active'),('NV005','Hoàng Văn E','1982-11-05','Nam','0967123456','e.hoang@bav.com','CoTruong','ATPL','BAV','Active'),('NV006','Vũ Thị F','1995-09-12','Nu','0945123456','f.vu@bav.com','TiepVien','Cabin Crew','BAV','Active'),('NV007','Đặng Văn G','1987-01-30','Nam','0918123456','g.dang@vra.com','CoPho','CPL','VRA','Active'),('NV008','Bùi Thị H','1992-06-18','Nu','0989123456','h.bui@qtr.com','TiepVien','Cabin Crew','QTR','Active'),('NV009','Phan Văn I','1979-04-22','Nam','0973123456','i.phan@ema.com','CoTruong','ATPL','EMA','Active'),('NV010','Ngô Thị K','1993-08-14','Nu','0938123456','k.ngo@sia.com','TiepVien','Cabin Crew','SIA','Active'),('NV011','Trần Văn L','1984-02-28','Nam','0965123456','l.tran@jal.com','CoPho','CPL','JAL','Active'),('NV012','Lê Thị M','1996-10-03','Nu','0947123456','m.le@thy.com','TiepVien','Cabin Crew','THY','Active'),('NV013','Nguyễn Minh N','1981-07-09','Nam','0919123456','n.nguyen@kal.com','CoTruong','ATPL','KAL','Active'),('NV014','Phạm Thị O','1994-03-27','Nu','0983123456','o.pham@afr.com','TiepVien','Cabin Crew','AFR','Active'),('NV015','Hoàng Văn P','1986-11-16','Nam','0976123456','p.hoang@vna.com','CoPho','CPL','VNA','Active'),('NV016','Vũ Thị Q','1997-01-05','Nu','0932123456','q.vu@vjc.com','TiepVien','Cabin Crew','VJC','Active'),('NV017','Đặng Văn R','1983-09-30','Nam','0968123456','r.dang@bav.com','CoTruong','ATPL','BAV','Active'),('NV018','Bùi Thị S','1991-06-12','Nu','0949123456','s.bui@vra.com','TiepVien','Cabin Crew','VRA','Active'),('NV019','Phan Văn T','1989-04-22','Nam','0917123456','t.phan@qtr.com','CoPho','CPL','QTR','Active'),('NV020','Ngô Thị U','1998-08-08','Nu','0982123456','u.ngo@ema.com','TiepVien','Cabin Crew','EMA','Active');
/*!40000 ALTER TABLE `nhan_vien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phan_cong_chuyen_bay`
--

DROP TABLE IF EXISTS `phan_cong_chuyen_bay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phan_cong_chuyen_bay` (
  `MaPhanCong` int NOT NULL AUTO_INCREMENT,
  `MaNhanVien` varchar(10) NOT NULL,
  `MaLichBay` int NOT NULL,
  `VaiTro` varchar(50) DEFAULT NULL,
  `TrangThai` enum('Active','Inactive') DEFAULT 'Active',
  PRIMARY KEY (`MaPhanCong`),
  KEY `MaNhanVien` (`MaNhanVien`),
  KEY `MaLichBay` (`MaLichBay`),
  CONSTRAINT `phan_cong_chuyen_bay_ibfk_1` FOREIGN KEY (`MaNhanVien`) REFERENCES `nhan_vien` (`MaNhanVien`),
  CONSTRAINT `phan_cong_chuyen_bay_ibfk_2` FOREIGN KEY (`MaLichBay`) REFERENCES `lich_chuyen_bay` (`MaLichBay`)
) ENGINE=InnoDB AUTO_INCREMENT=91 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phan_cong_chuyen_bay`
--

LOCK TABLES `phan_cong_chuyen_bay` WRITE;
/*!40000 ALTER TABLE `phan_cong_chuyen_bay` DISABLE KEYS */;
INSERT INTO `phan_cong_chuyen_bay` VALUES (55,'NV001',59,'Cơ trưởng','Active'),(56,'NV002',59,'Cơ phó','Active'),(57,'NV004',59,'Tiếp viên chính','Active'),(58,'NV003',60,'Cơ trưởng','Active'),(59,'NV015',60,'Cơ phó','Active'),(60,'NV006',61,'Tiếp viên','Active'),(61,'NV005',62,'Cơ trưởng','Active'),(62,'NV016',62,'Tiếp viên chính','Active'),(63,'NV009',63,'Cơ trưởng','Active'),(64,'NV008',64,'Tiếp viên','Active'),(65,'NV013',65,'Cơ trưởng','Active'),(66,'NV011',66,'Cơ phó','Active'),(67,'NV010',67,'Tiếp viên chính','Active'),(68,'NV012',68,'Tiếp viên','Active'),(69,'NV017',69,'Cơ trưởng','Active'),(70,'NV018',70,'Tiếp viên','Active'),(71,'NV019',71,'Cơ phó','Active'),(72,'NV020',72,'Tiếp viên','Active'),(73,'NV001',59,'Cơ trưởng','Active'),(74,'NV002',59,'Cơ phó','Active'),(75,'NV004',59,'Tiếp viên chính','Active'),(76,'NV003',60,'Cơ trưởng','Active'),(77,'NV015',60,'Cơ phó','Active'),(78,'NV006',61,'Tiếp viên','Active'),(79,'NV005',62,'Cơ trưởng','Active'),(80,'NV016',62,'Tiếp viên chính','Active'),(81,'NV009',63,'Cơ trưởng','Active'),(82,'NV008',64,'Tiếp viên','Active'),(83,'NV013',65,'Cơ trưởng','Active'),(84,'NV011',66,'Cơ phó','Active'),(85,'NV010',67,'Tiếp viên chính','Active'),(86,'NV012',68,'Tiếp viên','Active'),(87,'NV017',69,'Cơ trưởng','Active'),(88,'NV018',70,'Tiếp viên','Active'),(89,'NV019',71,'Cơ phó','Active'),(90,'NV020',72,'Tiếp viên','Active');
/*!40000 ALTER TABLE `phan_cong_chuyen_bay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `san_bay`
--

DROP TABLE IF EXISTS `san_bay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `san_bay` (
  `MaSanBay` char(3) NOT NULL,
  `TenSanBay` varchar(100) NOT NULL,
  `ThanhPho` varchar(100) NOT NULL,
  `QuocGia` varchar(50) NOT NULL,
  `TrangThai` enum('Active','Inactive') DEFAULT 'Active',
  PRIMARY KEY (`MaSanBay`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `san_bay`
--

LOCK TABLES `san_bay` WRITE;
/*!40000 ALTER TABLE `san_bay` DISABLE KEYS */;
INSERT INTO `san_bay` VALUES ('BKK','Sân bay Suvarnabhumi','Bangkok','Thailand','Active'),('BMV','Sân bay Buôn Ma Thuột','Buôn Ma Thuột','Vietnam','Active'),('CDG','Sân bay Charles de Gaulle','Paris','France','Active'),('CXR','Sân bay Quốc tế Cam Ranh','Nha Trang','Vietnam','Active'),('DAD','Sân bay Quốc tế Đà Nẵng','Đà Nẵng','Vietnam','Active'),('DLI','Sân bay Liên Khương','Đà Lạt','Vietnam','Active'),('DXB','Sân bay Dubai','Dubai','UAE','Active'),('HAN','Sân bay Quốc tế Nội Bài','Hà Nội','Vietnam','Active'),('HPH','Sân bay Quốc tế Cát Bi','Hải Phòng','Vietnam','Active'),('HUI','Sân bay Phú Bài','Huế','Vietnam','Active'),('ICN','Sân bay Incheon','Seoul','South Korea','Active'),('IST','Sân bay Istanbul','Istanbul','Turkey','Active'),('NRT','Sân bay Narita','Tokyo','Japan','Active'),('PQC','Sân bay Quốc tế Phú Quốc','Phú Quốc','Vietnam','Active'),('SGN','Sân bay Quốc tế Tân Sơn Nhất','TP. Hồ Chí Minh','Vietnam','Active'),('SIN','Sân bay Changi','Singapore','Singapore','Active'),('VDO','Sân bay Quốc tế Vân Đồn','Quảng Ninh','Vietnam','Active');
/*!40000 ALTER TABLE `san_bay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ve`
--

DROP TABLE IF EXISTS `ve`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ve` (
  `MaVe` varchar(20) NOT NULL,
  `MaHanhKhach` varchar(15) NOT NULL,
  `MaLichBay` int NOT NULL,
  `SoGhe` varchar(10) DEFAULT NULL,
  `GiaVe` decimal(12,2) NOT NULL,
  `TrangThaiVe` enum('Booked','CheckedIn','Cancelled') DEFAULT 'Booked',
  `TrangThai` enum('Active','Inactive') DEFAULT 'Active',
  PRIMARY KEY (`MaVe`),
  KEY `MaHanhKhach` (`MaHanhKhach`),
  KEY `MaLichBay` (`MaLichBay`),
  CONSTRAINT `ve_ibfk_1` FOREIGN KEY (`MaHanhKhach`) REFERENCES `hanh_khach` (`MaHanhKhach`),
  CONSTRAINT `ve_ibfk_2` FOREIGN KEY (`MaLichBay`) REFERENCES `lich_chuyen_bay` (`MaLichBay`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ve`
--

LOCK TABLES `ve` WRITE;
/*!40000 ALTER TABLE `ve` DISABLE KEYS */;
INSERT INTO `ve` VALUES ('VE00001','HK00001',59,'12A',1850000.00,'Booked','Active'),('VE00002','HK00002',60,'15B',2100000.00,'CheckedIn','Active'),('VE00003','HK00003',61,'08C',1350000.00,'Booked','Active'),('VE00004','HK00004',62,'22D',1650000.00,'Booked','Active'),('VE00005','HK00005',63,'30E',2450000.00,'Cancelled','Active'),('VE00006','HK00006',64,'10F',3200000.00,'Booked','Active'),('VE00007','HK00007',65,'05A',12500000.00,'CheckedIn','Active'),('VE00008','HK00008',66,'18B',9800000.00,'Booked','Active'),('VE00009','HK00009',67,'25C',4500000.00,'Booked','Active'),('VE00010','HK00010',68,'14D',6800000.00,'CheckedIn','Active'),('VE00011','HK00011',69,'07E',950000.00,'Booked','Active'),('VE00012','HK00012',70,'19F',1200000.00,'Cancelled','Active'),('VE00013','HK00013',71,'11A',850000.00,'Booked','Active'),('VE00014','HK00014',72,'23B',1750000.00,'Booked','Active'),('VE00015','HK00015',73,'28C',5200000.00,'CheckedIn','Active'),('VE00016','HK00016',74,'09D',1450000.00,'Booked','Active'),('VE00017','HK00017',75,'16E',2100000.00,'Booked','Active'),('VE00018','HK00018',76,'20F',1350000.00,'CheckedIn','Active'),('VE00019','HK00019',59,'13A',980000.00,'Booked','Active'),('VE00020','HK00020',60,'25D',1950000.00,'Booked','Active');
/*!40000 ALTER TABLE `ve` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'baitaplondb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-25 21:10:32
