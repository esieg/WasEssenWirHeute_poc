import os
import copy
import json
import random
import hashlib
from markdown_handler import get_properties

def get_recipes():
    '''Generate Recipe-Dict'''
    r_json = 'recipes.json'
    path = os.path.join(os.getcwd(), 'Recipes')
    mds = [md for md in os.listdir(path) if md.endswith('.md')]

    if(os.path.isfile(r_json)):
        with open(r_json, 'r', encoding='utf-8') as rj:
            recipes = json.loads(rj.read()) 
    else:
        recipes = dict()

    recipes_mds = list()
    for md in mds:
        md_path = os.path.join(path, md)
        name = md.replace('_', ' ')[:-3]
        with open(md_path, 'rb') as file_to_check:
            data = file_to_check.read()
            md5 = hashlib.md5(data).hexdigest()
        # check for new recipes and updates
        if not(name in recipes.keys() and recipes[name]['md5'] == md5):
            recipes[name] = get_properties(md_path)
            recipes[name]['md5'] = md5
        # later used for check of deleted recipes
        recipes_mds.append(name)

    # check for deleted names
    recipe_names = copy.deepcopy(recipes)
    for name in recipe_names.keys():
        if not(name in recipes_mds):
            del recipes[name]

    #write new recipes
    j_data = json.dumps(recipes, indent=2)
    with open(r_json, 'w', encoding='utf-8') as j_file:
        j_file.write(j_data)

    return(recipes)

def check_recipes(recipes, config):
    '''check recipes for properties'''
    selected_recipes = list()
    for recipe, properties in recipes.items():
        add = False if not(properties['diet'] in config['diet']) else True
        add = False if not(properties['kidsproofen'] or not(config['kidsproofen'])) else add
        add = False if not(properties['time_total'] <= config['time_total']) else add
        add = False if not(properties['time_cooking'] <= config['time_cooking']) else add
        if(add):
            selected_recipes.append(recipe)

    return(selected_recipes)

def choose_recipe(selected_recipes):
    '''choose available recipes by random'''
    choice = random.choice(selected_recipes)

    return(choice)