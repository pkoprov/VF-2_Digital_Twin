import psycopg2 as pg
import config
import pandas as pd

# get configs
db = config.db_name
user = config.user
password = config.password

# Connect to DataBase
conn = pg.connect(f"host = 10.76.152.200 port = 5432 dbname={db} user={user} password={password}")


def get_coords():
    try:
        query = f'SELECT * FROM public."VF-2_1" order by "Year, month, day" desc, "Power-on Time (total)" desc limit 1'
        df = pd.read_sql_query(query, conn)
        xposition_machine = float(df['Present machine coordinate position X'].tolist()[0])
        yposition_machine = float(df['Present machine coordinate position Y'].tolist()[0])
        zposition_machine = float(df['Present machine coordinate position Z'].tolist()[0])
    except:
        print('Query Failed')
    return xposition_machine, yposition_machine, zposition_machine


