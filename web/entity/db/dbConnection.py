import psycopg2


def getConnection():
    try:
        return psycopg2.connect(
            host="psql",
            database="postgres",
            user="postgres",
            password="postgres",
            port='5432')

    except:
        return False

def isIdExists(table, field, value):
    conn = getConnection()
    curr = conn.cursor()
    curr.execute("SELECT 1 FROM "+table+" WHERE "+ field +" ='"+ str(value) +"'")
    data = curr.fetchall()
    curr.close()
    conn.close()
    return (len(data) != 0)

def isRelationExists(table, field, value, field2, value2):
    conn = getConnection()
    curr = conn.cursor()
    curr.execute(f"SELECT 1 FROM {table} WHERE {field} ='{value}' AND {field2} ='{value2}';")
    data = curr.fetchall()
    curr.close()
    conn.close()
    return (len(data) != 0)