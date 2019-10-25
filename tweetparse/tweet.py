from datetime import datetime
import tweetparse.twitter


class Tweet:

    def __init__(self, html, debug=False):
        self.debug = html.html if debug else False
        self.pinned = True if 'js-pinned' in html.attrs['class'] else False
        tweet_div = html.find('div.tweet', first=True)
        self.id = int(tweet_div.attrs['data-tweet-id'])
        self.name = tweet_div.attrs['data-name']
        self.screen_name = tweet_div.attrs['data-screen-name']
        self.user_id = int(tweet_div.attrs['data-user-id'])
        self.permalink_path = tweetparse.twitter.Twitter.base_url + tweet_div.attrs['data-permalink-path']
        self.time = datetime.utcfromtimestamp(int(tweet_div.find('span.js-short-timestamp', first=True).attrs['data-time']))
        # -- parse tweet text and hyperlinks
        tweet_text_paragraph = tweet_div.find('p.tweet-text', first=True)
        self.text = tweet_text_paragraph.text
        self.urls = []
        self.hashtags = []
        self._parse_links(tweet_text_paragraph)
        # -- counts & metrics
        for item in ['reply', 'retweet', 'favorite']:
            xpath = 'span.ProfileTweet-action--{0} > span.ProfileTweet-actionCount'.format(item)
            count = int(tweet_div.find(xpath, first=True).attrs['data-tweet-stat-count'])
            self.__setattr__(item, count)

    def _parse_links(self, tweet_text_paragraph):
        # Parser and Store - External Links, Hash Tags, Tagged Users and Other URls
        for link in tweet_text_paragraph.find('a'):
            if 'data-expanded-url' in link.attrs:
                self.urls.append(link.attrs['data-expanded-url'])
            elif link.attrs['href'].startswith('/hashtag/') and link.attrs['href'].endswith('?src=hash'):
                tag = '#' + link.attrs['href'].split('?')[0].replace('/hashtag/', '')
                url = tweetparse.twitter.Twitter.base_url + link.attrs['href']
                self.hashtags.append(('hashtag', tag, url))
            elif link.attrs['href'].startswith('/') and len(link.attrs['href'].split('/')) == 2:
                screen_name = '@' + link.attrs['href'].split('/')[1]
                url = tweetparse.twitter.Twitter.base_url + link.attrs['href']
                self.hashtags.append(('screen_name', screen_name, url))
            elif link.attrs['href'].startswith('/'):
                self.urls.append(tweetparse.twitter.Twitter.base_url + link.attrs['href'])
            elif 'data-expanded-url' in link.attrs:
                self.urls.append(link.attrs['data-expanded-url'])
            else:
                self.urls.append(link.attrs['href'])
