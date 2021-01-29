
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
	[url_shortened_code] nvarchar(20),
	[url_shortened] as N'http://127.0.0.1:8080/teleport/' + [url_shortened_code],
	[expiration_time] datetime null default (getdate()+3),
	[expiration_time_str] as trim(str(year([expiration_time]))) + '-' + right(replicate('0',1)+trim(str(month([expiration_time]))),2) + '-' + right(replicate('0',1)+trim(str(day([expiration_time]))),2) + ' ' + right(replicate('0',1)+trim(str(datepart(HOUR,[expiration_time]))),2) + ':' + right(replicate('0',1)+trim(str(datepart(MINUTE,[expiration_time]))),2) + ':' + right(replicate('0',1)+trim(str(datepart(SECOND,[expiration_time]))),2),
	[active] as convert(bit, iif([expiration_time] > getdate(), 'TRUE', 'FALSE'))   
)
go


alter table url_map add constraint pk_url_map primary key clustered(ID);
go


create unique index ux_url_map_url_shrtn on dbo.url_map([url_shortened_code]);
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