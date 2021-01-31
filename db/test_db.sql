

use Hydrogrid;
go



select x.* from [dbo].[url_map] x;



select x.* from [dbo].[Setting] x order by [Setting_Code];
select x.* from [dbo].[Setting_ValidyTimeframe] x order by [Setting_Code];




/*
begin transaction
insert into [dbo].[url_map] ([url_original], [url_shortened_code], [expiration_time]) output inserted.* values (N'http://www.google.com', N'xxx', getdate()+convert(int, N'3'));
commit transaction

begin transaction
delete from [dbo].[url_map] output deleted.* where [url_shortened_code] = N'xxx'
commit transaction
*/





/*
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
*/



select x.* from [dbo].[url_map] x;



-- truncate table [dbo].[url_map];


