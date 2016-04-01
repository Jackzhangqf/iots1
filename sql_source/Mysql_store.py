import torndb 

try: 
	db = torndb.Connection("127.0.0.1:3306", "test1_database",user="test1_jack",password="123")
except:
	print "This is a error"


cre = 'create table if not exists blog(id int, content text)'
db.execute(cre)
string1 = 'wawueeeeee'
exe = 'insert into blog(id , content)values(%d,"%s")'%(1,string1)
db.execute(exe)
