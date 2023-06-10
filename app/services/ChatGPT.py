from app.utils import config_util, file_util, dir_util, str_util
import openai

config = config_util.Config()
openai.api_key = config.get("OPENAI_API_KEY")


class ChatGPT:
    def __init__(self):
        self.max_tokens = 2000
        self.temperature = 0.5
        self.top_p = 1
        self.file = None
        self.instruction = None

    def create(self):
        """
        Text generation tool using chat gpt
        :return:
        """
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=self.instruction,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            frequency_penalty=0,
            presence_penalty=0
        )

        result = response['choices'][0]

        return result['text']  # the generated text

    def code(self):
        """
        :return:
        """
        file_path = dir_util.safe_join(dir_util.app_path(), self.file)
        data = format(file_util.read_file(file_path))
        new_file = file_path[:-3] + '_2.' + file_path[-2:]
        response = openai.Edit.create(
            model="code-davinci-edit-001",
            input=data,
            instruction=self.instruction,
            temperature=self.temperature,
            top_p=self.top_p
        )
        result = response['choices'][0]
        new_data = result['text']
        file_util.write_file(new_file, new_data)
        return response['usage']['total_tokens']

    def edit(self):
        """
        :return:
        """
        file_path = dir_util.safe_join(dir_util.app_path(), self.file)
        data = format(file_util.read_file(file_path))
        new_file = file_path[:-3] + '_2.' + file_path[-2:]
        response = openai.Edit.create(
            model="text-davinci-edit-001",
            input=data,
            instruction=self.instruction,
            temperature=self.temperature,
            top_p=self.top_p
        )
        result = response['choices'][0]
        new_data = result['text']
        file_util.write_file(new_file, new_data)
        return response['usage']['total_tokens']

    def insert(self):
        file_path = dir_util.safe_join(dir_util.app_path(), self.file)
        data = format(file_util.read_file(file_path))
        inputs = data.split('[insert]')
        new_file = file_path[:-3] + '_2.' + file_path[-2:]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=inputs[0] + self.instruction,
            suffix=inputs[1],
            temperature=0,
            max_tokens=2000,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )
        result = response['choices'][0]
        new_data = inputs[0] + result['text'] + inputs[1]
        file_util.write_file(new_file, new_data)
        return response['usage']['total_tokens']


if __name__ == "__main__":
    gpt = ChatGPT()
    gpt.file = 'app/services/PhoneOTP/TextLocal.py'
    gpt.instruction = "edit send_otp function to send otp replacing {otp} with self.otp using textlocal api"
    response = gpt.code()
    print(response)
