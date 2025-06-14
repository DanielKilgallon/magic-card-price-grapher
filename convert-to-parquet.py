import datetime
import pandas as pd
import os
from pathlib import Path

for filename in os.listdir('card-prices-data-lake/mtg-daily-prices'):
    name, extension = filename.split('.')
    magic_file = Path(f'./output/{name}.parquet')
    if magic_file.is_file() and magic_file.exists():
        print(f'{name}.parquet exists, skipping...')
    else:
        if filename == 'prices_2025-06-14.parquet':
            continue
        df = pd.read_csv(f'./card-prices-data-lake/mtg-daily-prices/{filename}', header=None)
        file_date = datetime.datetime.strptime(name.split('_')[1], '%Y-%m-%d')
        df.columns = ["oracle_id", "name", "price"]
        df['timestamp'] = file_date
        df.to_parquet(f'./output/{name}.parquet')
        file_path = Path(f'./card-prices-data-lake/mtg-daily-prices/{filename}')
        file_path.unlink()


