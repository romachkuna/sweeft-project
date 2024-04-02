import json

import requests
import pandas as pd

from utils import *
from orm import Database

# db = Database(
#     host="localhost",
#     user="root",
#     password="romaroma",
#     database="sweeft"
# )


# headers = {
#     "accept": "application/json",
#     "x-api-key": "74236956836e4336b836845ae04c25f6"
# }
#
# response = make_call_to_api(headers)

df = construct_df_from_json()

print(df)
