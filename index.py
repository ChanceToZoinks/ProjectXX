from flask import Flask, request, jsonify
from recengine import ContentBasedFilter
from projectXhelpers import FileWriterHelper
import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
    return 'the endpoint is /getrec view the docs for help'


@app.route('/getrec', methods=['GET'])
def generate_rec_payload():
    # grab 25 user recipes from db here
    current_user_id = request.args.get('userID')
    current_ingredient = request.args.get('ingredient')
    like = 2
    dislike = 1
    fake_payload = {'newRecipes': [{'id': '2245', 'title': 'Banana Bread Story', 'summary': 'The banana went to the bread store.'},
                          {'id': '1234', 'title': 'Cows', 'summary': 'Steak is made from cows. Cows eat grass and bananas. They also like bread.'},
                          {'id': '2345', 'title': 'Pumpkin Soup', 'summary': 'Some random shit about pumpkins.'},
                          {'id': '2545', 'title': 'Cranberry Crepes', 'summary': 'Some random shit about Crepes maybe something about bananas.'},
                          {'id': '23545', 'title': 'White Russian', 'summary': '1.5oz vodka, .5oz khalua, top with cream add ice serve.'},
                          {'id': '1345', 'title': 'Cheese Pizza', 'summary': 'An italian bread dish made with cheese and tomato sauce.'},
                          {'id': '234545', 'title': 'Banana Cheese Bagel', 'summary': 'Cheese and bagels and bananas.'},
                          {'id': '254', 'title': 'Banana', 'summary': 'Banana banana banana banana banana.'},
                          {'id': '264', 'title': 'Ba', 'summary': 'Wow.'},
                          {'id': '274', 'title': 'B', 'summary': 'This is a sentence.'},
                          {'id': '284', 'title': 'Bna', 'summary': 'Im so funny hehe lele.'},
                          {'id': '294', 'title': 'Deer', 'summary': 'Im losing it'},
                          {'id': '204', 'title': 'Cook', 'summary': 'Hoop doop.'},
                          {'id': '2004', 'title': 'Meme', 'summary': 'Gucci gang.'},
                          {'id': '20004', 'title': 'Linux', 'summary': 'Give me a big juicy steak.'},
                          {'id': '2304', 'title': 'Orgeat', 'summary': 'Banana split.'},
                          {'id': '23984', 'title': 'Zoop', 'summary': 'Yeet.'},
                          {'id': '23094', 'title': 'Zip', 'summary': 'Random garbage.'},
                          {'id': '23134', 'title': 'Cobol', 'summary': 'This steak is really dry.'},
                          {'id': '21134', 'title': 'Meme', 'summary': 'Banana.'},
                          ],
           'user': [{'id': '3', 'title': 'Banana Bread', 'summary': 'The banana went to the market.', 'rating': like}, {'id': '5', 'title': 'Chicken Piccata', 'summary': 'A chicken dish made with white wine, butter and capers.', 'rating': dislike}, {'id': '1', 'title': 'Spaghetti Bolagnese', 'summary': 'A pasta dish made with tomatoes, bananas, and cows.', 'rating': like}]}

    # check if user is in storage yet
    if FileWriterHelper.user_in_dict_yet(current_user_id):
        print('user in table')
        fake_payload['user'] = FileWriterHelper.get_user_data(current_user_id)
    else:
        FileWriterHelper.add_user(current_user_id)
        for i in range(20):
            FileWriterHelper.add_dict_data(userID=current_user_id, data_dict=
                {'id': 'id{0}'.format(i), 'title': 'title{0}'.format(i), 'summary': 'summary{0}'.format(i), 'rating': 1}
            )
        FileWriterHelper.write_to_disk()
    # grab the user previous stuff

    try:
        return get_recommendation(fake_payload)
    except TypeError:
        return get_recommendation(fake_payload)


def get_recommendation(payload):
    # POST requests should include the following:
    #       A JSON object of this form:
    #               data = {'newRecipes': [{'id': 'id0', 'title': 'tit0', 'summary': 'sum0text'},
    #                                      {'id': 'id1', 'title': 'tit1', 'summary': 'sum1text'},
    #                                      ...
    #                                      {'id': 'id19', 'title': 'tit19', 'summary': 'sum19text'}
    #                       'user': [{'id': 'id0', 'title': 'tit0', 'summary': 'sum0text', 'rating': '(1 or 2)'},
    #                               {'id': 'id1', 'title': 'tit1', 'summary': 'sum1text', 'rating': '(1 or 2)'}
    #                               ...
    #                               {'id': 'id24', 'title24': 'tit24', 'summary': 'sum24text', 'rating': '(1 or 2)'}]
    #               Note: A rating of 1 indicates the user disliked the recipe. Rating of 2 is a like.
    #       They must also include a header of this form:
    #               headers = {"Content-Type": "application/json"}
    content_filter = ContentBasedFilter.ContentBasedFilter(payload)
    rec_json = content_filter.get_recommendation()

    summaries = []
    for i in json.loads(rec_json):
        r = requests.get('https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/{0}/summary'
                         .format(i['id']),
                         headers={
                                    "X-Mashape-Key": "oI6ulLorQ9mshxcUvqtwliyhi76cp15sxUDjsncRWnh7gRvIYA",
                                    "Accept": "application/json"
                                })
        summaries.append(r.json())
    print(summaries)
    return jsonify(summaries), 200


@app.route('/getinstructions', methods=['GET'])
def get_recipe_instructions():
    pass

if __name__ == '__main__':
    app.run()