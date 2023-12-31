import utils
import json
from flask import Response, abort, jsonify
import heapq
import pandas as pd
import pandas.core
from surprise import Dataset, NormalPredictor, Reader
import adaptador_modelos

CONTEXT = utils.open_files(file="context")
ACTION = utils.open_files(file="action")


def get_types():
    return {
        "rectypes": {
            0: "Popularity",
            1: {"Ranking": {0: "SVD", 1: "CoClustering", 2: "KNNBasic"}},
            2: "Content-based",
        }
    }


def get(
    Context: str,
    Action: str,
    nresult: int,
    rectype: int,
    ratingtype: int = 0,
    category: str = "",
    userId: str = "",
    itemId: str = "",
) -> None | dict | str:
    if rectype == 0:
        return get_popRecommendation(Context, nresult, Action)

    elif rectype == 1:
        return get_ratingRecommendation(Context, nresult, Action, userId, ratingtype)

    else:
        return get_contentBased(Context, itemId, nresult, category)


def get_popRecommendation(Context: str, nresult: int, Action: str) -> None | str:
    rating_count = adaptador_modelos.adapt_input(Context, 0, nresult, Action)
    rating_count.sort_values(
        "Ratings_per_item", ascending=False
    ).drop_duplicates().head(nresult)

    tmp_result = rating_count.to_dict(orient="index")
    return_json = adaptador_modelos.adapt_output(tmp_result, Context, 0, nresult)
    return_json = json.dumps(return_json)
    return return_json


def get_ratingRecommendation(
    Context: str, nresult: int, Action: str, userId: str, ratingtype: int
) -> None | dict:
    print(Context)
    RECOMMENDATION = utils.open_files("recommendation")
    return_json = adaptador_modelos.adapt_output(
        RECOMMENDATION, Context, 1, Action=Action, userId=userId, ratingtype=ratingtype
    )
    print(return_json)
    return return_json


def get_contentBased(
    Context: str, itemId: str, nresult: int, category: str
) -> None | dict:
    RECOMMENDATION = utils.open_files("recommendation")
    return_json = adaptador_modelos.adapt_output(
        RECOMMENDATION, Context, 2, itemId=itemId, nresult=nresult, category=category
    )

    return return_json
