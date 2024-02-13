from database import SQL

sql = SQL()

cursor = sql.connection.cursor()

query = f'SELECT path from path WHERE domain="archive";'
cursor.execute(query)

path = cursor.fetchone()

print(path[0])