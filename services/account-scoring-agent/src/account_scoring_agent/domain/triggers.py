"""The rule or trigger shown beside a rating. Codes and wording follow the scorecard."""

from voc_data.enums import Rating

from account_scoring_agent.domain.models import Trigger

NEW_RED = Trigger("AR1", "New red this week")
REPEAT_RED = Trigger("AR2", "Repeat red")
CHURN_LANGUAGE = Trigger("AR4", "Churn language")
GREEN_TO_YELLOW = Trigger("AY1", "Moved from green to yellow")
REPEAT_YELLOW = Trigger("AY2", "Yellow, repeat")
RED_TO_YELLOW = Trigger("AY3", "Moved from red to yellow")
NO_RULE = Trigger("AG0", "No rule matched")


def trigger_for(rating: Rating, previous: Rating | None, churn_language: bool) -> Trigger:
    if rating is Rating.RED:
        if churn_language:
            return CHURN_LANGUAGE
        return REPEAT_RED if previous is Rating.RED else NEW_RED
    if rating is Rating.YELLOW:
        if previous is Rating.RED:
            return RED_TO_YELLOW
        return REPEAT_YELLOW if previous is Rating.YELLOW else GREEN_TO_YELLOW
    return NO_RULE
