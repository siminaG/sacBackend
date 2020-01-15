# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 20:59:33 2019

@author: anama
"""

import pandas as pd
import re
import ast
basic_ingredients = ['oil', 'milk', 'flower', 'butter', 'honey', 'beef', 'chicken', 'pork']

recipes = pd.read_csv('RAW_recipes.csv')
recipes = recipes[:20001]


def replace_func(ingredients):
    min = 0
    max = 99
    noToProcess = len(ingredients)
    while(max < noToProcess):
        batch_ingredients = ingredients[min:max]
        for i in batch_ingredients.index:
            for j in range(len(batch_ingredients[i])):
                for element in basic_ingredients:
                    if element in batch_ingredients[i][j]:
                        batch_ingredients[i][j] = element
        ingredients[min:max] = batch_ingredients
        if max == noToProcess - 1:
            break
        min = max
        if max + 100 > noToProcess - 1:
            max = noToProcess -1
        else:
            max = max + 100
    return ingredients

recipes = recipes.rename({'name': 'Title', 'id': 'Recipe_ID', 'ingredients': 'Ingredients', 'minutes': 'Time_to_Cook'}, axis = 1)
recipes_updated = recipes.drop([ 'contributor_id', 'submitted', 'tags', 'n_steps', 'steps', 'description', 'n_ingredients', 'nutrition'], axis = 1)
recipes_updated['Title'] = recipes_updated['Title'].str.title()
recipes_updated['Title'] = recipes_updated['Title'].astype(str)
recipes_updated['Title'] = [re.sub('[^ a-zA-Z]*','', title) for title in recipes_updated['Title']]
recipes_updated['Title'] = [" ".join(title.split()) for title in recipes_updated['Title'].values] 
recipes_updated['Title'] = [re.sub("^\s+|\s+$", "", title) for title in recipes_updated['Title']]
recipes_updated['Title'] = recipes_updated['Title'].drop_duplicates()
recipes_updated.drop(recipes_updated[recipes_updated['Title'].isnull() == True].index, inplace = True)

#print(recipes_updated[recipes_updated['Title'].isnull() == True])

#recipes.Ingredients.to_list()
recipes_updated.Ingredients = recipes_updated.Ingredients.apply(lambda x: ast.literal_eval(str(x)))
recipes_updated.Ingredients = [[re.sub('[^ a-zA-Z]*','', ingredient) for ingredient in ingredients] for ingredients in recipes_updated.Ingredients]
print("Started normalization process.....")
test = replace_func(recipes_updated['Ingredients'])
recipes_updated['Ingredients'] = test

#print(recipes_updated[recipes_updated['Recipe_ID'] == 385464])
# print(type(recipes['Ingredients'][0]))
print("Done normalizing!")
recipes_updated.to_csv('recipes_updated.csv')