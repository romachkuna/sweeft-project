import requests
import json
import pandas as pd


def make_call_to_api(headers, url="https://api.opensea.io/api/v2/collections?chain=ethereum"):
    response = requests.get(url, headers=headers)
    return response


def save_response_to_json(response):
    if response.status_code == 200:
        data = response.json()
        with open("opensea_response.json", "w") as f:
            json.dump(data, f, indent=4)
        print("JSON response saved to 'opensea_response.json'")
    else:
        print(f"Error: {response.status_code}")


def save_response_to_pandas_df(response, path='collections'):
    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data, record_path=[path])
        return df
    else:
        print(f"Error creating data frame:{response.status_code}")
        return None


def construct_df_from_json(json_path='opensea_response.json', normalize_on='collections'):
    df = pd.read_json(json_path)
    df_normalized = pd.json_normalize(df[normalize_on])
    return df_normalized


def save_df_to_json(df):
    df.to_json("data.json", orient='records')


def drop_unnecessary_columns(df, columns):
    # ["collection","name","twitter_username","contracts","description","owner","image_url"]
    df.filter(columns, axis=1)


def replace_all_whitespace(df):
    df.replace('', 'NOT FOUND', inplace=True)
