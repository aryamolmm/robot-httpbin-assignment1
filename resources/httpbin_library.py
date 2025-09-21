import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from utils.data_generator  import generate_user_data
from robot.api.deco import keyword
from RequestsLibrary import RequestsLibrary
# from resources.data_generator import generate_user_data
from utils.retry_decorator import retry_robot
from utils.config_loader import BASE_URL, TIMEOUT

rl = RequestsLibrary()

class HttpbinLibrary:

    @keyword
    def create_http_session(self, session_name):
        rl.create_session(session_name, "https://httpbin.org")

    @keyword
    def post_random_user_data(self, session_name):
        """POST random user data to /post"""
        data = generate_user_data()   # <--- call here
        resp = rl.post_request(session_name, "/post", json=data)
        return resp