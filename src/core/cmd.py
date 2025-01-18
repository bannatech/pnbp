'''
'  pnbp - pnbp is not a blogging platform
'  cmd.py - manages the commandline interface
'  Paul Longtine <paul@nanner.co>
'''

from optparse import OptionParser
import core.conf
import core.module


def parsearg():
    parser = OptionParser()

    parser.add_option("-m", "--modules", dest="module_dir", default=core.module.module_path,
                      help="module directory", metavar="<dir>")

    parser.add_option("-p", "--project", dest="dir", default=".",
                      help="project root directory", metavar="<dir>")

    parser.add_option("-o", "--output", dest="out", default="site",
                      help="output directory", metavar="<out>")

    parser.add_option("-r", "--remove", dest="removedir", action="store_true",
                      default=False, help="remove output directory automatically")

    parser.add_option("-i", "--init", dest="init", action="store_true",
                      default=False, help="initalize basic project directory")

    parser.add_option("-t", "--pagestype", dest="pagestype", metavar="(yml|json)",
                      default=core.conf.target_type, help="pages format")

    parser.add_option("-n", "--pagesname", dest="pagesname", metavar="<name>",
                      default=core.conf.target_name, help="pages name")

    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      default=False, help="verbose stderr output")

    return parser.parse_args()


basicConfig = """# Skeletal configuration
index:
  template: "template.html"
  pagevar:
    title: "I'm basic"
  pagemod:
    page:
      mod: page
"""

basicTemplate = """<!-- Skeletal configuration -->
<html>
 <body>
   <h1>%title%</h1>
 </body>
</html>"""


def writeBasicConfig():
    open("pages.yml", "w").write(basicConfig)
    open("template.html", "w").write(basicTemplate)
