import datetime
import pandas as pd
import os
from pathlib import Path

for filename in os.listdir('card-prices-data-lake/mtg-daily-prices'):
    name, extension = filename.split('.')
    file_date = datetime.datetime.strptime(name.split('_')[1], '%Y-%m-%d')
    magic_file = Path(f'./output/year={file_date.year}/month={file_date.month}/{file_date.day}.parquet')
    os.makedirs(f'./output/year={file_date.year}/month={file_date.month}', exist_ok=True)
    if magic_file.is_file() and magic_file.exists():
        print(f'{name}.parquet exists, skipping...')
    elif extension == 'csv':
        if filename == 'prices_2025-06-14.parquet':
            continue
        df = pd.read_csv(f'./card-prices-data-lake/mtg-daily-prices/{filename}', header=None)
        df.columns = ["oracle_id", "name", "price"]
        df['timestamp'] = file_date
        df.to_parquet(f'./output/year={file_date.year}/month={file_date.month}/{file_date.day}.parquet')

