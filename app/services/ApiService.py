from daba.Mongo import collection
from app.utils import request_util, dt_util, mongo_util


class ApiService:
    def __init__(self):
        self.db_referers = collection('referers')
        self.db_monthly_access = collection('monthly_access')

    @property
    def verified(self):
        return self.verify_request()

    def verify_request(self):
        api_key = request_util.headers('X-API-Key')
        referer = request_util.headers('Referer')

        # Verifying the API key and Referer
        query = mongo_util.Query()
        query.Status = 1
        query.Key = api_key
        query.Referer = referer

        referer_data = self.db_referers.getAfterCount(query.build(), "CallCount")

        if not referer_data:
            return False

        # Checking the Monthly Access
        current_month = dt_util.get_current_time().month
        query = mongo_util.Query()
        query.RefererId = referer_data["_id"]
        query.Month = current_month

        monthly_access_data = self.db_monthly_access.getAfterCount(query.build(), "CallCount")
        if monthly_access_data is None:
            # Insert a new document for the current month with CallCount 1
            self.db_monthly_access.put({"RefererId": referer_data["_id"], "Month": current_month, "CallCount": 1})
        elif monthly_access_data["CallCount"] >= referer_data["Limit"]:
            return False

        return True
