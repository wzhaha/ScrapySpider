from termcolor import *
import json
from .MyEncoder import *
def green_print(content):
    print(colored(json.dumps(content,indent=4,cls=MyEncoder), "green"))