from flask import Flask, request, abort
from flask_cors import CORS
import pymongo
from json import dumps
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
CORS(app)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["sac"]

def recommender(list_ingredients):
    recipes = pd.read_csv('recipes_updated.csv')
    query_user = [{'Recipe_ID': 0, 'Ingredients': list_ingredients}]
    recipes = recipes.append(query_user, ignore_index=True, sort=False)
    recipes['Ingredients'] = ["".join(ingredient) for ingredient in recipes['Ingredients'].values]

    tfidf = TfidfVectorizer(analyzer='word', min_df=0, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(recipes['Ingredients'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(recipes.index, index=recipes['Ingredients']).drop_duplicates()

    idx = indices.iloc[-1]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]
    recipes_indices = [i[0] for i in sim_scores]

    recommended_recipes = recipes.iloc[recipes_indices].to_json(orient='records')
    print(recommended_recipes)
    return recommended_recipes

def addSpace(word):
    string2 = word
    string_length = len(string2) + 1  # will be adding 1 extra space
    return string2.rjust(string_length)

@app.route("/login", methods=['POST'])
def login():
    mycol = mydb["user"]
    mydoc = mycol.find_one({"email": request.json['email']})
    if mydoc is not None:
        if mydoc['password'] == request.json['password']:
            # print('parola buna')
            return "OK"
        else:
            # print('parola gresita')
            abort(403)
    else:
        # print('fara user bun')
        abort(403)


@app.route("/register", methods=['POST'])
def register():
    mycol = mydb["user"]
    mydict = request.json
    mycol.insert_one(mydict)
    return "OK"

@app.route("/ingredients", methods=['POST'])
def post_ingredients():
    mycollection = mydb["user"]
    ingredients = request.json[0]
    email = request.json[1]
    # mydoc = mycollection.find_one({"email": email})
    mycollection.update_one({"email": email}, {"$set": {"ingrdients": ingredients}})
    result = map(addSpace, ingredients)
    # suggestedRecipes = recommender(result)
    # return dumps(str(suggestedRecipes))
    return recommender(result)


if __name__ == '__main__':
    app.run()
