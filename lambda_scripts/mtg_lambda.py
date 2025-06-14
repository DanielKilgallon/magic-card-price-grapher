import urllib3
import json
import boto3
import io
# pandas and pyarrow imported into lambda using public resource arn
import pandas as pd

def get_card_data():
    http = urllib3.PoolManager()
    print('getting download uri...')
    card_url_data = http.request('GET', 'https://api.scryfall.com/bulk-data/oracle-cards')
    card_url_json = json.loads(card_url_data.data.decode('utf-8'))
    
    print('downloading json...')
    card_data_response = http.request('GET', card_url_json['download_uri'])
    card_data = json.loads(card_data_response.data.decode('utf-8'))
    output_data = []
    print('building list...')
    today = pandas.to_datetime('today').normalize()
    for card in card_data:
        price_value = card['prices']['usd']
        if not price_value:
            price_value = '0'
        output_data.append([card['oracle_id'], card['name'], str(price_value), today])
    return output_data

def lambda_handler(event, context):
    today = pandas.to_datetime('today').normalize()
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('card-prices-data-lake')
    card_data = get_card_data()
    filename = 'mtg-daily-prices/prices_' + today.strftime('%Y-%m-%d') + '.parquet'
    print('uploading file to s3...')
    parquet_output = io.BytesIO()
    pd.DataFrame(card_data, columns=['oracle_id', 'name', 'price', 'timestamp']).to_parquet(parquet_output)
    bucket.put_object(Key=filename, Body=parquet_output.getvalue())
    return {
        'statusCode': 200,
        'body': json.dumps(f'Created file in s3{filename}!')
    }
