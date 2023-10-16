# recommendation.py
import utils
import json
from flask import Response, abort, jsonify
import heapq
import pandas as pd
import pandas.core
from surprise import Dataset, NormalPredictor, Reader

CONTEXT = utils.open_files(file="context")


def get_types():
    return {"rectypes": {0: "Popularity", 1: {"Ranking": {0: "SVD"}}}}


def get(Context: str, userId: str, nresult: int, rectype: int) -> None | dict | str:
    if rectype == 0:
        pass  # FBC

    elif rectype == 1:
        return get_ratingRecommendation(Context, nresult, "teste", userId)

    else:
        return get_popRecommendation(Context, nresult, "teste")


def get_popRecommendation(Context: str, nresult: int, Action: str) -> None | str:
    df = pd.DataFrame(
        CONTEXT[Context]["actions"][Action], columns=["itemID", "ratings"]
    )

    df["Ratings_per_item"] = df.groupby("itemID")["itemID"].transform("count")
    rating_count = pd.DataFrame(df, columns=["itemID", "Ratings_per_item"])
    rating_count.sort_values(
        "Ratings_per_item", ascending=False
    ).drop_duplicates().head(nresult)

    # rating_count.set_index('itemID', inplace=True)
    tmp_result = rating_count.to_dict(orient="index")
    result = dict()
    result["recommendationType"] = "2"
    result["Recommendation"] = {}
    for i in tmp_result:
        print(tmp_result[i])
        result["Recommendation"][f"itemID_{i}"] = tmp_result[i]["itemID"].strip("\n")

    result = json.dumps(result)
    print(result)
    return result


def get_ratingRecommendation(
    Context: str, nresult: int, Action: str, userId: str
) -> None | dict:
    RECOMMENDATION = utils.open_files("recommendation")
    return_json = {}
    return_json["recommendationType"] = "1"
    return_json["Recommendation"] = {}
    if Context in RECOMMENDATION.keys():
        if Action in RECOMMENDATION[Context].keys():
            if userId in RECOMMENDATION[Context][Action].keys():
                for item in range(
                    len(RECOMMENDATION[Context][Action][userId][:nresult])
                ):
                    return_json["Recommendation"][f"itemID_{item}"] = RECOMMENDATION[
                        Context
                    ][Action][userId][item]
                print(return_json)
                return return_json
