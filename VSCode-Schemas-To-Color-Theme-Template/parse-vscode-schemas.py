#!/usr/bin/env python3
# please Python 3.7 >

# Epically parses the .json files in /resources to create a mostly complete color theme template


import json


theme_name = "theme-template"
output_file = theme_name + ".json"

use_comments = False # ig technically vscode themes are JSON5 even though they still use .json ?
                    # comment out semantic and textmate token colors if they are included since they don't
                    # support using "default" as a value
use_semantic_colors = True # these 2 options can be used at the same time
use_textmate_colors = True

workbench_colors = "resources/workbench-colors.json" # editor colors (not syntax highlighting)
token_styling = "resources/token-styling.json" # language specific syntax highlighting provided by extensions
textmate_colors = "resources/textmate-colors.json" # TextMate based syntax highlighting (built-in)

template = {
    "name": theme_name,
    "colors": {}, # from workbench_colors
    "semanticHighlighting": use_semantic_colors,
    "semanticTokenColors": {}, # from token_styling
    "tokenColors": [] # from textmate_colors
}


with open(workbench_colors, "r") as file_json:
    data = json.load(file_json)["properties"]

    for key, value in data.items():
        template["colors"][key] = "default"

if use_semantic_colors:
    with open(token_styling, "r") as file_json:
        data = json.load(file_json)["properties"]

        for key, value in data.items():
            # this might be a little hacky but it works very cleanly, we just switch the quotation mark and
            # comment indicator around later, after the JSON is dumped to a string, or remove the indicator
            template["semanticTokenColors"]["//" + key] = "#FFFFFF"

if use_textmate_colors:
    with open(textmate_colors, "r") as file_json:
        data = json.load(file_json)
        scopes = list(data["items"]["properties"]["scope"]["anyOf"][0]["enum"])
        names = {} # seperate the scopes by the first part of the selector (up to the first period)

        for item in scopes:
            key = item.split('.')[0]

            if not key in names:
                names[key] = []

            names[key].append(item)

        for name in names:
            color_object = {
                "name": name,
                "scope": names[name],
                "settings": {
                    "//foreground": "#FFFFFF",
                    #"//background": "#000000FF", # not yet supported? default to transparent in future
                    "//fontStyle": ""
                }
            }

            for index, value in enumerate(color_object["scope"]):
                color_object["scope"][index] = "//" + value

            template["tokenColors"].append(color_object)

with open(output_file, "w+") as file_json:
    string_buffer = json.dumps(template, indent = 4).replace("\"//", "//\"" if use_comments else "\"")
    file_json.write(string_buffer)
