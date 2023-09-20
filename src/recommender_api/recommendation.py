# recommendation.py
import utils
import json
from flask import abort
import heapq
import pandas as pd
from pandas.core import *

CONTEXT = utils.open_files(file="context")


def get(Context, userId, nresult, rectype):
    if rectype == 0:
        pass  # FBC

    elif rectype == 1:
        pass  # FC

    else:
        return get_popRecommendation(Context, nresult, "teste")


def get_popRecommendation(Context, nresult, Action):
    
    df = pd.DataFrame(CONTEXT[Context]["Actions"][Action], columns=['itemID', 'ratings'])
    
    df["Ratings_per_item"] = pd.groupby('itemID')['itemID'].transform('count')
    rating_count = pd.DataFrame(df, columns=['itemID','Ratings_per_item'])
    rating_count.sort_values('Ratings_per_item', ascending=False).drop_duplicates().head(nresult)
    
    result = rating_count.to_json(orient="split")
    return result
   # popular = {}
   # print("oi")
   # for item in CONTEXT[Context]["items"]:
   #     popular[item] = CONTEXT[Context]["items"][item][Action]["interactions"]
   #     print("oi 2")
    #most_rated_book = pd.DataFrame(books, columns=['book_id', 'user_id', 'avg_rating', 'no_of_ratings'])
   # poprec = heapq.nlargest(nresult, popular.items(), key=lambda i: i[1])

   # return poprec
