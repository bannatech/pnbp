# pnbp

pnbp is a simple, scriptable and extendable platform to generate static websites
with simple configuration and dynamic content.

I can't possibly use someone elses software for static website generation, so I
made my own.

# Installing

## Dependencies:

* Python 3.x

* [pyyaml](https://pypi.org/project/PyYAML/)

* [markdown](https://python-markdown.github.io/)

## How to install

You may configure `BINDIR` and `PREFIX` to your preference. The default is
in `/usr/local/lib` and `/usr/local/bin` respectively.

```bash
# Clone the repository
$ git clone https://github.com/bannatech/pnbp.git
  
$ cd pnbp
# Install pnbp
$ sudo make install
```

# Basic usage

To set up a basic site, run `pbuild -i`

For information regarding configration documentation, please refer to the
[documentation](http://pnbp.nanner.co). (which is very sparse)

# Building the documentation

Contained in this repository is an `example` project which may be used to build
something more complex than what is generated with `pbuild -i`. It is also the
way the documentation site is built!

After installing `pnbp`, you may run `pbuild` in the `example` site:

```
$ pnbp
using directory '.'
WRITE 0ba9cb260a29ef71c1fa812bf6e16c124e0012de0c77163befb71cd492a279b8 site/index.html 832
WRITE 36ebfb7b6a014e3fc1210a6296ddb87da4424f3bca32a9b981dba4ab569a4f86 site/docs/index.html 826
WRITE 48467552f5cd73c8513749abfe71a5ad71e28d2930ec3f7aa1ad656cbfbd00c6 site/docs/post/getting_started/index.html 1538
WRITE d4466bd591ceca018d91e2dabcc4708e66d1d2be62a47a5b7bfda3d9840a4945 site/docs/post/site_configuration/index.html 2097
WRITE 5cb5c7b441c4ce47dc9cb667893832a00c43e25ff1aee67fdec63c315000f494 site/docs/post/templates_and_includes/index.html 960
COPY 50eb1b3d8f245dea18e442d70e3dc9e5bf896e547a7333ac8a7e204d2d25e55d site/styles/style.css 298
generated 7 files across 6 dirs in 23.888292 ms
```

The content of the site is read from a set of JSON files at `example/data/json`.

If any file under `example/data/sources` is modified, the `example/data/json`
files can be generated with the `example/packContent.py` script:

```
$ cd example
$ ./packContent.py
wrote 'data/json/docs.json'
wrote 'data/json/index.json'
packed sources
```



