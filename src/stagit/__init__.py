import os, sys, yaml

import stagit.ambassador

def init(arg):
	if os.path.exists(arg.dir):
		os.chdir(arg.dir)
	else:
		print("'{}' does not exist".format(arg.dir))
		sys.exit(1)

	#Try to get the config
	try:
		raw_config = file("stagit_config.yml")
		print("stagit enabled")

	except:
		return

	config = yaml.load(raw_config)

	stagit.ambassador.stagit(config)



