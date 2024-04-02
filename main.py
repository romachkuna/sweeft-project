import json

import requests
import pandas as pd

import utils
from orm import Database

#
# collections_api_url = "https://api.opensea.io/api/v2/collections?chain=ethereum"
#
# headers = {
#     "accept": "application/json",
#     "x-api-key": "74236956836e4336b836845ae04c25f6"
# }
#
db = Database(
    host="localhost",
    user="root",
    password="romaroma",
    database="sweeft"
)

db.create_schema()

test = [{
    "collection": "mmerchegg",
    "name": "mmERCH // Egg Collection",
    "description": "mmERCH is Neo-Couture. 1-of-1-of-x luxury apparel linking fashion and art across the digital, physical, and virtual. 960 NFTs, physical twin and avatar included.",
    "image_url": "https://i.seadn.io/s/raw/files/dc03d66ec4f88fd940c18e1ae37adf5c.png?w=500&auto=format",
    "owner": "0x52fc180b32646830ab6ec584a2da2099e95e974a",
    "twitter_username": "",
    "contracts": [
        {
            "address": "0x4663cb85e4360b7a97ec5763788f86e39e6533ca",
            "chain": "ethereum"
        }
    ]
}, {
    "collection": "neeta-oy-art-pictures-by-sohvitar",
    "name": "Neeta Oy: Art Pictures by Sohvitar",
    "description": "Neeta Oy: Art pictures by Sohvitar from Finland.",
    "image_url": "https://i.seadn.io/s/raw/files/301ce92f2940e628945d7060f2f0f9a8.jpg?w=500&auto=format",
    "owner": "0x383b825c12fb4163c30b45f73ac4b696ebdb6949",
    "twitter_username": "",
    "contracts": [
        {
            "address": "0x01ab51b14ccb486096b28be29f000d983c2cbdd9",
            "chain": "ethereum"
        }
    ]
}]

db.insert_data(test)


