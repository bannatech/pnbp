description: A quick guide to start using pnbp
post: '0'
title: Getting Started

%=%
### Welcome!

To get started using pnbp, you need to configure your first site.

With pnbp, there's a specific directory structure that is at the base of every
site.

It looks something like this:

    |- pages.yml
    |
    |-- data
       \ - static

#### `pages.yml`

This file specifies every page that's created, along with what template
directories/files are going to be used. If no templates are specified,
`templates/` is assumed as the default template directory.

#### `data`

This is where all the information regarding any module will be kept.

#### `data/static`

The static directory is what will be added into the root directory of the site
when built. This is used for things such as cat pictures, cgi scripts and styles
for the site.

So far, this site wouldn't generate anything.

To get a working site, we need [configure one](/docs/post/site_configuration)
