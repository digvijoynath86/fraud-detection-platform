class RuleBasedScorer:

    def score(

            self,

            features

    ):

        score = 0

        if features["amount_ratio"] > 5:

            score += 0.4

        if features["is_new_country"]:

            score += 0.3

        if features["is_new_device"]:

            score += 0.2

        if features["transaction_count"] < 3:

            score += 0.1

        return min(

            score,

            1.0
        )