import taipy as tp
import pandas as pd
from taipy import Config, Scope, Gui

# Create a Taipy App that will output the 7 best movies for a genre

# Callback definition
def modify_df(state):
    scenario.selected_value_node.write(state.selected_value)
    tp.submit(scenario)
    state.df = scenario.filtered_data.read()    
# Filter function for Task
def filter_genre(initial_dataset: pd.DataFrame, selected_value):
    filtered_dataset = initial_dataset[initial_dataset['genres'].str.contains(selected_value)]
    filtered_data = filtered_dataset.nlargest(7, 'Popularity %')
    return filtered_data

# Loading the configuration
Config.load('config.toml')
scenario_cfg = Config.scenarios['scenario']

# Run of the Taipy Core service
tp.Core().run()

# Create a scenario for "Fantasy" genre
scenario = tp.create_scenario(scenario_cfg)

# Get list of genres
dataset = scenario.initial_dataset.read()
list_genres = list(dataset['genres'].str.split('|').explode().unique())

# Initialization of variables
df = pd.DataFrame(columns=['Title', 'Popularity %'])
selected_value = None

# My page
my_page = """
# Film recommendation

## Choose your favorite genre
<|{selected_value}|selector|lov={list_genres}|on_change=modify_df|dropdown|>

## Here are the top 7 picks
<|{df}|chart|x=Title|y=Popularity %|type=bar|title=Film Popularity|>
"""

Gui(page=my_page).run()
