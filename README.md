pnbp
====

pnbp is a simple, scriptable and extendable platform to generate static websites with simple configuration and dynamic content.

I can't possibly use someone elses software for static website generation, so I made my own.

***

#Installing

##Dependencies:

* Python 2.x

* pyyaml (`pip install pyyaml`)

##How to install

  # Clone the repository
  $ git clone https://github.com/bannana/pnbp.git
  
  $ cd pnbp
  # Install pnbp
  $ sudo sh install.sh
  
#Basic usage

In the directory of a configured site, run the `build` command to generate the site into the `site/` directory.

To specify the destination directory, pass the path in as an arguement of the `build [path]` command.

For information regarding configration documentation, please refer to the [documentation](http://pnbp.nanner.co).
