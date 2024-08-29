import os
import re
import pypandoc
from PIL import Image

def get_images_scale(line, max_width, max_height):
    '''get image, get their width and heigth and scale them for a nice looking print'''
    if('./Bilder/' in line):
        path_start = line.find('(./') + 3
        path_end = line.find('.jpg') + 4
        path = os.path.join(os.getcwd(), 'Recipes', line[path_start:path_end])
        
        im = Image.open(path)
        width, height = im.size 
        # check if scaling is necessary
        w_scale = width/max_width
        h_scale = height/max_height
        scale = w_scale if(w_scale > h_scale) else h_scale
        # scale
        if(scale > 1):
            width /= scale
            height /= scale
        # convert width ad heigth to target format
        width = f'{int(width)}px' 
        height = f'{int(height)}px' 
    else:  
        # if not needed, make the variable by default empty
        width=''
        height=''

    return(width, height)

def adjust_image(recipes_file):
    '''add "./recipes" before imagepath and add a width and height'''
    pattern = r'\!\[.*?\]\(\./Bilder/(.*?\.jpg)\)'
    replacement_base = './Recipes/Bilder/'

    max_width = 500 #px
    max_height = 300 #px

    with open(recipes_file, 'r') as in_file:
        lines = in_file.readlines()

    with open(recipes_file, 'w') as out_file:
        out_file.write(r'\renewcommand{\figurename}{Fig.}')
        for line in lines:
            width, height = get_images_scale(line, max_width, max_height)
            new_line = re.sub(pattern, fr'![\1]({replacement_base}\1){{ width={width} height={height} }}', line)

            out_file.write(new_line)

    return(recipes_file)

def merge_md_recipes(recipe_files):
    '''merge the MarkDown-Files for our choosen Recipes to a single one'''
    recipes = os.path.join(os.getcwd(), 'recipes.md')
    newpages = len(recipe_files) - 1

    with open(recipes, 'w') as recipes_file:
        for counter, recipe_file in enumerate(recipe_files):
            with open(recipe_file, 'r') as rec_file:
                content = rec_file.read()
                recipes_file.write(content)
                # add newpage between every file
                if(counter < newpages):
                    recipes_file.write('\n\n\\newpage\n\n')

    adjust_image(recipes)

    return(recipes)

def create_buylist(joined_ingredients):
    '''create buylist-Markdown from given joined_ingredients'''
    buylist_md = os.path.join(os.getcwd(), 'buylist.md')

    # create two string for buylist
    ingredients_string = '\n\n'
    optional_string = '\n\n'

    for ingredient in joined_ingredients:
        #get all pieces of the ingredient
        ing_optional = joined_ingredients[ingredient]['optional']
        ing_unit = joined_ingredients[ingredient]['unit']
        ing_amount = joined_ingredients[ingredient]['amount']
        ing_name = ingredient.replace('opt_', '').replace(f'_({ing_unit})', '')
        # connect the pieces to a line
        ing_string = f'{ing_amount} ' if (ing_amount != 0) else ''
        ing_string = f'{ing_string}{ing_unit} ' if (ing_unit != '') else ing_string
        ing_string = f'* {ing_string}{ing_name}\n' if(ing_string != '') else f'* {ing_name}\n'

        # add the line to the right text
        if(ing_optional):
            optional_string += ing_string
        else:
            ingredients_string += ing_string

    # create the md file
    md_content = f'# Einkaufsliste\n\n## Zutaten{ingredients_string}\n\n## optionale Zutaten{optional_string}'
    with open(buylist_md, 'w') as blmd:
        blmd.write(md_content)

    return(buylist_md)

def convert_md_to_pdf(in_md, out_type):
    '''convert markdownfile to pdf'''
    out_pdf = os.path.join(os.getcwd(), f'{out_type}.pdf')
    pypandoc.convert_file(in_md, 'pdf', outputfile=out_pdf, encoding='utf-8')
