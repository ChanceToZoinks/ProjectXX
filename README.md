# RecetteIO

>All requests should be made to the endpoint chancetofreeze.pythonanywhere.com/getrec
>
>POST requests should include the following:
>         A JSON object of this form:
>                 data = {'newRecipes': [{'id': 'id0', 'title': 'tit0', 'summary': 'sum0text'},
>                                        {'id': 'id1', 'title': 'tit1', 'summary': 'sum1text'},
>                                        ...
>                                        {'id': 'id19', 'title': 'tit19', 'summary': 'sum19text'}
>                         'user': [{'id': 'id0', 'title': 'tit0', 'summary': 'sum0text', 'rating': '(1 or 2)'},
>                                 {'id': 'id1', 'title': 'tit1', 'summary': 'sum1text', 'rating': '(1 or 2)'}
>                                 ...
>                                 {'id': 'id24', 'title24': 'tit24', 'summary': 'sum24text', 'rating': '(1 or 2)'}]
>                 Note: A rating of 1 indicates the user disliked the recipe. Rating of 2 is a like.
>                 The 'newRecipes' key refers to a list containing dicts with each dict corresponding to a recipe.
>                 Likewise, 'user' refers to a list containing dicts with each dict being a recipe.
>                 There should be a maximum of 20 new recipes sent and 25 user rated recipes.
>         They must also include a header of this form:
>                 headers = {"Content-Type": "application/json"}
