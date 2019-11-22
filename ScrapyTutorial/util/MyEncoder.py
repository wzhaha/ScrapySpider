import json
from ..items import *


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj, Author):
            return {
                'name': obj['name'],
                'birthdate': obj['birthdate'],
                'bio': obj['bio']
            }
        return json.JSONEncoder.default(self, obj)