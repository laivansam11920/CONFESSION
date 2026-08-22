from base import GetData

from flask import request


class GetDataWeb(GetData):

    def get_data(self):
        data = request.get_json()
        pass
