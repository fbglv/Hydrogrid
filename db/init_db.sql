
if db_id(N'Hydrogrid') is null
create database Hydrogrid
go


use Hydrogrid
go




--
--
--	TASK A (Url Shortener)
--
--



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



begin transaction

merge into [dbo].[url_map] as Tgt
using 
(
	select N'https://www.hydrogrid.eu' as [url_original], N'9631943045954765780' as [url_shortened_code], getdate()+3 as [expiration_time]
	union all select N'https://hydraulics.unibs.it/hydraulics' as [url_original], N'2675854229534319119' as [url_shortened_code], getdate()-10 as [expiration_time]
	union all select N'http://www.repubblica.it' as [url_original], N'2641603234708071700' as [url_shortened_code], getdate()+10 as [expiration_time]
	union all select N'https://www.corriere.it' as [url_original], N'8184027350677630900' as [url_shortened_code], getdate()+10 as [expiration_time]
	union all select N'https://open.online' as [url_original], N'9139048072246564113' as [url_shortened_code], getdate()+10 as [expiration_time]

) as Src on (Tgt.[url_shortened_code] = Src.[url_shortened_code]) 
when matched then update set
	Tgt.[url_original] = Src.[url_original],
	Tgt.[expiration_time] = coalesce(Src.[expiration_time], Tgt.[expiration_time], getdate()+3)
when not matched then insert ([url_original], [url_shortened_code], [expiration_time]) values (Src.[url_original], Src.[url_shortened_code], Src.[expiration_time])
;
commit transaction







/*
--
--	Full-Text Search must be enabled on SQL Server!
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






--
--
--	TASK B (Settings Database)
--
--




--	
--	Setting_Base
--



if object_id(N'Setting_Base','U') is not null drop table [dbo].[Setting_Base]
go 

create table [dbo].[Setting_Base]
(
	[ID] int identity(1,1) primary key, 
	[Setting_Code] nvarchar(10), -- unique index!
	[Setting_Type_ID] int,
	[Setting_Name] nvarchar(50),
	[Setting_Unit] varchar(10),
	[Setting_Value_Type] nvarchar(10),
	[Setting_Value] nvarchar(50) null
);

create unique index [UX_Setting_Base_Code] on [dbo].[Setting_Base]([Setting_Code]);

-- truncate table [dbo].[Setting_Base];



begin transaction

-- truncate table [dbo].[Setting_Base];

merge into [dbo].[Setting_Base] Tgt
using
(
	select
		[Setting_Code]			= 'PID078',
		[Setting_Name]			= 'Perform_Intraday_Redispatch',
		[Setting_Type_ID]		=  1,
		[Setting_Unit]			= 'MW',
		[Setting_Value_Type]	= 'BOOLEAN',
		[Setting_Value]			= 'TRUE'
	union all
	select
		[Setting_Code]			= 'PMX003',
		[Setting_Name]			= 'PMax',
		[Setting_Type_ID]		= 3,
		[Setting_Unit]			= 'MW',
		[Setting_Value_Type]	= 'NUMERICAL',
		[Setting_Value]			= '4.3'
	union all
	select
		[Setting_Code]			= 'TBBX07',
		[Setting_Name]			= 'BX_Turbine_Calibrate',
		[Setting_Type_ID]		= 3,
		[Setting_Unit]			= 'None',
		[Setting_Value_Type]	= 'DATE',
		[Setting_Value]			= '2021-03-17'
	union all
	select
		[Setting_Code]			= 'CTSL817',
		[Setting_Name]			= 'Customer_Calibration_PX_23',
		[Setting_Type_ID]		= 2,
		[Setting_Unit]			= 'None',
		[Setting_Value_Type]	= 'SELECTION',
		[Setting_Value]			= null
) Src on (Tgt.[Setting_Code] = Src.[Setting_Code])
when matched then update set
	Tgt.[Setting_Name] = Src.[Setting_Name],
	Tgt.[Setting_Type_ID] = Src.[Setting_Type_ID],
	Tgt.[Setting_Unit] = Src.[Setting_Unit],
	Tgt.[Setting_Value_Type] = Src.[Setting_Value_Type],
	Tgt.[Setting_Value] = Src.[Setting_Value]
when not matched then insert
(
	[Setting_Code],
	[Setting_Name],
	[Setting_Type_ID],
	[Setting_Unit],
	[Setting_Value_Type],
	[Setting_Value]
)
values
(
	Src.[Setting_Code],
	Src.[Setting_Name],
	Src.[Setting_Type_ID],
	Src.[Setting_Unit],
	Src.[Setting_Value_Type],
	Src.[Setting_Value]
);

commit transaction






--
--	Setting Type
--

if object_id(N'Setting_Type','U') is not null drop table [dbo].[Setting_Type]
go 


create table [dbo].[Setting_Type]
(
	[ID] int primary key not null,
	[Setting_Type_Parent_ID] int null,
	[Setting_Type_Name] nvarchar(50)
);


begin transaction

insert into [dbo].[Setting_Type]([ID],[Setting_Type_Parent_ID],[Setting_Type_Name])
select 1, null, N'Customer' union all select 2, 1, N'Plant' union all select 3, 2, 'Control_Unit';

commit transaction
go


-- select x.* from [dbo].[Setting_Type] x;




--
--	Setting Selection
--

if object_id(N'Setting_Selection','U') is not null drop table [dbo].[Setting_Selection]
go


create table [dbo].[Setting_Selection]
(
	[ID] int identity(1,1) primary key not null,
	[Setting_Base_ID] int null,
	[Setting_Selection_Value] nvarchar(50)
);


begin transaction

insert into [dbo].[Setting_Selection]([Setting_Base_ID],[Setting_Selection_Value])
select
	[Setting_Base_ID]			= sb.[ID],
	[Setting_Selection_Value]	= sl.[Setting_Selection_Value]
from
	(select x.[ID] from [dbo].[Setting_Base] x where x.[Setting_Code] = 'CTSL817' and x.[Setting_Value_Type] = 'SELECTION') sb
	cross join (select 'SMALL' as [Setting_Selection_Value] union all select 'MEDIUM' union all select 'LARGE') sl
;

commit transaction
go

-- select x.* from [dbo].[Setting_Selection] x;






--
--	Setting_ValidityFrame
--

if object_id(N'Setting_ValidyTimeframe','U') is not null drop table dbo.[Setting_ValidyTimeframe]
go 


create table [dbo].[Setting_ValidyTimeframe]
(
    [ID] int identity(1,1) primary key not null,

	[Setting_Code] nvarchar(10) null, -- FK TO SETTING_BASE!

	[From_Year] smallint null,
	[From_Month] smallint null,
	[From_Weekday] smallint null,
	[From_DayOfMonth] smallint null,
	[From_Hour] smallint null,

	[To_Year] smallint null,
	[To_Month] smallint null,
	[To_Weekday] smallint null,
	[To_DayOfMonth] smallint null,
	[To_Hour] smallint null,
)
go


begin transaction

-- truncate table [dbo].[Setting_ValidyTimeframe];

insert into [dbo].[Setting_ValidyTimeframe]
([Setting_Code], [From_Year], [From_Month], [From_Weekday], [From_DayOfMonth], [From_Hour], [To_Year], [To_Month], [To_Weekday], [To_DayOfMonth], [To_Hour])
values
('PID078', 2020, 8, null, 11, null, null, null, null, null, null), 
('PMX003', null, null, null, null, 6, null, null, null, null, 18),
('CTSL817', 2020, null, null, null, null, 2021, null, null, null, null),
('TBBX07', null, 8, null, 1, null, null, 8, null, 16, null),
('PID078', null, 8, null, 1, 9, null, 8, null, 16, 13),
('PMX003', null, 1, null, 1, null, null, 1, null, 31, null),
('PID078', null, 1, 4, null, null, null, 1, 7, null, null),
('PMX003', null, 1, 4, null, null, null, 1, 6, null, null),
('PMX003', null, null, 7, null, 14, null, null, 7, null, 14)
;

commit transaction


-- select x.* from [dbo].[Setting_ValidyTimeframe] x;
-- go








--
--	Setting
--



if object_id(N'Setting','V') is not null drop view [dbo].[Setting]
go


create view [dbo].[Setting] as
with rd as
(
	-- select convert(datetime, '2021-03-15 12:11:09') as [RfDt]
	select convert(datetime, getdate()) as [RfDt]
)
, svtf as
(
	select
		[Setting_Code]	= x.[Setting_Code],
		[RfDt]			= convert(date, x.[RfDt]),
		[Rf_Weekday]	= isnull(nullif((datepart(weekday, x.[RfDt])-1)%7,0),7),
		[Rf_Hour]		= datepart(hour, x.[RfDt]),

		[From_Dt]		= convert(date, str(x.[From_Year]) + right(replicate('0',1)+trim(str(x.[From_Month])),2) + right(replicate('0',1)+trim(str(x.[From_DayOfMonth])),2)),
		[From_Weekday]	= x.[From_Weekday],
		[From Hour]		= x.[From_Hour],

		[To_Dt]			= convert(date, str(x.[To_Year]) + right(replicate('0',1)+trim(str(x.[To_Month])),2) + right(replicate('0',1)+trim(str(x.[To_DayOfMonth])),2)),
		[To_Weekday]	= x.[To_Weekday],
		[To_Hour]		= x.[To_Hour]
	from
	(
		--
		--	Substitutes the empty entries in dbo.Setting_ValidyTimeframe with the corresponding one of the current datetime (reference datetime)
		--	The idea here is to check the current datetime (reference datetime) with the ones in the dbo.Setting_ValidyTimeframe
		--
		select
			x.[Setting_Code],
			rd.[RfDt],
		
			[From_Year]			= isnull(x.[From_Year], year(rd.[RfDt])),
			[From_Month]		= isnull(x.[From_Month], month(rd.[RfDt])),
			[From_DayOfMonth]	= isnull(x.[From_DayOfMonth], day(rd.[RfDt])),
			[From_Weekday]		= isnull(x.[From_Weekday], isnull(nullif((datepart(weekday, rd.[RfDt])-1)%7,0),7)),
			[From_Hour]			= isnull(x.[From_Hour], datepart(hour, rd.[RfDt])),

			[To_Year]			= isnull(x.[To_Year], year(rd.[RfDt])),
			[To_Month]			= isnull(x.[To_Month], month(rd.[RfDt])),
			[To_DayOfMonth]		= isnull(x.[To_DayOfMonth], day(rd.[RfDt])),
			[To_Weekday]		= isnull(x.[To_Weekday], isnull(nullif((datepart(weekday, rd.[RfDt])-1)%7,0),7)), -- in Europe the first day of the week is monday and not sunday...
			[To_Hour]			= isnull(x.[To_Hour], datepart(hour, rd.[RfDt]))
		from
			[dbo].[Setting_ValidyTimeframe] x
			cross join rd
	) x
)
select distinct
	sb.[Setting_Code],
	sb.[Setting_Name],
	[Setting_Type]		= st.[Setting_Type_Name],
	sb.[Setting_Unit],
	sb.[Setting_Value_Type],
	[Setting_Value]		=	
							case [Setting_Value_Type]
								when 'SELECTION' then sl.[Setting_Selection_Value]
								else  sb.[Setting_Value]
							end,

	[Active_YN] = case
		when
		(
			(x.[RfDt] >= x.[From_Dt] and x.[RfDt] <= x.[To_Dt]) -- is the current (reference) date between the date range (if present)?
			and (x.[Rf_Weekday] >= x.[From_Weekday] and x.[Rf_Weekday] <= x.[To_Weekday]) -- is the current (reference) weekday between the weekday range?
			and (x.[Rf_Hour] >= x.[From Hour] and x.[Rf_Hour] <= x.[To_Hour]) -- is the current (reference) hour between the hour range?
		)
		then	'Y'
		else	'N'
	end
	
	/*
	-- DEBUG
	[<---- ONLY FOR DEBUG PURPOSES ---->] = '                         ',
	 
	x.[From_Dt],
	x.[RfDt],
	x.[To_Dt],

	x.[From_Weekday],
	x.[Rf_Weekday],
	x.[To_Weekday],

	x.[From Hour],
	x.[Rf_Hour],
	x.[To_Hour]	
	*/

from
	[dbo].[Setting_Base] sb
	inner join svtf x on x.[Setting_Code] = sb.[Setting_Code]	
	inner join [dbo].[Setting_Type] st on st.[ID] = sb.[Setting_Type_ID]
	left outer join [dbo].[Setting_Selection] sl on 
		sb.[Setting_Value_Type] = 'SELECTION'
		and sl.[Setting_Base_ID] = sb.[ID]
;
go


-- select x.* from [dbo].[Setting] x;


