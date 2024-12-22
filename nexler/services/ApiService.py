import httpx
import json
from daba.Mongo import collection
from nexler.utils import request_util, dt_util, mongo_util, str_util, config_util, token_util
from nexler.services.AuthService import user


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

        # -1 means there is no monthly limit. Any positive number will be checked for monthly access.
        if referer_data["Limit"] == -1:
            return True

        # Checking the Monthly Access
        current_month = int(str(dt_util.get_current_time().year) + str(dt_util.get_current_time().month))
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


class ExternalApi:
    def __init__(
            self,
            url,
            data=None,
            user_agent=None,
            authorization=None,
            accept=None,
            content_type=None,
            headers=None
    ):
        self.url = url
        self.data = data
        self.headers = {
            "User-Agent": user_agent or "Nexler/1.4",
            "Accept": accept or "application/json",
            "Content-Type": content_type or "",
            "X-Client-Type": "internal"
        }
        auth_header = {"Authorization": authorization} if authorization else {}
        self.headers.update(auth_header)
        if headers:
            self.headers.update(headers)
        self.response = None

    async def fetch(self, method):
        if self.headers['Content-Type'] == 'application/json':
            data = json.dumps(self.data)
        else:
            data = self.data

        async with httpx.AsyncClient() as client:
            if method.lower() == 'get':
                self.headers.pop("Content-Type")
                self.response = await client.get(self.url, headers=self.headers)
            elif method.lower() == 'post':
                self.response = await client.post(self.url, headers=self.headers, data=data)
            elif method.lower() == 'put':
                self.response = await client.put(self.url, headers=self.headers, data=data)
            elif method.lower() == 'delete':
                self.response = await client.delete(self.url, headers=self.headers)
            else:
                raise ValueError(f"Invalid method: {method}")

        return self.parse_response()

    def parse_response(self):
        if 200 <= self.response.status_code < 300:
            content_type = self.response.headers['content-type']
            if 'application/json' in content_type:
                if self.response.text:
                    return str_util.parse(self.response.text)
                return {"status": "Success", "Content": None, "Status": self.response.status_code}
            else:
                return self.response.text
        elif self.response.status_code == 401:
            return {"status": "unauthorised", "Message": self.response.text}
        else:
            return {"status": "error", "Error": f"received status code {self.response.status_code}", "Message": self.response.text, "Status": self.response.status_code}


class InternalApi(ExternalApi):
    def __init__(self, service='gateway', path="", data=None, secure=False):
        self.token = None
        api_config = config_util.Config(f'app/config/{service}.json')
        if service == 'gateway':
            url = config_util.Config().get('GATEWAY_URL')
        else:
            url = api_config.get('API_URL')
        if not url:
            raise SystemError(f'API configuration for {service} is null.')
        super().__init__(str(url) + str(path))
        self.headers = {
            "User-Agent": "Nexler/1.1",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        if secure:
            self.token = token_util.create_access_token(user.Id)
            self.headers["Authorization"] = f"Bearer {self.token}"
        if service == 'gateway':
            self.headers['X-API-Key'] = config_util.Config().get('GATEWAY_KEY')
            self.headers['Referer'] = config_util.Config().get('SERVICE_NAME')
        else:
            self.headers['X-API-Key'] = api_config.get('API_KEY')
            self.headers['Referer'] = api_config.get('SERVICE_NAME')
        if data:
            self.data = data
