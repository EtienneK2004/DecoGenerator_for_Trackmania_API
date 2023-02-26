import entity.db.dbConnection as db
import entity.Build as Build

def findByUuid(uuid):
    conn = db.getConnection()
    print("result findByUuid -> getConnection")
    curr = conn.cursor()
    curr.execute(f"""SELECT 
                    uuid,
                    account_id,
                    create_date,
                    finish_date,
                    status,
                    file_name
                 FROM build 
                 WHERE uuid = '{uuid}';
                 """)

    data = curr.fetchall()
    curr.close()
    conn.close()
    if(data):
        for row in data:
            print("row")
            print(row)
            build = Build.Build()
            build.initWithDB(row)
            return build

    return False


def findNextBuildByCreatedDate():
    conn = db.getConnection()
    print("result findNextBuildByCreatedDate -> getConnection")
    curr = conn.cursor()
    curr.execute(f"""SELECT 
                    uuid,
                    account_id,
                    create_date,
                    finish_date,
                    status,
                    file_name
                 FROM build 
                 WHERE status = 0
                 ORDER BY create_date
                 LIMIT 1;
                 """)

    data = curr.fetchall()
    curr.close()
    conn.close()
    if(data):
        for row in data:
            print("row")
            print(row)
            build = Build.Build()
            build.initWithDB(row)
            return build

    return False


def persist(build):
    if(db.isIdExists("build", "uuid", build.uuid)):
        print("UPDATE")
        query = f"""
            UPDATE build
                SET account_id = '{build.account_id}',
                    create_date = to_timestamp({build.create_date}),
                    finish_date = {("NULL" if build.finish_date == "" else f"to_timestamp({build.finish_date})")},
                    status = '{str(build.status)}',
                    file_name = '{build.file_name}'
            WHERE
                uuid = '{build.uuid}'
            ;
        """
    else:
        #insert
        print("INSERT")
        query = f"""
            INSERT INTO build
            (
                uuid,
                account_id,
                create_date,
                finish_date,
                status,
                file_name
            )
            VALUES
            (
                '{build.uuid}',
                '{build.account_id}',
                to_timestamp({build.create_date}),
                {("NULL" if build.finish_date == "" else f"to_timestamp({build.finish_date})")},
                '{str(build.status)}',
                '{build.file_name}'
            );
        """
        #to_timestamp({build.finish_date}),
    print("debug sql")
    print(query)
    conn = db.getConnection()
    curr = conn.cursor()
    curr.execute(query)
    conn.commit()
    curr.close()
    conn.close()



