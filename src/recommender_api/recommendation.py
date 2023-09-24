# recommendation.py
import utils
import json
from flask import Response, abort, jsonify
import heapq
import pandas as pd
import pandas.core
from surprise import Dataset, NormalPredictor, Reader

CONTEXT = utils.open_files(file="context")


def get(Context: str, userId: str, nresult: int, rectype: int) -> None | dict | str:
    if rectype == 0:
        pass  # FBC

    elif rectype == 1:
        return get_ratingRecommendation(Context, nresult, "teste", userId)

    else:
        return get_popRecommendation(Context, nresult, "teste")


def get_popRecommendation(Context: str, nresult: int, Action: str) -> None | str:
    df = pd.DataFrame(
        CONTEXT[Context]["Actions"][Action], columns=["itemID", "ratings"]
    )

    df["Ratings_per_item"] = pd.groupby("itemID")["itemID"].transform("count")
    rating_count = pd.DataFrame(df, columns=["itemID", "Ratings_per_item"])
    rating_count.sort_values(
        "Ratings_per_item", ascending=False
    ).drop_duplicates().head(nresult)

    result = rating_count.to_json(orient="split")
    return result


def get_ratingRecommendation(
    Context: str, nresult: int, Action: str, userId: str
) -> None | dict:
    RECOMMENDATION = utils.open_files("recommendation")
    return_json = {}
    if Context in RECOMMENDATION.keys():
        if Action in RECOMMENDATION[Context].keys():
            if userId in RECOMMENDATION[Context][Action].keys():
                for item in range(
                    len(RECOMMENDATION[Context][Action][userId][:nresult])
                ):
                    return_json[f"itemID_{item}"] = RECOMMENDATION[Context][Action][
                        userId
                    ][item]
                return return_json
