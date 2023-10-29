-- file: init_db.sql

CREATE DATABASE IF NOT EXISTS BeautySalesManagement;

USE BeautySalesManagement;

CREATE TABLE IF NOT EXISTS Inventory (
    ItemID INT AUTO_INCREMENT,
    ItemName VARCHAR(255) NOT NULL,
    Quantity INT NOT NULL,
    CostPrice DECIMAL(10, 2) NOT NULL,
    SellingPrice DECIMAL(10, 2) NOT NULL, -- New column for SellingPrice
    PRIMARY KEY (ItemID)
);

CREATE TABLE IF NOT EXISTS Sales (
    SaleID INT AUTO_INCREMENT,
    ItemID INT,
    QuantitySold INT NOT NULL,
    SellingPrice DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (SaleID)
);

CREATE TABLE IF NOT EXISTS Expenses (
    ExpenseID INT AUTO_INCREMENT,
    ExpenseType VARCHAR(255) NOT NULL,
    ExpenseAmount DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (ExpenseID)
);
