from requests_html import HTMLSession
from fake_useragent import UserAgent
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Twitter:
    base_url = 'https://twitter.com'
    api_base_url = 'https://api.twitter.com'
    mobile_base_url = 'https://mobile.twitter.com'
    user_agent = UserAgent()
    session = HTMLSession()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': base_url,
        'User-Agent': user_agent.opera,
        'X-Twitter-Active-User': 'yes',
    }
    search_params = {
        'vertical': 'default',
        'src': 'unkn',
        'include_available_features': 1,
        'include_entities': 1,
        'max_position': None,
        'reset_error_state': 'false',
        'lang': 'en',
        'f': 'tweets',
    }

    @classmethod
    def get_page(cls, url, params=None):
        response = cls.session.get(url=url, params=params, headers=cls.headers, verify=False)
        return response

    @classmethod
    def get_json_page(cls, url, params=None):
        headers = cls.headers
        headers['X-Requested-With'] = 'XMLHttpRequest'
        response = cls.session.get(url=url, params=params, headers=headers, verify=False)
        return response.json()