# DoAn_Python.NhomDoAn4.DH24TH2_Nhom2_To1
```sql
-- Bước 1: Tạo cơ sở dữ liệu
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'QuanLySach')
BEGIN
    CREATE DATABASE QuanLySach;
END;
GO

-- Bước 2: Sử dụng cơ sở dữ liệu vừa tạo
USE QuanLySach;
GO

-- Bảng 1: Lĩnh Vực (Ví dụ: Kinh tế, Văn học)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='LinhVuc' and xtype='U')
BEGIN
    CREATE TABLE LinhVuc (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        TenLinhVuc NVARCHAR(100) NOT NULL UNIQUE
    );
END;
GO

-- Bảng 2: Tác Giả
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='TacGia' and xtype='U')
BEGIN
    CREATE TABLE TacGia (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        TenTacGia NVARCHAR(100) NOT NULL UNIQUE,
        QuocTich NVARCHAR(50) NULL
    );
END;
GO

-- Bảng 3: Nhà Xuất Bản
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='NhaXuatBan' and xtype='U')
BEGIN
    CREATE TABLE NhaXuatBan (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        TenNXB NVARCHAR(150) NOT NULL UNIQUE,
        DiaChi NVARCHAR(255) NULL,
        SoDienThoai VARCHAR(20) NULL
    );
END;
GO

-- Bảng 4: Sách (Bảng chính)
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Sach' and xtype='U')
BEGIN
    CREATE TABLE Sach (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        MaSach VARCHAR(50) NOT NULL UNIQUE,
        TenSach NVARCHAR(255) NOT NULL,
        
        -- Khóa ngoại: Liên kết với TacGia
        IdTacGia INT,
        CONSTRAINT FK_Sach_TacGia FOREIGN KEY (IdTacGia) REFERENCES TacGia(Id),
        
        -- Khóa ngoại: Liên kết với LinhVuc
        IdLinhVuc INT,
        CONSTRAINT FK_Sach_LinhVuc FOREIGN KEY (IdLinhVuc) REFERENCES LinhVuc(Id),
        
        -- Khóa ngoại: Liên kết với NhaXuatBan
        IdNhaXuatBan INT,
        CONSTRAINT FK_Sach_NXB FOREIGN KEY (IdNhaXuatBan) REFERENCES NhaXuatBan(Id),

        LoaiSach NVARCHAR(50) NULL,
        GiaMua FLOAT NULL,
        GiaBia FLOAT NULL,
        LanTaiBan INT DEFAULT 0,
        NamXB VARCHAR(10) NULL
    );
END;
GO
```