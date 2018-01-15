from bs4 import BeautifulSoup
from collections import namedtuple
import asyncio
import aiohttp


class RecipeParser:
    "Abstract Parser class for recipes"
    def __init__(self, data):
        self.data = data
        self.name = type(self).__name__

    def __len__(self):
        return len(self.parse())

    def __repr__(self):
        return '< {} : {} >'.format(self.name, self.parse())

    def parse(self):
        return {}


class TudoGostoso(RecipeParser):
    """
    Parses the html of a query in 'http://tudogostoso.com.br'.
    returns a dict in the following format: title + n: link
    """
    url = 'http://tudogostoso.com.br/busca.php?q='

    def parse(self):
        soup = BeautifulSoup(self.data, 'lxml')
        content = soup.find('div', {'class': 'content'})
        recipes = content.find('ul', {'class': 'clearfix'}).find_all('li')
        return self.to_dict(recipes)

    def to_dict(self, recipes):
        core_url = 'https://www.tudogostoso.com.br'
        if recipes:
            return {recipe.find('h2').text + ' - ' + str(i): core_url +
                    recipe.find('a')['href'] for i,
                    recipe in enumerate(recipes)}
        return {}


class TudoReceitas(RecipeParser):
    """
    Parses the html of a query in 'http://tudoreceitas.com'.
    returns a dict in the following format: title + n: link
    """
    url = 'http://tudoreceitas.com/pesquisa?q='

    def parse(self):
        soup = BeautifulSoup(self.data, 'lxml')
        recipes = soup.find_all('div', {'class': 'resultado link'})
        return self.to_dict(recipes)

    def to_dict(self, recipes):
        if recipes:
            return {recipe.find('a').text + ' - ' + str(i):
                    recipe.find('a')['href'] for i, recipe
                    in enumerate(recipes)}
        return {}


class RecipeScrapper:
    """
    Scrapes recipes asynchronously.
    Takes an arbitrary number of parsers classes, and a query as arguments
    """

    def __init__(self, parsers, q):
        self.parsers = parsers
        parser_url = namedtuple('ParserUrl', 'parser url')
        self.urls = [parser_url(p, p.url + q) for p in parsers]
        self.session = aiohttp.ClientSession()

    async def get_html(self, parser_url):
        "aync http request: returns a tuple with"
        async with self.session.get(parser_url.url) as response:
            html = await response.read()
            parser_html = namedtuple('ParserHtml', 'parser html')
            return parser_html(parser_url.parser, html)

    async def run_coroutines(self):
        tasks = []
        for url in self.urls:
            task = asyncio.ensure_future(self.get_html(url))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses

    def fetch_recipes(self):
        """
        fetch urls and return a list of tuples in the following form:
        (Parser: html)
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run_coroutines())
        loop.run_until_complete(future)
        loop.close()
        return future.result()

    def scrape(self):
        parsers_html = self.fetch_recipes()
        return [i.parser(i.html).parse() for i in parsers_html]
