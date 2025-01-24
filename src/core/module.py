'''
'  pnbp - pnbp is not a blogging platform
'  module.py - implements the page module and the interface for loading modules
'  Paul Longtine <paul@banna.tech>
'''

import os
import sys
import imp
import core.template

base_module_path = os.path.join(os.path.dirname(__file__), "../modules")
module_path = ""
loaded_modules = {}


# Built-in module, generates page as subpage
def modPage(pageTemplate, pageDefinition, modDefinition, modName, pageName):
    if 'settings' in modDefinition and 'template' in modDefinition['settings']:
        templateFile = modDefinition['settings']['template']

        try:
            temp = open(templateFile).read()
        except Exception as e:
            ex = f"Error occured at {pageName} using module page: failed to open file {templateFile}: {e}"
            raise Exception(ex)

    else:
        temp = pageTemplate

    pagevar = {}
    if 'pagevar' in pageDefinition:
        pagevar = pageDefinition['pagevar']

        if 'settings' in modDefinition and 'pagevar' in modDefinition['settings']:
            pageDefinition['pagevar'].update(modDefinition['settings']['pagevar'])

    temp = core.template.generate(temp, pagevar, pageName)

    if 'settings' in modDefinition and 'location' in modDefinition['settings']:
        loc = modDefinition['settings']['location']
        if len(loc.split('.')) > 0:
            page = {
                loc: temp
            }
        else:
            page = {
                loc: {
                    'index': temp
                }
            }
    else:
        page = {
            'index': temp
        }

    return page


def getModule(module_name):
    if module_name not in loaded_modules:
        module_py = f"{module_name}.py"
        module_fname = os.path.join(base_module_path, module_py)
        if os.path.exists(module_fname) is False and module_path != "":
            module_fname = os.path.join(module_path, module_py)

        if os.path.exists(module_fname) is False:
            raise Exception(f"Module not found: '{module_name}'")

        loaded_modules[module_name] = imp.load_source(module_name, module_fname)

    return loaded_modules[module_name]


# Runs modules defined in pages.json
#
def run(pageTemplate, pageDefinition, pageName):
    subpage = {}
    for modName, modDefinition in pageDefinition['pagemod'].items():
        modType = modDefinition['mod']
        if modType == "page":
            mergeSubpages(
                subpage,
                modPage(
                    pageTemplate,
                    pageDefinition,
                    modDefinition,
                    modName,
                    pageName
                )
            )

        else:
            mergeSubpages(
                subpage,
                getSubpages(
                    pageTemplate,
                    pageDefinition,
                    modDefinition,
                    modName,
                    pageName
                )
            )

        if 'index' in subpage:
            pageTemplate = subpage['index']

    return subpage


# Gets subpages from module specified in data
def getSubpages(pageTemplate, pageDefinition, modDefinition, modName, pageName):
    returns = {}
    settings = {}
    if "settings" in modDefinition:
        settings = modDefinition['settings']

    module_name = modDefinition['mod']

    module = getModule(module_name)
    if module is not None:
        getPages = getattr(module, 'getPages')
        try:
            returns = getPages(pageTemplate, settings, modName, pageName)
        except Exception as e:
            raise Exception(f"Error occured at {pageName} using module {module_name}: {e}")
    else:
        raise Exception(f"No such module {module_name}")

    return returns


def mergeSubpages(subpages, newpages):
    for page, content in newpages.items():
        if page in subpages and isinstance(subpages[page], dict) and isinstance(newpages[page], dict):
            mergeSubpages(subpages[page], newpages[page])
        else:
            subpages[page] = newpages[page]
