from flask import Flask, request, jsonify
from recengine import ContentBasedFilter

app = Flask(__name__)


@app.route('/')
def index():
    return 'the endpoint is /getrec view the docs for help'


@app.route('/getrec', methods=['GET', 'POST'])
def get_recommendation():
    # POST requests should include the following:
    #       A JSON object of this form:
    #               data = {'newRecipes': [{'id': 'id0', 'title': 'tit0', 'summary': 'sum0text'},
    #                                      {'id': 'id1', 'title': 'tit1', 'summary': 'sum1text'},
    #                                      ...
    #                                      {'id': 'id19', 'title': 'tit19', 'summary': 'sum19text'}
    #                       'user': [{'id': 'id0', 'title': 'tit0', 'summary': 'sum0text', 'rating': '(0 or 1)'},
    #                               {'id': 'id1', 'title': 'tit1', 'summary': 'sum1text', 'rating': '(0 or 1)'}
    #                               ...
    #                               {'id': 'id24', 'title24': 'tit24', 'summary': 'sum24text', 'rating': '(0 or 1)'}]
    #               Note: A rating of 0 indicates the user disliked the recipe. Rating of 1 is a like.
    #       They must also include a header of this form:
    #               headers = {"Content-Type": "application/json"}
    if request.method == 'POST':
        rec = ContentBasedFilter.ContentBasedFilter(request.get_json())
        # print(rec)
        return '', 204
    elif request.method == 'GET':
        return "This is a POST only endpoint"


if __name__ == '__main__':
    app.run()