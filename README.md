# WasEssenWirHeute_poc
Simple App (currently CLI only) for planning the next meals 

## Purpose
This app is designed to answer the well-known question “What are we eating today”. The reponame is in German and that is exactly what the name means

## Installation

First, please install the programs [pandoc](https://pandoc.org/installing.html) and a Tex-Engine (on my Mac I use [BasicTex](https://tug.org/mactex/morepackages.html)). Make sure you have at least Python 3.7 installed and install the necessary requirements:

`pip install -r requirements.txt`

## Configuration
In the config.json you set how you want the dishes to be. 

I have provided the following settings for this:
* recipes_needed - the number of dishes that the program should select for you. But be careful, if you have only collected 15 dishes as specified and ask for 20, only 15 dishes will be selected. No recipe will be selected twice.
* diet - I use this to differentiate between vegetarian and vegan recipes. You could also add other tags here, e.g. gluten-free, organic, with meat or whatever else you need. In the recipe files there is the tag Ernährung. 
* kidsproofen - A particularly important property field for a family man. It is Boolean, i.e. it knows “true” and “false” and describes whether the recipe is suitable for your children or not.
* time_total: From chopping vegetables to cooking in the oven or leaving to infuse for half a day, the maximum total time for the meal is set here.
* time_cooking: And here, how long you really need to be active during preparation.

## The recipe
The recipes are structured according to a simple scheme and are stored in the “Recipes” folder. A photo of each recipe is also stored in the “Pictures” folder. We choose Markdown as the format, with the file extension “md”. 

The recipes are organized as follows:
* Title
* Picture
* Ingredients (Zutaten)
* Preparation (Zubereitung)
* Properties (Eigenschaften)

In the ingredients section you can enter \<amount\> \<quantity\> (i.e. gr., can, etc.) \<ingredient\>. In bom.py you will see all the quantities I have needed so far on line 5. You are welcome to extend the list.  You can also write the ingredients directly (salt), without quantity and quantities or just the ingredient with a quantity (1 loaf). And you can add the "opt." flag. So the ingredient will be marked as "optional".

## Architecture and further development
As written in another corner of the internet, this was a weekend project (with 35 recipes to enter) for my girlfriend that she understands how computer programs are programmed. Accordingly, everything is kept very simple and unfortunately has no architecture, the names are not really consistent, the modules are not sophisticated and overall I would like to make everything a bit more dynamic and not hide variable declarations like the quantity in a file. And a GUI for entering recipes, for configuring and executing the app and a free stand so that people without Python can get started right away. At the moment I am starting a larger project that is very close to my heart and then I will certainly want to continue here again. Until then, feel free to make suggestions or write one or two commits yourself.

**What is important to me is that the project remains open source and I will keep it free.**