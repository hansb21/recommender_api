from collections import defaultdict
import json
from surprise import CoClustering, Dataset, SVD, KNNBasic, accuracy
import pandas as pd
import pandas.core
from surprise import Dataset, NormalPredictor, Reader
from surprise.prediction_algorithms import predictions
from surprise.model_selection import KFold
import utils
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import adaptador_modelos

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
            RECOMMENDATION["ranking"][c][a][0] = {}
            data = adaptador_modelos.adapt_input(c, 1, Action=a)

            # SDV
            trainset = data.build_full_trainset()  # DIVIDIR AQUI
            algo = SVD()
            algo.fit(trainset)

            testset = trainset.build_anti_testset()
            predictions = algo.test(testset)
            RECOMMENDATION["ranking"][c][a][0]["rmse"] = accuracy.rmse(predictions, verbose=True)
      
            top_n = get_top_n(predictions, n=10)
            for uid, user_ratings in top_n.items():
                RECOMMENDATION["ranking"][c][a][0][uid] = [
                    iid for (iid, _) in user_ratings
                ]

            # CoCLuresting

            RECOMMENDATION["ranking"][c][a][1] = {}
            trainset = data.build_full_trainset()
            algo = CoClustering()
            algo.fit(trainset)

            testset = trainset.build_anti_testset()
            predictions = algo.test(testset)
            RECOMMENDATION["ranking"][c][a][1]["rmse"] = accuracy.rmse(predictions, verbose=True)
            
            top_n = get_top_n(predictions, n=10)
            for uid, user_ratings in top_n.items():
                RECOMMENDATION["ranking"][c][a][1][uid] = [
                    iid for (iid, _) in user_ratings
                ]

            # KNNBasic
            RECOMMENDATION["ranking"][c][a][2] = {}
            trainset = data.build_full_trainset()
            algo = KNNBasic()
            algo.fit(trainset)

            testset = trainset.build_anti_testset()
            predictions = algo.test(testset)
            RECOMMENDATION["ranking"][c][a][2]["rmse"] = accuracy.rmse(predictions, verbose=True)
            top_n = get_top_n(predictions, n=10)
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
        if ITEM[context]["item_schema"] == "Movie":
            for key, _ in data.items():
                if key in [
                    "title",
                    "description",
                    "year",
                    "tags",
                    "director",
                    "actors",
                ]:
                    # Remove palavras de parada, como "the", "and"
                    data_tfidf = TfidfVectorizer(stop_words="english")
                    data[key] = data[key].fillna("")
                    data_key_matrix = data_tfidf.fit_transform(
                        data[key]
                    )  # Gera a matrix para calculo da similaridade do coseno

                    # print(data_key_matrix.shape)

                    similaridade_coseno = linear_kernel(
                        data_key_matrix, data_key_matrix
                    )
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

        if ITEM[context]["item_schema"] == "Book":
            for key, _ in data.items():
                if key in ["title", "description", "year", "tags", "author"]:
                    # Remove palavras de parada, como "the", "and"
                    data_tfidf = TfidfVectorizer(stop_words="english")
                    data[key] = data[key].fillna("")
                    data_key_matrix = data_tfidf.fit_transform(
                        data[key]
                    )  # Gera a matrix para calculo da similaridade do coseno

                    # print(data_key_matrix.shape)

                    similaridade_coseno = linear_kernel(
                        data_key_matrix, data_key_matrix
                    )
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

        if ITEM[context]["item_schema"] == "Item":
            for key, _ in data.items():
                if key in ["title", "price", "dataAdded"]:
                    # Remove palavras de parada, como "the", "and"
                    data_tfidf = TfidfVectorizer(stop_words="english")
                    data[key] = data[key].fillna("")

                    data_key_matrix = data_tfidf.fit_transform(
                        data[key]
                    )  # Gera a matrix para calculo da similaridade do coseno

                    # print(data_key_matrix.shape)

                    similaridade_coseno = linear_kernel(
                        data_key_matrix, data_key_matrix
                    )
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

    utils.save_files("recommendation", RECOMMENDATION)



def precision_recall_at_k(predictions, k=10, threshold=3.5):
    """Return precision and recall at k metrics for each user"""

    # First map the predictions to each user.
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():

        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)

        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)

        # Number of recommended items in top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])

        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(
            ((true_r >= threshold) and (est >= threshold))
            for (est, true_r) in user_ratings[:k]
        )

        # Precision@K: Proportion of recommended items that are relevant
        # When n_rec_k is 0, Precision is undefined. We here set it to 0.

        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0

        # Recall@K: Proportion of relevant items that are recommended
        # When n_rel is 0, Recall is undefined. We here set it to 0.

        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 0

    return precisions, recalls

def get_recall():
    ACTION = utils.open_files("action")
    for c in ACTION.keys():
        RECOMMENDATION["ranking"][c] = {}
        for a in ACTION[c]["actions"]:

            RECOMMENDATION["ranking"][c][a] = {}
            RECOMMENDATION["ranking"][c][a][0] = {}
            data = adaptador_modelos.adapt_input(c, 1, Action=a)

            # SDV
            trainset = data.build_full_trainset()  # DIVIDIR AQUI
            kf = KFold(n_splits=5)
            algo = SVD()

            for trainset, testset in kf.split(data):
                algo.fit(trainset)
                predictions = algo.test(testset)
                precisions, recalls = precision_recall_at_k(predictions, k=5, threshold=4)

                # Precision and recall can then be averaged over all users
                print(sum(prec for prec in precisions.values()) / len(precisions))
                print(sum(rec for rec in recalls.values()) / len(recalls))

                precision_t = sum(prec for prec in precisions.values()) / len(precisions)
                recall_t = sum(rec for rec in recalls.values()) / len(recalls)
                f1_score = 2 * ((precision_t * recall_t )/ (precision_t+recall_t))
                print(f"f1={f1_score}")


#get_all_top_n()
#content_based()
get_recall()
