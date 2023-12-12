import pandas as pd
from collections import defaultdict
from surprise import Dataset, accuracy
import requests
from requests.auth import HTTPBasicAuth
import json
import numpy as np
import action

from surprise import CoClustering, Dataset, SVD, KNNBasic

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Auth": "qtpnqygJElFxxn1BtG3gc7VuGcovK7yb871PlPYiroNgkxozSkQNgx5bYJjF17j8XsteKm5F4eMZReaxrBkHQQDfxXI3B0g73Ba93sd1m67teFSbMdGdwfLbeWmSz4jW",
}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        return super(NumpyEncoder, self).default(obj)


def read_data(header=headers):
    #    data = pd.read_csv("u.data", sep="\t")
    data = pd.read_csv("ratings.dat", sep="::", engine="python")
    data.columns = ["userId", "itemId", "rating", "timestamp"]
    url = "http://127.0.0.1:8000/api/action"

    for index, row in data.iterrows():
        obj = {
            "Action": "rating",
            "Context": "ml-1m",
            "Unit": "5-estrelas",
            "itemIds": [
                {data["itemId"]: {"user": data["userId"], "ParameterValue": data["rating"]}}
            ],
        }
        obj = json.dumps(obj, cls=NumpyEncoder)
        obj = json.loads(obj)
        # action.register(obj)
        x = requests.post(url, json=obj, headers=header)
        print(x.text)
        if x.status_code not in range(200, 209):
            return


def configure_context(header=headers):
    url = "http://127.0.0.1:8000/api/context"
    headers = {
        "Accept": "application/json",
        # "X-Auth": "qtpnqygJElFxxn1BtG3gc7VuGcovK7yb871PlPYiroNgkxozSkQNgx5bYJjF17j8XsteKm5F4eMZReaxrBkHQQDfxXI3B0g73Ba93sd1m67teFSbMdGdwfLbeWmSz4jW",
    }
    # auth = HTTPBasicAuth('apiKey', 'qtpnqygJElFxxn1BtG3gc7VuGcovK7yb871PlPYiroNgkxozSkQNgx5bYJjF17j8XsteKm5F4eMZReaxrBkHQQDfxXI3B0g73Ba93sd1m67teFSbMdGdwfLbeWmSz4jW')
    obj = {
        "Context": "ml-1m",
        "email": "user@example.com",
        "item_schema": "string",
        "name": "string",
        "recommenders": [{"recommender": {"id": 1, "updateTime": 360}}],
    }
    x = requests.post(url, json=obj, headers=headers)  # auth=auth)
    print(x.text)

    url = "http://127.0.0.1:8000/api/metric"
    obj = {
        "Context": "ml-1m",
        "Units": [{"Unit": "5-estrelas", "maxScale": 1, "minScale": 5}],
    }
    x = requests.post(url, json=obj, headers=header)  # auth=auth)
    print(x.text)




configure_context()
read_data()


