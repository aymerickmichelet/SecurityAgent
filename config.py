import json


class Config():
    def __init__(self):
        self.list = json.load(open('config.json', 'r'))

    def getText(self, text: str) -> str:
        if text in self.list["text"]:
            return self.list["text"][text]
        else:
            return ""

    def getToken(self) -> str:
        if "token_path" in self.list:
            return open(self.list["token_path"], "r").read()
        else:
            return ""

    def getUrl(self, text: str) -> str:
        if text in self.list["url"]:
            return self.list["url"][text]
        else:
            return ""