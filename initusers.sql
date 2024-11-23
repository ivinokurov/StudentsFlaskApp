DECLARE @admin nvarchar(50); 
SET @admin = 'admin1';
DECLARE @adminpwd nvarchar(max); 
SET @adminpwd = 'scrypt:32768:8:1$Va4XHHBg7eRbIHL5$a917dc951ae5ff6b267e60bdecdb43b4c69ee22120ef1736d47d0ee63f11a4be1ed3e288a9d5c640b05c6d616bfcef2c07162449a32aeba056476e27a8280b69';

DECLARE @user nvarchar(50); 
SET @user = 'user1';
DECLARE @userpwd nvarchar(max); 
SET @userpwd = 'scrypt:32768:8:1$WsKuL41tCbllLHEJ$0ca05618fab49f1de709efd3a8c14d8da5f1697ca7478e9b1f18b7e66f1eab9ece1b3937e3624b2dd5c905e700ecb50d70e3b708aee5ef24cc9dc44b28c30d1b';

INSERT INTO [User] VALUES (@admin, @adminpwd, 'admin')
INSERT INTO [User] VALUES (@user, @userpwd, 'user')