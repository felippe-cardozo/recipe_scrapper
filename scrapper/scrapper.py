from bs4 import BeautifulSoup
import re
import requests

class TudoGostoso:
    def __init__(self, q):
        self.core_url = 'http://tudogostoso.com.br'
        self.q = re.sub(' ', '+', q)
        self.results = self.format_results()

    def get_html(self):
        return requests.get(self.core_url + '/busca.php?q=' + self.q).text

    def scrap_results(self):
        r = self.get_html()
        soup = BeautifulSoup(r, 'html.parser')
        contents = soup.find('div', class_='content')
        ul = contents.find('ul', class_='clearfix')
        recipes = ul.find_all('li')
        return recipes

    def format_results(self):
        recipes = self.scrap_results()
        return {recipe.find('h2').text: self.core_url +
                recipe.find('a')['href'] for recipe in recipes}
