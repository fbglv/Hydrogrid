from sqlalchemy import create_engine
from datetime import datetime
from random import seed, random


class DbManager:  
    db = None


    def connect_db(self):
        db_string = "mssql+pymssql://sa:1234qwerASDF@hydrogrid_db/Hydrogrid?charset=utf8"
        self.db = create_engine(db_string, isolation_level = "AUTOCOMMIT")
        # global db = create_engine(db_string)
        if self.db is not None:
            print("Connected to the database.")
        else:
            print("Connection attempt to the database unsuccessful.")

    
    """
    def init_db(self):          
        # db.execute("CREATE TABLE IF NOT EXISTS...")    
    """

   
    def add_url_shrtn(self, url_original_protocol, url_original_domain, expiration_days):
        print("\n\n\n\n\nurl_original: "+str(url_original_protocol) + "; url_original_domain: " + str(url_original_domain) + "; expiration_days: " + str(expiration_days)) # DEBUG

        url_original = url_original_protocol + '://' + url_original_domain
        seed(1)
        url_shrtn = str(abs(hash(url_original+str(datetime.now())+str(random()))))

        res = self.db.execute("insert into [dbo].[url_map] ([url_original], [url_shortened_code], [expiration_time]) output inserted.* values (%s, %s, getdate()+convert(int, %s));", url_original, url_shrtn, expiration_days)  
        res_dict = []
        for i in res:
            res_dict.append({"status": "OK", "url_shrtn": i['url_shortened']}) 

        if len(res_dict) < 1:
            res_dict = []
            res_dict.append({"status": "GENERIC_DATABASE_ERROR"})

        return res_dict[0]



    def del_url_shrtn(self, url_shortened_code):
        print("\n\n\nurl_shortened_code: "+str(url_shortened_code)) # DEBUG

        res = self.db.execute("delete from [dbo].[url_map] output deleted.* where [url_shortened_code] = %s;", url_shortened_code)
        res_dict = []
        for i in res:
            if i['active'] == True:
                res_status = "OK_DELETED"
            else:
                res_status = "OK_URLSHRTN_ALREADY_INACTIVE"
            print("LOOP_STATUS") # DEBUG
            res_dict.append({"status": res_status, "url_shrtn_code": i['url_shortened_code'], "active": str(i['active'])})

        print(res_dict) # DEBUG

        if len(res_dict) < 1:
            res_dict = []
            res_dict.append({"status": "ERROR_URLSHRTN_NOT_FOUND", "url_shrtn_code": str(url_shortened_code)})

        return res_dict[0]



    def get_url_shrtn(self, url_shrt_code):  
        res = self.db.execute("select top 1 x.[url_shortened], x.[url_shortened_code], x.[url_original], x.[expiration_time_str] as [expiration_time], x.[active] from dbo.url_map x where [url_shortened_code] = %s", url_shrt_code)
        res_dict = []
        for i in res:
            res_dict.append({"status": "OK", "url_shortened": i[0], "url_shortened_code": i[1], "url_original": i[2], "expiration_time": i[3], "active": i[4]})
        # print("ROW COUNT: " + str(len(res_dict)))
        if len(res_dict) < 1:
            # print("NO RESULT")
            res_dict.append({"status": "ERROR_NO_URL_STORED"})
        elif res_dict[0]['active'] == False:
            # print("ACTIVE: " + str(res_dict[0]['active']))
            # print("DATA TYPE: " + str(type(res_dict[0]['active'])))
            res_dict = []
            res_dict.append({"status": "ERROR_URL_NOT_ACTIVE"})               

        return res_dict[0] 

    """
    def get_url_shrtn(self, url_original):  
    res = self.db.execute("select top 1 x.[url_shortened], x.[url_original], x.[expiration_time], x.[active] from dbo.url_map x where [url_original] = %s", url_original)
    res_dict = []
    for i in res:
        res_dict.append({"url_shortened": i[0], "url_original": i[1], "expiration_time": i[2], "active": i[3]})
    return res_dict[0]
    """



    def get_url_orig(self, url_shortened_code):  
        res = self.db.execute("select top 1 x.[url_original], x.[url_shortened], x.[url_shortened_code], x.[active] from dbo.url_map x where [url_shortened_code] = %s", url_shortened_code)
        res_dict = []
        for i in res:
            res_dict.append({"status": "OK", "url_original": i[0], "url_shortened": i[1], "active": i[3]})

        if len(res_dict) < 1:
            res_dict.append({"status": "ERROR_NO_URLSHRTN_STORED"})
        elif res_dict[0]['active'] == False:
            res_dict = []
            res_dict.append({"status": "ERROR_URL_NOT_ACTIVE"})

        return res_dict[0]




"""
dbmgr = DbManager()  
dbmgr.connect_db()
#dbmgr.init_db()  
"""

"""
url_shrtn = dbmgr.get_url_shrtn("https://www.repubblica.it")
print (type(url_shrtn))
for i in url_shrtn:
    print("Shortened URL: " + str(i[0]) + "; original URL: " + str(i[1]))
"""

"""
match_name = input("Name: ")
match_partner_name = input("Partner Name: ")
dbmgr.add_match(match_name, match_partner_name)  
"""