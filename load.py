import psycopg2
import pandas as pd

conn = psycopg2.connect(database = "postgres",
                        user = "postgres",
                        host = "localhost",
                        password = "admin",
                        port = 5432)

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS dallas_shelters_(
            impound_id VARCHAR (15) PRIMARY KEY,
            animal_id VARCHAR (10) NOT NULL,
            breed VARCHAR (20) NOT NULL,
            intake_type VARCHAR (50) NOT NULL,
            intake_subtype VARCHAR (50) NOT NULL,
            intake_date DATE NOT NULL,
            intake_time TIME NOT NULL,
            intake_condition VARCHAR(60) NOT NULL,
            outcome VARCHAR (50) NOT NULL,
            outcome_date DATE,
            outcome_time TIME);
            """)
conn.commit()


df = pd.read_csv('Dallas_AS_2014-2024.csv', header=1)

for index, row in df.iterrows():
    insert_query = """INSERT INTO dallas_shelters_ (impound_id, animal_id, breed,intake_type,intake_subtype,intake_date,intake_time,
                                                    intake_condition,outcome,outcome_date,outcome_time)
                    VALUES (%s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s);"""
    values = list(row)
    cur.execute(insert_query, values)

conn.commit()
cur.close()
conn.close()