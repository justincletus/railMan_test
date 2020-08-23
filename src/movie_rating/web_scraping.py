import urllib.parse
import urllib.request
import http.client
import mimetypes
from urllib.error import HTTPError
import requests
import urllib.response
from bs4 import BeautifulSoup


class WebScrap:

    def getHtmlContent(self):
    
        data = []
        list_header = []

        url = "https://www.imdb.com/india/top-rated-indian-movies/"
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }       

        page = requests.get(url, headers=headers) 

        soup = BeautifulSoup(page.content, 'html.parser')    

        results = soup.find("table", class_="chart")

        html_data = results.tbody.find_all("tr")

        movie_list = []

        for i in range(len(html_data)):
            context = {}
            context['id'] = i+1
            data = []
            for x in html_data[i].find_all("td"):            
                x = x.get_text().strip()
                x = x.split('\n')
                data.append(x)
            context['detail'] = data

            movie_list.append(context)

        movie_data = []
        count  = 1
        for item in movie_list:
            context = {}
            context['id'] = item['id']
            
            for detail in item['detail'][1:-1]:
                index = item['detail'][1:-1].index(detail)
                context['name'] = item['detail'][1:-1][0][1].strip()
                slug = context['name'].lower()
                slug = slug.split(' ')
                slug = '-'.join([ n for n in slug ])
                context['slug'] = slug
                year = item['detail'][1:-1][0][2].strip()
                context['year'] = year[1:-1]
                context['rating'] = item['detail'][1:-1][1][0].strip()

                break
            movie_data.append(context)
                
        return movie_data
        # print(movie_data)

    

# getHtmlContent()

    
