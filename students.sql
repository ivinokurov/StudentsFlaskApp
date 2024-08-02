USE Students

GO -- Создание таблицы Department
CREATE TABLE dbo.Department (
	id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	name nvarchar(100) NOT NULL
) 

GO -- Создание таблицы StudentGroup
CREATE TABLE dbo.StudentGroup (
	id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	name nvarchar (15) NOT NULL,
chief int NULL FOREIGN KEY REFERENCES dbo.Student (id),
	deptId int NOT NULL FOREIGN KEY REFERENCES dbo.Department (id) 
ON UPDATE CASCADE ON DELETE CASCADE 
)

GO -- Создание таблицы Student
CREATE TABLE dbo.Student (
	id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	name nvarchar (50) NOT NULL,
	phone nvarchar (50) NULL,
	card nvarchar (15) NOT NULL,
	groupId int NOT NULL FOREIGN KEY REFERENCES dbo.StudentGroup (id)
ON UPDATE CASCADE ON DELETE CASCADE
)

GO -- Создание таблицы User
CREATE TABLE dbo.User (
	id int IDENTITY(1,1) NOT NULL PRIMARY KEY,
	username nvarchar (50) NOT NULL,
	password nvarchar (max) NOT NULL,
	role nvarchar (20) NOT NULL CHECK (role IN (‘admin’, ‘user’))
)
