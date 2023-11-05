from collections import defaultdict
import json
from surprise import CoClustering, Dataset, SVD, KNNBasic
import pandas as pd
import pandas.core
from surprise import Dataset, NormalPredictor, Reader
from surprise.prediction_algorithms import predictions
import utils
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from . import adaptador_modelos

RECOMMENDATION = dict()
RECOMMENDATION["ranking"] = {}
RECOMMENDATION["content"] = {}


def get_top_n(predictions: list, n=10) -> defaultdict:
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


def get_all_top_n() -> None:
    ACTION = utils.open_files("action")
    for c in ACTION.keys():
        RECOMMENDATION["ranking"][c] = {}
        for a in ACTION[c]["actions"]:
            RECOMMENDATION["ranking"][c][a] = {}

            RECOMMENDATION["ranking"][c][a] = {}
            data = adaptador_modelos.adapt_input(c, 1, Action=a)

            # SDV
            trainset = data.build_full_trainset()
            algo = SVD()
            algo.fit(trainset)

            testset = trainset.build_anti_testset()
            predictions = algo.test(testset)

            top_n = get_top_n(predictions, n=10)
            RECOMMENDATION["ranking"][c][a][0] = {}
            for uid, user_ratings in top_n.items():
                RECOMMENDATION["ranking"][c][a][0][uid] = [
                    iid for (iid, _) in user_ratings
                ]

            # CoCLuresting

            trainset = data.build_full_trainset()
            algo = CoClustering()
            algo.fit(trainset)

            testset = trainset.build_anti_testset()
            predictions = algo.test(testset)

            top_n = get_top_n(predictions, n=10)
            RECOMMENDATION["ranking"][c][a][1] = {}
            for uid, user_ratings in top_n.items():
                RECOMMENDATION["ranking"][c][a][1][uid] = [
                    iid for (iid, _) in user_ratings
                ]

            # KNNBasic
            trainset = data.build_full_trainset()
            algo = KNNBasic()
            algo.fit(trainset)

            testset = trainset.build_anti_testset()
            predictions = algo.test(testset)

            top_n = get_top_n(predictions, n=10)
            RECOMMENDATION["ranking"][c][a][2] = {}
            for uid, user_ratings in top_n.items():
                RECOMMENDATION["ranking"][c][a][2][uid] = [
                    iid for (iid, _) in user_ratings
                ]

    utils.save_files("recommendation", RECOMMENDATION)


def content_based():
    ITEM = utils.open_files("item")
    for context in ITEM.keys():
        RECOMMENDATION["content"][context] = {}
        data = pd.DataFrame.from_dict(ITEM[context]["items"], orient="index")
        for key, _ in data.items():
            if key != "itemId" and key != "name":  # Ver sobre utilizar o nome ou não
                # Remove palavras de parada, como "the", "and"
                data_tfidf = TfidfVectorizer(stop_words="english")
                data[key] = data[key].fillna("")
                data_key_matrix = data_tfidf.fit_transform(
                    data[key]
                )  # Gera a matrix para calculo da similaridade do coseno

                # print(data_key_matrix.shape)

                similaridade_coseno = linear_kernel(data_key_matrix, data_key_matrix)
                RECOMMENDATION["content"][context][key] = {}
                for idx in range(data.shape[0]):
                    RECOMMENDATION["content"][context][key][
                        data["itemId"].iloc[idx]
                    ] = []
                    scores = list(enumerate(similaridade_coseno[idx]))
                    scores = sorted(scores, key=lambda x: x[1], reverse=True)
                    scores = scores[1:10]
                    index = [i[0] for i in similaridade_coseno]
                    for p in data["itemId"].iloc[index]:
                        RECOMMENDATION["content"][context][key][
                            data["itemId"].iloc[idx]
                        ].append(p)
                    #   print(p)
                #        print(data["name"].iloc[index])
    print(RECOMMENDATION)
    utils.save_files("recommendation", RECOMMENDATION)


get_all_top_n()
content_based()
