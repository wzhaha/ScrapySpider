from termcolor import *
import json
def green_print(content):
    print(colored(json.dumps(content,indent=4), "green"))