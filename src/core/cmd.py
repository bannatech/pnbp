'''
'  pnbp - pnbp is not a blogging platform
'  cmd.py - manages the commandline interface
'  Paul Longtine <paul@banna.tech>
'''

from optparse import OptionParser
import core.conf
import core.module


def parsearg():
    parser = OptionParser()

    parser.add_option("-m", "--modules", dest="module_dir", default="",
                      help="module directory", metavar="<dir>")

    parser.add_option("-p", "--project", dest="dir", default=".",
                      help="project root directory", metavar="<dir>")

    parser.add_option("-o", "--output", dest="out", default="site",
                      help="output directory", metavar="<out>")

    parser.add_option("-I", "--index", dest="index_file", default="",
                      help="specify the file name for index files",
                      metavar="<filename>")

    parser.add_option("-d", "--dry-run", dest="dry_run", action="store_true",
                      default=False, help="build site, do not write")

    parser.add_option("-r", "--scrub", dest="scrub", action="store_true",
                      default=False, help="clean output dir after write")

    parser.add_option("-i", "--init", dest="init", action="store_true",
                      default=False, help="initalize basic project directory")

    parser.add_option("-t", "--pagestype", dest="pagestype",
                      metavar="(yml|json)", help="pages format",
                      default=core.conf.target_type)

    parser.add_option("-n", "--pagesname", dest="pagesname",
                      metavar="<name>", help="pages name",
                      default=core.conf.target_name)

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
