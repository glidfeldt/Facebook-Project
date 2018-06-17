import psycopg2
import psycopg2.extras
from psycopg2 import ProgrammingError

class Database():
    def __init__(self,name):
        self.connection = psycopg2.connect("host=localhost, dbname="+name)
        self.connection.autocommit=True
        self.cursor = self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor)

    def clearTables(self):
        tableList = ['participation', 'message', 'friends', 'conversation']
        for table in tableList:
            try:
                self.cursor.execute("DROP TABLE " + table)
            except ProgrammingError:
                pass
    def createTables(self):
        self.cursor.execute("CREATE TABLE friends(id int NOT NULL, name VARCHAR, PRIMARY KEY (id));")
        self.cursor.execute("CREATE TABLE conversation(id INTEGER NOT NULL, name VARCHAR, PRIMARY KEY(id));")
        self.cursor.execute("CREATE TABLE message(id int NOT NULL ,convID int, userID VARCHAR, time TIMESTAMP, message VARCHAR, PRIMARY KEY(id));")
        self.cursor.execute("CREATE TABLE participation(userid int, conversationID int, PRIMARY KEY(userid, conversationID))")

    def insert_entry(self, table, attributes, data):
        s='%s'
        length=len(attributes)
        if length==len(data):
            for i in range(0, length-1):
                s=s+', %s'
            att=', '.join(attributes)
            query= ("INSERT INTO "+table+"("+att+") VALUES("+s+");")
            self.cursor.execute(query, data)


def main():
    database=Database('template1')
    database.clearTables()
    database.createTables()


#main()