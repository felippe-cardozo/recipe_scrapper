from flask import Flask, request, jsonify
from scrapper.recipes import TudoGostoso, TudoReceitas, RecipeScrapper

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def show_recipes():
    q = request.args.get('q')
    parsers = [TudoGostoso, TudoReceitas]
    scrapper = RecipeScrapper(parsers, q)
    return jsonify(scrapper.scrape())


if __name__ == '__main__':
    app.run()
