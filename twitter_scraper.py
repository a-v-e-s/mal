import urllib3, json, re
from anonBrowser import *

class reconPerson():

    def __init__(self, first_name, last_name, job='', social_media={}):
        self.first_name = first_name
        self.last_name = last_name
        self.job = job
        self.social_media = social_media

    def __repr__(self):
        return self.first_name + ' ' + self.last_name + ' has job ' + self.job

    def get_social(selfself, media_name):
        if self.social_media.has_key(media_name):
            return self.social_media[media_name]
        else:
            return None

    def query_twitter(self, query):
        query = urllib3.quote_plus(query)
        results = []
        browser = anonBrowser()
        response = browser.open('https://search.twitter.com/search.json?q=' + query)
        json_objects = json.load(response)
        for result in json_objects['results']:
            new_result = {}
            new_result['from_user'] = result['from_user_name']
            new_result['geo'] = result['geo']
            new_result['tweet'] = result['text']
            results.append(new_result)
        return results

    def get_tweets(self, handle):
        query = urllib3.quote_plus('from:' + handle + ' since:2009-01-01 inclue:retweets')
        tweets = []
        browser = anonBrowser()
        browser.anonymize()
        response = browser.open('https://search.twitter.com/search.json?1=' + query)
        json_objects = json.load(response)
        for result in json_objects['results']:
            new_result = {}
            new_result['from_user'] = result['from_user_name']
            new_result['geo'] = result['geo']
            new_result['tweet'] = result['text']
            tweets.append(new_result)
        return tweets

    def find_interests(self, tweets):
        interests = {}
        interests['links'] = []
        interests['users'] = []
        interests['hashtags'] = []
        for tweet in tweets:
            text = tweet['tweet']
            links = re.compile(r'(https.*?)|(http.*?)').findall(text)
            for link in links:
                if link[0]:
                    link = link[0]
                elif link[1]:
                    link = link[1]
                else:
                    continue
                try:
                    response = urllib3.urlopen(link)
                    full_link = response.url
                    interests['links'].append(full_link)
                except Exception:
                    pass
            interests['users'] += re.compile(r'(@\w+)').findall(text)
            interests['hashtags'] += re.compile(r'(#\w+)').findall(text)
        interests['users'].sort()
        interests['hashtags'].sort()
        interests['links'].sort()
        return interests

    def load_cities(self, cityFile):
        cities = []
        for line in open(cityFile).readlines():
            city = line.strip('\n').strip('\r').lower()
            cities.append(city)
        return cities

    def twitter_locate(self, tweets, cities):
        locations = []
        locCnt = 0
        cityCnt = 0
        tweetsText = ''
        for tweet in tweets:
            if tweet['geo'] != None:
                locations.append(tweet['geo'])
                locCnt += 1
                tweetsText += tweet['tweet'].lower()
        for city in cities:
            if city in tweetsText:
                locations.append(city)
                cityCnt += 1
        print('[+] Found ' + str(locCnt) + ' locations via Twitter API and ' \
              + str(cityCnt) + ' locations from text search.')
        return locations
