'''
'  pnbp - pnbp is not a blogging platform
'  module.py - implements the page module and the interface for loading modules
'  Paul Longtine <paul@banna.tech>
'''

import os
import sys
import importlib.util

import core.template

# Built-in module, generates page as subpage
class PageMod:
    @staticmethod
    def getPages(pageTemplate, pageDefinition, modDefinition, modName, pageName):
        if 'template' in modDefinition:
            templateFile = modDefinition['template']

            try:
                temp = open(templateFile).read()
            except Exception as e:
                ex = f"Error occured at {pageName} using module page: failed to open file {templateFile}: {e}"
                raise Exception(ex)

        else:
            temp = pageTemplate

        pagevar = {}
        if 'pagevar' in pageDefinition:
            pagevar.update(pageDefinition['pagevar'])

        if 'pagevar' in modDefinition:
            pagevar.update(modDefinition['pagevar'])

        temp = core.template.generate(temp, pagevar, pageName)

        if 'location' in modDefinition:
            loc = modDefinition['location']
            if len(loc.split('.')) > 0:
                page = {loc: temp}
            else:
                page = {loc: {'index': temp}}
        else:
            page = {'index': temp}

        return page


def getModule(module_name):
    if module_name in loaded_modules:
        module = loaded_modules[module_name]
    else:
        module_py = f"{module_name}.py"

        # Resolve the file path – try base first, then fallback if needed
        module_fname = os.path.join(base_module_path, module_py)
        if not os.path.exists(module_fname) and module_path:
            module_fname = os.path.join(module_path, module_py)

        if not os.path.exists(module_fname):
            raise Exception(f"module not found: '{module_name}'")

        # Create a module spec and load the module
        spec = importlib.util.spec_from_file_location(module_name, module_fname)
        if spec is None or spec.loader is None:
            raise Exception(f"could not create import spec for module '{module_name}'")

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise Exception(f"error loading module '{module_name}': {e}")

        loaded_modules[module_name] = module

    return module

base_module_path = os.path.join(os.path.dirname(__file__), "../modules")
module_path = ""
loaded_modules = {'page':PageMod}

# Runs modules defined in pages.json
#
def run(pageTemplate, pageDefinition, pageName):
    subpage = {}
    for modName, modDefinition in pageDefinition['pagemod'].items():
        mergeSubpages(subpage, getSubpages(
            pageTemplate,
            pageDefinition,
            modDefinition,
            modName,
            pageName
        ))

        if 'index' in subpage:
            pageTemplate = subpage['index']

    return subpage


# Gets subpages from module specified in data
def getSubpages(pageTemplate, pageDefinition, modDefinition, modName, pageName):
    returns = {}
    settings = modDefinition.get('settings', {})
    module_name = modDefinition['mod']
    module = getModule(module_name)
    if module is not None:
        getPages = getattr(module, 'getPages')
        try:
            returns = getPages(pageTemplate, pageDefinition, settings, modName, pageName)
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
