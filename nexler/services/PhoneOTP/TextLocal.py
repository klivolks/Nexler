from nexler.services import ExternalApi
from nexler.utils import config_util, dir_util
from nexler.utils import file_util


class TextLocal:
    def __init__(self, template='otp', sender='EXMPLE', phone=None):
        self.message = None
        self.phone = phone
        self.template = template
        self.sender = sender
        self.config = config_util.Config()

    def send_sms(self, **kwargs):
        template_path = dir_util.safe_join(dir_util.app_path(), f'app/templates/sms/{self.template}.txt')
        self.message = file_util.read_file(template_path)
        for key, value in kwargs.items():
            self.message = self.message.replace('{' + key + '}', str(value))
        api = ExternalApi(self.config.get('TEXTLOCAL_URL'))
        api.headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        api.data = "apikey={0}&numbers={1}&message={2}&sender={3}".format(
            self.config.get('TEXTLOCAL_KEY'), self.phone, self.message,
            self.sender
        )
        response = api.fetch('post')
        return response
