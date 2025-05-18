CREATE SCHEMA `blood_donation` ;
USE `blood_donation`;

DROP TABLE IF EXISTS DonorInfo;
DROP TABLE IF EXISTS Donors;
DROP TABLE IF EXISTS BloodTypes;

CREATE TABLE BloodTypes (
    BloodTypeID VARCHAR(4) PRIMARY KEY,
    BloodType VARCHAR(3) NOT NULL
);

INSERT INTO BloodTypes (BloodTypeID, BloodType) VALUES
('B001', 'A+'),
('B002', 'A-'),
('B003', 'B+'),
('B004', 'B-'),
('B005', 'AB+'),
('B006', 'AB-'),
('B007', 'O+'),
('B008', 'O-');

CREATE TABLE Donors (
    DonorID VARCHAR(4) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    BloodTypeID VARCHAR(4),
    FOREIGN KEY (BloodTypeID) REFERENCES BloodTypes(BloodTypeID)
);

INSERT INTO Donors (DonorID, Name, BloodTypeID) VALUES
('D001', 'Maria Santos', 'B001'),
('D002', 'John Cruz', 'B002'),
('D003', 'Angela Reyes', 'B003'),
('D004', 'Carlos Dela Peña', 'B004'),
('D005', 'Luisa Tan', 'B005'),
('D006', 'Mark Villanueva', 'B006'),
('D007', 'Jasmine Lim', 'B007'),
('D008', 'Paolo Ramirez', 'B008'),
('D009', 'Ella Navarro', 'B001'),
('D010', 'Kevin Gomez', 'B003'),
('D011', 'Sofia Ramos', 'B005'),
('D012', 'Miguel Torres', 'B007'),
('D013', 'Bianca Yu', 'B004'),
('D014', 'Lorenzo Silva', 'B006'),
('D015', 'Nicole David', 'B002');

CREATE TABLE DonorInfo (
    DonorID VARCHAR(4) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Age INT NOT NULL,
    DateOfBirth DATE NOT NULL,
    FirstTimeDonor ENUM('Yes', 'No') NOT NULL,
    FOREIGN KEY (DonorID) REFERENCES Donors(DonorID)
);

INSERT INTO DonorInfo (DonorID, Name, Age, DateOfBirth, FirstTimeDonor) VALUES
('D001', 'Maria Santos', 28, '1997-03-15', 'Yes'),
('D002', 'John Cruz', 35, '1989-06-02', 'No'),
('D003', 'Angela Reyes', 22, '2003-08-21', 'Yes'),
('D004', 'Carlos Peña', 31, '1994-12-10', 'No'),
('D005', 'Luisa Tan', 26, '1998-02-05', 'Yes'),
('D006', 'Mark Villanueva', 40, '1985-11-09', 'No'),
('D007', 'Jasmine Lim', 24, '2001-01-20', 'Yes'),
('D008', 'Paolo Ramirez', 29, '1995-04-30', 'No'),
('D009', 'Ella Navarro', 27, '1997-07-17', 'Yes'),
('D010', 'Kevin Gomez', 33, '1992-10-13', 'No'),
('D011', 'Sofia Ramos', 21, '2004-09-12', 'Yes'),
('D012', 'Miguel Torres', 30, '1995-06-18', 'No'),
('D013', 'Bianca Yu', 23, '2002-05-25', 'Yes'),
('D014', 'Lorenzo Silva', 38, '1986-03-02', 'No'),
('D015', 'Nicole David', 25, '2000-08-04', 'Yes');

UPDATE DonorInfo
SET Name = 'Carlos Peña'
WHERE DonorID = 'D004';



    
    
DELETE FROM DonorInfo
WHERE DonorID = 'D005';

SELECT 
    d.DonorID,
    di.Name,
    bt.BloodType
FROM 
    Donors d
JOIN 
    DonorInfo di ON d.DonorID = di.DonorID
JOIN 
    BloodTypes bt ON d.BloodTypeID = bt.BloodTypeID
ORDER BY 
	d.DonorID;
