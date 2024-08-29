#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json

# add custom modules
sys.path.append(os.path.join(os.getcwd(), 'modules'))
from bom_handler import parse_ingredients, join_ingredients
from markdown_handler import parse_markdown
from recipe_handler import get_recipes, check_recipes, choose_recipe
from pdf_handler import merge_md_recipes, create_buylist, convert_md_to_pdf


if(__name__ == '__main__'):
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    recipes = get_recipes()
    selected_recipes = check_recipes(recipes, config)

    # check if we have enough recipes
    recipes_needed = config['recipes_needed'] if(config['recipes_needed'] <= len(selected_recipes)) else len(selected_recipes)

    # gather recipes by random
    recipe_files = list()
    ingredients_list = list()
    for recipe_counter in range(0, recipes_needed):
        choice = choose_recipe(selected_recipes)
        selected_recipes.remove(choice)
        md_path = os.path.join(os.getcwd(), 'Recipes', choice.replace(' ', '_') + '.md')
        ingredients = parse_markdown(md_path)
        ingredients_dict = parse_ingredients(ingredients)

        recipe_files.append(md_path)
        ingredients_list.append(ingredients_dict)
    
    joined_ingredients = join_ingredients(ingredients_list)

    recipes_md = merge_md_recipes(recipe_files)
    convert_md_to_pdf(recipes_md, 'recipes')
    buylist_md = create_buylist(joined_ingredients)
    convert_md_to_pdf(buylist_md, 'buylist')
    os.remove(recipes_md)
    os.remove(buylist_md)