import sqlite3, time
class SQLite():
    def __init__(self,name):
        self.name = name
    def connect(self):
        self.conn = sqlite3.connect(self.name)
    def cursor(self):
        self.cur = self.conn.cursor()
    def create(self,item,id,statement):
        currtime = time.strftime("%Y%m%d%H%M", time.localtime())
        tablename = "'"+item+'-'+id+'-'+currtime+"'"
        self.cur.execute('CREATE TABLE {0}{1};'.format(tablename,statement))
        # namelist = []
        # for x in range(len(statement.split(','))):
            # getname = ''
            # for index,str in enumerate(statement.split(',')[x]):
                # if '(' not in str and ')' not in str:
                    # getname = getname+str
            # for check in getname.split(' '):
                # if check is not '':
                    # namelist.append(check)
                    # break
        # self.ntuple = tuple(namelist)
        return tablename
    def insert(self,table,columns,values):
        for count in range(len(values)):
            self.cur.execute('INSERT INTO {0}{1} VALUES {2}'.format(table,columns,values[count]))
    def commit(self):
        self.conn.commit()
    def table(self):
        getlist = self.cur.execute("SELECT * FROM sqlite_master where type='table'")
        tablelist = []
        for list in getlist:
            tablelist.append(list)
        return tablelist
    def select(self,table):
        self.conn.total_changes
        values = self.cur.execute("SELECT *  from {0}".format(table))
        datalist = []
        for x in values:
           datalist.append(x)
        return datalist
    def getcolname(self,table):
        rowlist = []
        for row in self.cur.execute("PRAGMA table_info({})".format(table)):
            rowlist.append(row[1])
        return rowlist
    def close(self):
        self.conn.close()

# a = SQLite('C:/Users/nick/chart/sqlite/CODA4589')
# a.connect()
# a.cursor()
# a.getcolname("'PHY21-ABCDEFG-201710131159'")
# statement = '''(Frequency     INT    NOT NULL,\
       # MOD            TEXT   NOT NULL,\
       # REPORT         INT    NOT NULL,\
       # MEASURE        INT    NOT NULL,\
       # DELTA          INT    NOT NULL)'''
# name = a.create('PHY21',statement)
# value = [(330000000,'64QAM',33,30,3),(550000000,'256QAM',33,30,2.1),(750000000,'256QAM',23,30,8.1)]
# a.insert(name,('frequency','mod','report','measure','delta'),value)
# a.commit()
# a.select(name)

# a.create('PHY12',statement)
# value = [(10000000,'QPSK',33,30,3),(15000000,'QPSK',33,30,2.1),(20000000,'QPSK',23,30,8.1)]
# a.insert('PHY12',('frequency','mod','report','measure','delta'),value)
# a.commit()