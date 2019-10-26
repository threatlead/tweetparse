import json
from requests_html import HTML
from datetime import datetime
from .twitter import Twitter
from .tweet import Tweet


class User:

    def __init__(self, screen_name, debug=False):
        self.screen_name = screen_name
        self.debug = debug
        self.min_position = None
        self.max_position = None
        # -- profile
        self.raw = None
        self.id = None
        self.name = None
        self.created_at = None
        self.description = None
        self.favourites_count = None
        self.followers_count = None
        self.friends_count = None
        self.location = None
        self.profile_image_url = None
        self.statuses_count = None
        self.verified = None

    @property
    def profile_url(self):
        return f'{Twitter.base_url}/{self.screen_name}?lang=en'

    @property
    def timeline_url(self):
        return f'{Twitter.base_url}/i/profiles/show/{self.screen_name}/timeline/tweets'

    @property
    def favorites_url(self):
        return f'{Twitter.mobile_base_url}/{self.screen_name}/favorites'

    @property
    def followers_url(self):
        return f'{Twitter.mobile_base_url}/{self.screen_name}/followers'

    @property
    def following_url(self):
        return f'{Twitter.mobile_base_url}/{self.screen_name}/following'

    def get_profile(self):
        response = Twitter.get_page(url=self.profile_url)
        data = json.loads(response.html.find('input#init-data', first=True).attrs['value'])
        self.raw = data['profile_user'] if self.debug else False
        self.id = data['profile_user']['id']
        self.name = data['profile_user']['name']
        self.screen_name = data['profile_user']['screen_name']
        self.created_at = datetime.strptime(data['profile_user']['created_at'], '%a %b %d %H:%M:%S %z %Y')
        self.description = data['profile_user']['description']
        self.favourites_count = data['profile_user']['favourites_count']
        self.followers_count = data['profile_user']['followers_count']
        self.friends_count = data['profile_user']['friends_count']
        self.location = data['profile_user']['location']
        self.profile_image_url = data['profile_user']['profile_image_url']
        self.statuses_count = data['profile_user']['statuses_count']
        self.verified = data['profile_user']['verified']

    @property
    def as_dict(self):
        user_dict = self.__dict__
        for key in ['debug', 'raw', 'max_position', 'min_position']:
            del user_dict[key]
        user_dict['created_at'] = self.created_at.isoformat()
        return user_dict

    def get_tweets(self):
        search_params = Twitter.search_params
        search_params['max_position'] = self.min_position
        response = Twitter.get_json_page(url=self.timeline_url, params=search_params)
        self.min_position = int(response['min_position']) if 'min_position' in response else self.min_position
        self.max_position = int(response['max_position']) if 'max_position' in response else self.max_position
        # parse tweets
        tweet_list = []
        for item in HTML(html=response['items_html']).find('li.stream-item'):
            if item.attrs['data-item-type'] == 'tweet':
                tweet_list.append(Tweet(html=item, debug=self.debug))
        return tweet_list

    def get_favorites(self):
        params = {'lang': 'en', 'max_id': None}
        url = self.favorites_url
        pass

    def get_followers(self):
        params = {'lang': 'en', 'cursor': None}
        url = self.followers_url
        response = Twitter.get_page(url=url, params=params)
        return User._parse_screen_names(response)

    def get_following(self, recent_followers=True, all_followers=False):
        params = {'lang': 'en', 'cursor': None}
        url = self.following_url
        response = Twitter.get_page(url=url, params=params)
        return User._parse_screen_names(response)

    @classmethod
    def _parse_screen_names(cls, response):
        user_list = []
        for html in response.html.find('span.username'):
            if html.text.startswith('@'):
                user = User(screen_name=html.text.replace('@', ''))
                user_list.append(user)
        return user_list
