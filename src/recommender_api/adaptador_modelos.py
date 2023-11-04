def adapt_input():
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
        pass

    if rectype == 1:
        return_json = {}
        return_json["recommendationType"] = "1"
        return_json["ratingType"] = ratingtype
        return_json["Recommendation"] = {}
        if Context in data["ranking"].keys():
            if Action in data["ranking"][Context].keys():
                if ratingtype in data["ranking"][Context][Action].keys():
                    if userId in data["ranking"][Context][Action][ratingtype].keys():
                        for item in range(
                            len(
                                data["ranking"][Context][Action][ratingtype][userId][
                                    :nresult
                                ]
                            )
                        ):
                            return_json["Recommendation"][f"itemID_{item}"] = data[
                                "ranking"
                            ][Context][Action][ratingtype][userId][item]
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
