description: Specifications on the Site config file
post: '1'
title: Site configuration

%=%
For every page, there's an entry in the pages.yml file specifying the template,
module and page-variables/includes.

A basic pages.yml:

    (pagename):
      template: "templates/standard.html"
      pagevar:
        $include: "includes/include.html"
        var: "Variable"
      pagemod:
        (modid):
          mod: "page"
    (pagename):
      template: "templates/other.html"
      pagevar:
        title: "pnbp"
      pagemod:
        (modid):
          mod: "page"
          settings:
            location: "space"

### `(pagename)`

This specifies the name and location of the page.

"index" is a special term used to define the home page of the website, thus
creating this page in the root of the website.

### [`template`](/docs/post/templates_and_includes/)

This specifies the location of the template that is going to be used in this
page.

### `pagevar`

These are the variables that are specified in the templates to be replaced with
the values specified.

Includes are specified with a `$` character at the beginning of the name of the
variable, followed by the the value being the location of the file to include.

### `pagemod`

This is a specialized set of variables, pointing to a module that can create
subpages.

`(modid)` is used for the id of the module that is being used. This may be used
in different ways for different modules.

For information on the use of `(modid)`, refer to the module being used.
