from flask import Flask, request, jsonify
from scrapper.recipes import TudoGostoso, TudoReceitas

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def show_recipes():
    q = request.args.get('q')
    tg = TudoGostoso(q)
    tr = TudoReceitas(q)
    # res = {**tg.results, **tr.results}
    return jsonify([tg.results, tr.results])


if __name__ == '__main__':
    app.run()
