from bs4 import BeautifulSoup
from functools import reduce
import re
import requests


class RecipeScrapper:
    def __init__(self, q):
        self.name = 'RecipeScrapper'
        self.q = re.sub(' ', '+', q)
        self.results = 0

    def __len__(self):
        return len(self.results)

    def __repr__(self):
        return '<{}: query for "{}" found {} results>'.format(self.name,
                                                              self.q,
                                                              len(self))


class TudoGostoso(RecipeScrapper):
    def __init__(self, q, pages=1):
        self.name = 'TudoGostoso'
        self.core_url = 'http://tudogostoso.com.br'
        self.q = re.sub(' ', '+', q)
        self.pages = pages
        self.results = self.format_results()

    def get_html(self):
        url = self.core_url + '/busca.php?q=' + self.q + '&pag='
        reqs = [requests.get(url + str(i)) for i in range(1, self.pages + 1)]
        return [r.text for r in reqs if r.status_code == 200]

    def scrap(self, page):
        soup = BeautifulSoup(page, 'html.parser')
        contents = soup.find('div', class_='content')
        ul = contents.find('ul', class_='clearfix')
        recipes = ul.find_all('li')
        return recipes

    def join_pages(self):
        pages = self.get_html()
        if not pages:
            return []
        return reduce(lambda a, b: a + b, [self.scrap(page) for page in pages])

    def format_results(self):
        recipes = self.join_pages()
        return {recipe.find('h2').text + ' - ' + str(i): self.core_url +
                recipe.find('a')['href'] for i, recipe in enumerate(recipes)}


class TudoReceitas(RecipeScrapper):
    def __init__(self, q):
        self.name = 'TudoReceitas'
        self.core_url = 'https://www.tudoreceitas.com/'
        self.q = q
        self.results = self.format_results()

    def get_html(self):
        url = self.core_url + '/pesquisa?q=' + self.q
        req = requests.get(url)
        if req.status_code == 200:
            return req.text
        return ''

    def scrap(self):
        page = self.get_html()
        soup = BeautifulSoup(page, 'html.parser')
        results = soup.find_all('div', class_='resultado link')
        return results

    def format_results(self):
        recipes = self.scrap()
        if recipes:
            return {recipe.find('a').text + ' - ' + str(i): 
                    recipe.find('a')['href'] for i, recipe
                    in enumerate(recipes)}
        return {}
