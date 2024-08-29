def parse_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()

    ingredients = list()
    current_part = ''

    for line in content.split('\n'):
        if('## Zutaten' in line):
            current_part = 'Zutaten'
        elif('##' in line):
            current_part = ''
        elif(current_part == 'Zutaten'):
            ingredient = line.strip().replace('* ', '')
            if(len(ingredient)):
                ingredients.append(ingredient)

    return(ingredients)

def get_properties(md_path):
    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()

    properties = dict()
    props = False

    for line in content.split('\n'):
        if('## Eigenschaften' in line):
            props = True
        elif(props):
            value = line.split(' ')[-1]
            if('Ernährung' in line):
                properties['diet'] = value
            elif('Kinderfreundlich' in line): 
                eval = True if(value == 'Ja') else False
                properties['kidsproofen'] = eval
            elif('Gesamtzeit' in line): 
                properties['time_total'] = int(value)
            elif('Zubereitungszeit' in line): 
                properties['time_cooking'] = int(value)

    return(properties)