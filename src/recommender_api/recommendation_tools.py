from collections import defaultdict
import json
from surprise import Dataset, SVD
import pandas as pd
import pandas.core
from surprise import Dataset, NormalPredictor, Reader
from surprise.prediction_algorithms import predictions
import utils


def get_top_n(predictions, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def get_all_top_n():
    CONTEXT = utils.open_files("context")
    RECOMMENDATION = dict()
    for c in CONTEXT.keys():
        RECOMMENDATION[c] = {}
        for a in CONTEXT[c]["actions"]:
            RECOMMENDATION[c][a] = {}
            rating_df = pd.DataFrame(
                CONTEXT[c]["actions"][a], columns=["userID", "itemID", "rating"]
            )
            reader = Reader(rating_scale=(CONTEXT[c]["actions"][a]["scale"]))

            data = Dataset.load_from_df(
                rating_df[["userID", "itemID", "rating"]], reader
            )
            print(rating_df)
            trainset = data.build_full_trainset()
            algo = SVD()
            algo.fit(trainset)

            testset = trainset.build_anti_testset()
            predictions = algo.test(testset)

            top_n = get_top_n(predictions, n=10)

            for uid, user_ratings in top_n.items():
                RECOMMENDATION[c][a][uid] = [iid for (iid, _) in user_ratings]

    utils.save_files("recommendation", RECOMMENDATION)

get_all_top_n()
