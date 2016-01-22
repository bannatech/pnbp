import os, sys, yaml

import core.ambassador

def init(arg):
	if os.path.exists(arg.dir):
		os.chdir(arg.dir)
	else:
		print("'{}' does not exist".format(arg.dir))
		sys.exit(1)

	#Try to get the config
	try:
		raw_config = file("stagit_config.yml")

	except:
		print("Can't open file 'stagit_config.yml'")
		sys.exit(0)

	config = yaml.load(raw_config)

	core.ambassador.stagit(config)



