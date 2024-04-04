from utils import *
from orm import *

headers = {
    "accept": "application/json",
    "x-api-key": "74236956836e4336b836845ae04c25f6"
}
response = make_call_to_api(headers)

df = save_response_to_pandas_df(response)

df = drop_unnecessary_columns(df, ["collection", "name", "twitter_username", "contracts", "description", "owner",
                                   "image_url"])
replace_all_whitespace(df)
# save to json
save_df_to_json(df)

data = prepare_data_for_orm(df)
# initialize database
db = Database(
    host="localhost",
    user="root",
    password="romaroma",
    database="sweeft"
)
db.create_schema()

db.insert_data(data)

query_result = db.retrieve_table_data("collections", limit=10, LIKE=("name", '%Suika%'), order_by="id")
print(query_result)

# insert new dummy data
data = [
    {
        'collection': 'dummycollection',
        'name': 'dummy name',
        'description': 'this is a dummy data insertion',
        'image_url': 'NOT FOUND',
        'owner': '0xa4518367eb30f0017f791763a98c6bd4b11e6a2c',
        'twitter_username': 'NOT FOUND',
        'contracts': [{'address': 'dummyaddress', 'chain': 'ethereum'}]
    }
]

db.insert_data(data)

# retrieve the newly inserted data
query_result = db.retrieve_table_data("collections", LIKE=("name", '%dummy%'), order_by="id")
print(query_result)

# all the other functions that are in the requirements are implement , tho i am not running them here due to they
# modify the database.
