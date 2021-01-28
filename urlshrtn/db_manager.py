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
        # db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")    
    """

    def add_match(self, match_name, match_partner_name):   
        self.db.execute("merge into dbo.matches as Tgt using (select %s as [name], %s as [partner_name]) as Src on (Tgt.[name] = Src.[name]) when matched then update set Tgt.[name] = Src.[name], Tgt.[partner_name] = Src.[partner_name] when not matched then insert ([name], [partner_name]) values (Src.[name], Src.[partner_name]);", match_name, match_partner_name)  
        
        
    def get_matches(self):  
        return self.db.execute("select x.* from dbo.matches x")  
        


"""
dbmgr = DbManager()  
dbmgr.connect_db()
#dbmgr.init_db()  

match_name = input("Name: ")
match_partner_name = input("Partner Name: ")
dbmgr.add_match(match_name, match_partner_name)  

matches = dbmgr.get_matches()
# print (type(matches))
for i in matches:
        print("Name: " + str(i[0]) + "; Partner Name: " + str(i[1]))
"""