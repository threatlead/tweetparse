from requests_html import HTML
from .twitter import Twitter
from .tweet import Tweet


class Search:

    def __init__(self, search=None):
        self.query = ''

    def search(self, search=None):
        self.query = f' {search}'

    def screen_name(self, screen_name):
        self.query += f' from:{screen_name}'

    def geocode(self, geocode):
        self.query += f' geocode:{geocode}'

    def until(self, timestamp):
        self.query += ' until:{0}'.format(timestamp.strftime('%Y-%m-%d'))

    def since(self, timestamp):
        self.query += " since:{0}".format(timestamp.strftime('%Y-%m-%d'))

    def filter_emails(self):
        self.query += ' "{0}"'.format('" OR "'.join(['mail', 'email', 'gmail', 'e-mail']))

    def filter_phones(self):
        self.query += f' "{0}"'.format('" OR "'.join(['phone', 'call me', 'text me']))

    def verified(self):
        self.query += ' filter:verified'

    def to(self, screen_name):
        self.query += f' to:{screen_name}'

    def all(self, screen_name):
        self.query += f' to:{screen_name} OR from:{screen_name} OR @{screen_name}'

    def near(self, near):
        self.query += f' near:{near}'

    def filter_images(self):
        self.query += ' filter:images'

    def filter_videos(self):
        self.query += ' filter:videos'

    def filter_media(self):
        self.query += ' filter:media'

    def filter_replies(self):
        self.query += ' filter:replies'

    def filter_min_likes(self, min_likes):
        self.query += f' min_faves:{min_likes}'

    def filter_min_retweets(self, min_retweets):
        self.query += f' min_retweets:{min_retweets}'

    def filter_min_replies(self, min_replies):
        self.query += f' min_retweets:{min_replies}'

    def filter_links(self, include=True):
        if include:
            self.query += ' filter:links'
        else:
            self.query += ' exclude:links'

    def source(self, source):
        self.query += f' source:\"{source}\"'

    def members_list(self, members):
        self.query += f' list:{members}'

    def filter_retweets(self, exclude=False):
        if exclude:
            self.query += f' exclude:nativeretweets exclude:retweets'
        else:
            self.query += ' filter:nativeretweets'

    def execute(self, max_position=0):
        url = '{0}/i/search/timeline'.format(Twitter.base_url)
        search_params = Twitter.search_params
        search_params['q'] = self.query
        search_params['max_position'] = max_position
        response = Twitter.get_page(url=url, params=search_params)
        # -- position
        if 'min_position' in response.json().keys():
            max_position = response.json()['min_position']
        # -- tweets
        tweet_list = []
        for item in HTML(html=response.json()['items_html']).find('li.stream-item'):
            if item.attrs['data-item-type'] == 'tweet':
                tweet_list.append(Tweet(html=item, debug=False))
        return max_position, tweet_list
