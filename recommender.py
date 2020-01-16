# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:15:31 2019

@author: anama
"""

import pandas as pd
# import ast
# import re
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime

# recipes = pd.read_csv('recipes_updated.csv')
# user_data = {'User_ID': [], 'Recipe_ID': [], 'Recipe_liked_or_not': []}
# user_interactions = pd.DataFrame(user_data)

def get_user_input_ingred():
    print('Add your desired ingredients: ')
    list_ingredients = input().split(',')
    # conver to the list
    return list_ingredients

# def get_user_wanted_calories():
#     return input()

# print('Add your desierd ingredients: ')
# ingredient_list_from_user = get_user_input_ingred()
ingredient_list_from_user = [' apple', ' banana', ' flour', 'honey']
# print(ingredient_list_from_user)
#print('Select calories: ')
# calories_wanted_user = get_user_wanted_calories()
#print(calories_wanted_user, ingredient_list_from_user)

# query_user = [{'Recipe_ID': 0, 'Ingredients': ingredient_list_from_user}]
# recipes = recipes.append(query_user,ignore_index=True,sort=False)
# recipes['Ingredients']=["".join(ingredient) for ingredient in recipes['Ingredients'].values]
##print(df)
#print(recipes.Ingredients[:3])
#
# tfidf = TfidfVectorizer(analyzer = 'word', min_df = 0, stop_words = 'english')
# tfidf_matrix = tfidf.fit_transform(recipes['Ingredients'])
# print(tfidf_matrix)
# cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# indices = pd.Series(recipes.index, index=recipes['Ingredients']).drop_duplicates()

# validation = []
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
    # validation.append(sim_scores)
    recipes_indices = [i[0] for i in sim_scores]

    recommended_recipes_titles = recipes.iloc[recipes_indices].to_json(orient='records')
#    recommended_recipes_ingredients = recipes.iloc[recipes_indices]['Ingredients'].tolist()
    return recommended_recipes_titles
#, recipes['Ingredients'].iloc[recipes_indices]

print(datetime.now())
recommended_recipes = recommender(ingredient_list_from_user)
print(datetime.now())
print(recommended_recipes)
print('What recipe do you like to try?')
# print('Choose a recipe: ')
# recipe_chosen = input()
#
# program = 1
# while program == 1:
#     if recipe_chosen in recipes[recipes['Title'] == recipe_chosen]['Title'].to_string(index = False):
#         print("The list of ingredients that you need for the chosen recipe: ")
#         print(recipes[recipes['Title'] == recipe_chosen]['Ingredients'].to_string(index = False))
#         program = 0
#     else:
#         print('The recommended recipes are: ', recommended_recipes)
#         print('Type again the recipe that you want to try: ')
#         recipe_chosen = input()
#
# print('Validation scores: ', validation)
# recipes = recipes[recipes['Recipe_ID'] != 'Index_ingrediente']
