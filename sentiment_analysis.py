from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup

BLOOMBERG_URL = "https://www.bloomberg.com/search?query="
companies = ["Google", "Apple"]


class Spider:

    def __init__(self):
        self._sentiment_analysis_endpoint = "https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"
        self._key1 = "bb27d2f5fb3b4b889bce822d726b09ac"
        self._key2 = "01572def178342179993aa4eef97d341"

    def __get_sentiment(self, story):
        payload = {'documents':[{'id':1, 'language':'en', 'text':story}]}
        print(json.dumps(payload))
        headers = headers = {'Ocp-Apim-Subscription-Key': self._key2}
        url = self._sentiment_analysis_endpoint
        request = requests.post(url, data=json.dumps(payload), headers=headers)
        print(request.text)

    def get_links(self, company):
        return_array = []
        url = BLOOMBERG_URL + company
        body = requests.get(url)
        content = body.text

        soup = BeautifulSoup(content, "html.parser")

        story_links = soup.find_all("h1", {"class": "search-result-story__headline"})

        for link in story_links:
            return_array.append(link.contents[1]["href"])

        return return_array


    def get_content(self, company):

        links = self.get_links(company)
        return_content = dict()
        for link in links:
            content = requests.get(link).text
            soup = BeautifulSoup(content,"html.parser")
            story = ""
            paragraphs = soup.find_all("p")
            for paragraph in paragraphs:
                try:
                    story += paragraph.contents[0]
                    story += "\n"
                except:
                    continue
            return_content[link] = story
        return return_content




    def get_sentiments(self, company):
        return_sentiments = dict()
        stories = self.get_content(company=company)
        stories = dict(stories)

        for key in stories.keys():
            if key is not None:
                story = stories.get(key)
                self.__get_sentiment(story)









spider = Spider()
pprint(spider.get_sentiments(company="Google"))

