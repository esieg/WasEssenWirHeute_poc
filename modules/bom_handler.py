import re

def parse_ingredients(ingredients):
    '''Get all needed ingredients out of the recipe'''
    unit_markers = ['gr', 'gramm', 'kilo', 'ml', 'l', 'Tube', 'Laib', 'Dose', 'EL', 'Packung', 'Stück', 'TL', 'Messerspitzen', 'Prise', 'Schuss', 'cm', 'g', 'Glas']

    ingredients_dict = dict()
    for ingredient in ingredients:
        # convert optional to opt.
        ingredient = ingredient.replace('optional','opt.').strip()
        # convert units and to unit names
        ingredient = ingredient.replace('Pkg.','Packung').strip()
        ingredient = ingredient.replace('Packungen','Packung').strip()
        ingredient = ingredient.replace('Pack ','Packung').strip()
        ingredient = ingredient.replace('Esslöffel','EL').strip()
        ingredient = ingredient.replace('Teelöffel','TL').strip()
        ingredient = ingredient.replace('Prisen','Prise').strip()
        ingredient = ingredient.replace('gr.', 'gr')
        ingredient = ingredient.replace('EL.', 'EL')
        # convert german , to englisch .
        #ingredient = re.sub(r'(\d+),(\d+)', r'\1.\2', ingredient)

        opt = False
        if('opt.' in ingredient):
            opt = True
            ingredient = ingredient.replace('opt.', '').lstrip()
        amount_search = re.search(r'\d+', ingredient)
        amount = int(amount_search.group()) if amount_search else 0
        unit_search = re.search(r'\b(?:' + '|'.join(map(re.escape, unit_markers)) + r')\b', ingredient)
        unit = unit_search.group() if unit_search else ''
        # replace with ' ' is needed, else a "g" or "l" in the ingredient after g or l as unit will also be replaced
        ingredient = ingredient.replace(str(amount), '').replace(f'{unit} ', '').strip()
        if len(ingredient):
            ingredients_dict[ingredient] = {'amount': amount, 'unit': unit, 'optional': opt} 

    return(ingredients_dict)

def join_ingredients(ingredients_list):
    '''join all the ingredients from former get_incredents'''
    joined_ingredients = dict()

    for ingredient_list in ingredients_list:
        for ingredient in ingredient_list:
            # first, check if ingredient is optional, if so, add prefix 'opt_'
            if(ingredient_list[ingredient]['optional']):
                joined_ingredient_name = f'opt_{ingredient}'
            else:
                joined_ingredient_name = ingredient
            #check if ingredient is already in the joined_dict, if not, append directly
            if(joined_ingredient_name in joined_ingredients.keys()):
                #if, we have to check for the unit
                unit_joined = joined_ingredients[joined_ingredient_name]['unit']
                unit_ingredient = ingredient_list[ingredient]['unit']
                # if they are the same, we can add the amount
                if(unit_joined == unit_ingredient):
                    joined_ingredients[joined_ingredient_name]['amount'] += ingredient_list[ingredient]['amount']
                # else, we need a evasive_ingredient and have to check, if this is also yet existing
                else:
                    evasive_ingredient = f'{joined_ingredient_name}_({unit_ingredient})'
                    if(evasive_ingredient in joined_ingredients.keys()):
                        joined_ingredients[evasive_ingredient]['amount'] += ingredient_list[ingredient]['amount']
                    else:
                        joined_ingredients[evasive_ingredient] = ingredient_list[ingredient]
            else:
                joined_ingredients[joined_ingredient_name] = ingredient_list[ingredient]

    return(joined_ingredients)