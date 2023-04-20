#  import libs
import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name 
    url = params.url
    
    csv_name = 'data.csv'

    os.system(f"wget {url} -O {csv_name}")

    #  Create and connect engine to postgres DB
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    #  Create iterator to chunk data to DB
    df_iter = pd.read_csv(csv_name,
                        compression='gzip',
                        parse_dates=["tpep_pickup_datetime","tpep_dropoff_datetime"],
                        iterator=True, 
                        chunksize=100000)
    
    #  Create DataFrame to get column names
    df = next(df_iter)

    #  Add column names
    df.head(0).to_sql(name=table_name,con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df.to_sql(name=table_name,con=engine, if_exists='append')
            t_end = time()
            print('another chunk inserted in {:.3f} second'.format(t_end - t_start))
        except StopIteration:
            print('Finished insertion')
            break

if __name__ == '__main__':
#  Create argparser

#  arguments: 
#  user
#  password
#  host
#  port
#  database name
#  table name
#  url of the csv

    parser = argparse.ArgumentParser(description='Ingest data from csv file to postgres DB')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for DB')
    parser.add_argument('--port', help='port for DB')
    parser.add_argument('--db', help='DB name')
    parser.add_argument('--table_name', help='table name inside DB')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)