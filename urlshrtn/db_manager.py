from sqlalchemy import create_engine

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

    """
    def add_match(self, match_name, match_partner_name):
        self.db.execute("merge into dbo.matches as Tgt using (select %s as [name], %s as [partner_name]) as Src on (Tgt.[name] = Src.[name]) when matched then update set Tgt.[name] = Src.[name], Tgt.[partner_name] = Src.[partner_name] when not matched then insert ([name], [partner_name]) values (Src.[name], Src.[partner_name]);", match_name, match_partner_name)  
    """    
        
    def get_url_shrtn(self, url_original):  
        res = self.db.execute("select top 1 x.[url_shortened], x.[url_original], x.[expiration_time], x.[active] from dbo.url_map x where [url_original] = %s", url_original)
        res_dict = []
        for i in res:
            res_dict.append({"url_shortened": i[0], "url_original": i[1], "expiration_time": i[2], "active": i[3]})
        return res_dict[0]

    # DEBUG
    def get_url_shrtn_test(self, url_original, expiration_date):  
        res = self.db.execute("select top 1 x.[url_shortened], x.[url_original], x.[expiration_time_str] as [expiration_time], x.[active] from dbo.url_map x where [url_original] = %s", url_original)
        res_dict = []
        for i in res:
            res_dict.append({"status": "OK", "url_shortened": i[0], "url_original": i[1], "expiration_time": i[2], "active": i[3]})
        print("ROW COUNT: " + str(len(res_dict)))
        if len(res_dict) < 1:
            print("NO RESULT")
            res_dict.append({"status": "ERROR_NO_URL_STORED"})
        
        return res_dict[0] 

        """
        if res.rowcount < 0: # i.e. if no result is given
            return res_dict.append({"result": "NO_URL_STORED"})
        else:
            for i in res:
                res_dict.append({"url_shortened": i[0], "url_original": i[1], "expiration_time": i[2], "active": i[3]})
            # print("EXPIRATION_TIME: " + str(res_dict[0]['expiration_time']))
            return res_dict[0]        
        """


    def get_url_orig(self, url_shortened):  
        res = self.db.execute("select top 1 x.[url_original], x.[url_shortened], x.[active] from dbo.url_map x where [url_shortened] = %s", url_shortened)
        res_dict = []
        for i in res:
            res_dict.append({"url_original": i[0], "url_shortened": i[1], "active": i[2]})

        return res_dict[0]
        #
        # ADD EXCEPTION IN CASE URL IS NOT FOUND / NOT ACTIVE!
        # OR SIMPLY CHECK IN main.py for the [active] field
        #

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