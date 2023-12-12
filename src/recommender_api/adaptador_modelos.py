import pandas as pd
from surprise import Dataset, NormalPredictor, Reader
from surprise.dataset import DatasetAutoFolds
import utils


def adapt_input(
    Context: str,
    rectype: int,
    nresult: int = 10,
    Action: str = "",
    userId: str = "",
    itemId: str = "",
    ratingtype: int = -1,
    category: str = "",
) -> None | dict | pd.DataFrame | DatasetAutoFolds:
    if rectype == 0:
        ACTION = utils.open_files(file="action")
        df = pd.DataFrame(
            ACTION[Context]["actions"][Action], columns=["itemID", "ratings"]
        )

        df["Ratings_per_item"] = df.groupby("itemID")["itemID"].transform("count")

        output_data = pd.DataFrame(df, columns=["itemID", "Ratings_per_item"])

        return output_data

    if rectype == 1:
        ACTION = utils.open_files(file="action")
        rating_df = pd.DataFrame(
            ACTION[Context]["actions"][Action], columns=["userID", "itemID", "rating"]
        )
        reader = Reader(rating_scale=(ACTION[Context]["actions"][Action]["scale"]))

        data = Dataset.load_from_df(rating_df[["userID", "itemID", "rating"]], reader)

        return data
    if rectype == 2:
        pass


def adapt_output(
    data: dict,
    Context: str,
    rectype: int,
    nresult: int = 10,
    Action: str = "",
    userId: str = "",
    itemId: str = "",
    ratingtype: int = -1,
    category: str = "",
) -> None | dict:
    if rectype == 0:
        result = dict()
        result["recommendationType"] = "0"
        result["Recommendation"] = {}
        for i in data:
            result["Recommendation"][f"itemID_{i}"] = data[i]["itemID"].strip("\n")

        return result

    if rectype == 1:
        return_json = {}
        return_json["recommendationType"] = "1"
        return_json["ratingType"] = ratingtype
        return_json["Recommendation"] = {}
        if Context in data["ranking"].keys():
            if Action in data["ranking"][Context].keys():
                if str(ratingtype) in data["ranking"][Context][Action].keys():
                    print(userId)
                    if userId in data["ranking"][Context][Action][str(ratingtype)].keys():
                        print("entrou!")
                        for item in range(
                            len(
                                data["ranking"][Context][Action][str(ratingtype)][userId][
                                    :nresult
                                ]
                            )
                        ):
                            return_json["Recommendation"][f"itemID_{item}"] = data[
                            "ranking"
                        ][Context][Action][str(ratingtype)][userId][item]
                        return return_json

    else:
        result = dict()
        result["recommendationType"] = "2"
        result["category"] = category
        result["Recommendation"] = {}

        if Context in data["content"]:
            if category in data["content"][Context]:
                if itemId in data["content"][Context][category]:
                    for item in range(len(data["content"][Context][category][itemId])):
                        result["Recommendation"][f"itemId_{item}"] = data["content"][
                            Context
                        ][category][itemId][item]

        return result
