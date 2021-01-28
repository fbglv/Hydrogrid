
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
    [url_original] nvarchar(255),
    [url_shortened] nvarchar(50),
	[expiration_time] datetime null default (getdate()+3),
	[active] as convert(bit, iif([expiration_time] > getdate(), 'TRUE', 'FALSE'))   
)
go


alter table url_map add constraint PK_url_map primary key clustered(ID);
go




/*
--
--	Full-Text Search must be enabled on SQL Server
--

select serverproperty('IsFullTextInstalled');
go


if not exists (select 1 from sys.fulltext_catalogs x where x.[name] = 'ft')
begin
	create fulltext catalog ft as default;
end
go

if not exists (select 1 from sys.fulltext_indexes x where x.[name] = 'PK_url_map') 
begin
	create fulltext index on [dbo].[url_map]([url_shortened])
	   key index PK_url_map
	   with stoplist = system;
end
go
*/