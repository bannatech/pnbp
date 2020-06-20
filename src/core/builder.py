'''
'  pnbp - pnbp is not a blogging platform
'  builder.py
'  Paul Longtine <paul@nanner.co>
'''

import os
import sys

import core.template
import core.module


# Orchestrate templating by iterating pd, which contains the necessary data to
# define a set of root pages.
def build(pd):
    site = {}
    for pageName, pageDefinition in pd.items():
        genTemplate = ""
        if 'template' in pageDefinition:
            template = ""
            templateFile = pageDefinition['template']
            try:
                template = open(templateFile).read()
            except Exception as err:
                ex = f"{pageName}: Can't open file '{templateFile}': {err}"
                raise Exception(ex)

            pagevar = {}
            if 'pagevar' in pageDefinition:
                pagevar = pageDefinition['pagevar']
            genTemplate = core.template.generate(template, pagevar, pageName)

        print(f"Running modules for page: '{pageName}'")
        site[pageName] = core.module.run(genTemplate, pageDefinition, pageName)
        print(f"Built page: '{pageName}'\n")

    return site
