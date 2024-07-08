import os
import psycopg2 # type: ignore
# import psycopg2.extras

password = os.getenv("POSTGRESQL_PASSWORD")
conn = None
cur = None

try: 
        conn = psycopg2.connect(
            host = 'localhost',
            dbname = 'Banking',
            user = 'postgres',
            password = password,
            port = 5432
    )
        
        cur = conn.cursor()
        
        our_script = """CREATE TABLE IF NOT EXISTS BankingThree (
		"ID" INTEGER,
                "NAME" VARCHAR(50),
                "Age" INTEGER,
		"SEX" CHAR(1),
		"Balance" INTEGER
        )"""
        
        cur.execute(our_script)
        
        conn.commit()
        
except Exception as e:
        print(f"Error: {e}")

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


