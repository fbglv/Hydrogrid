
if db_id(N'Hydrogrid') is null
create database Hydrogrid
go


use Hydrogrid
go


if object_id(N'url_map','U') is not null drop table dbo.url_map
go 

create table url_map    
(
    ID int identity(1,1) not null,
    [original_url] nvarchar(255),
    [shortened_url] nvarchar(50),
	[expiration_date] datetime not null default (getdate()+3),
    primary key(ID)    
)
go


 -- add full text index