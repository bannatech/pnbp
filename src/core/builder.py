'''
'  pnbp - pnbp is not a blogging platform
'  builder.py
'  Paul Longtine <paul@banna.tech>
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
            temp = ""
            tempFile = pageDefinition['template']
            try:
                temp = open(tempFile).read()
            except Exception as err:
                ex = f"{pageName}: Can't open file '{tempFile}': {err}"
                raise Exception(ex)

            pagevar = {}
            if 'pagevar' in pageDefinition:
                pagevar = pageDefinition['pagevar']
            genTemp = core.template.generate(temp, pagevar, pageName)

        site[pageName] = core.module.run(genTemp, pageDefinition, pageName)

    return site
