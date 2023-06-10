import boto3
import json
from app.utils import config_util, dir_util, file_util


class AWSEmailService:
    def __init__(self):
        config = config_util.Config()
        self.aws_access_key_id = config.get('AWS_ACCESS_KEY_ID')
        self.aws_region = config.get('AWS_REGION')
        self.aws_secret_access_key = config.get('AWS_SECRET_ACCESS_KEY')
        self.ses = boto3.client('ses', aws_access_key_id=self.aws_access_key_id,
                                aws_secret_access_key=self.aws_secret_access_key, region_name=self.aws_region)
        self.sender_email = None
        self.receiver_email = None
        self.subject = None
        self.body = None
        self.email_type = 'html'
        self.template_name=None

    def send_email(self, **kwargs):
        body_type = 'Html' if self.email_type == 'html' else 'Text'
        if self.template_name:
            template_path = dir_util.safe_join(dir_util.app_path(), 'app/templates/email/{}.html'.format(self.template_name))
            # read template file
            self.body = file_util.read_file(template_path)
            # replace shortcodes with values
            for key, value in kwargs.items():
                self.body = self.body.replace('{'+key+'}', value)

        response = self.ses.send_email(
            Source=self.sender_email,
            Destination={
                'ToAddresses': [
                    self. receiver_email,
                ]
            },
            Message={
                'Subject': {
                    'Data': self.subject
                },
                'Body': {
                    body_type: {
                        'Data': self.body
                    }
                }
            }
        )
        return response

    def create_contact_list(self, contact_list_name):
        self.ses.create_contact_list(
            ContactListName=contact_list_name
        )

    def add_contact_to_list(self, contact_list_name, contact_email, contact_first_name=None, contact_last_name=None):
        self.ses.create_contact(
            ContactListName=contact_list_name,
            EmailAddress=contact_email,
            AttributesData=json.dumps({
                'FirstName': contact_first_name,
                'LastName': contact_last_name
            }) if contact_first_name or contact_last_name else None
        )
