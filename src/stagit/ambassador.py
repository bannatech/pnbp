import sys, os

from subprocess import call

def stagit(config):
	config['output_dir'] = config.get("output_dir", "html/")

	config['repo_dir'] = config.get("repo_dir", "src/")

	repos = []

	for repo in os.listdir(config['repo_dir']):
		repo_path = os.path.join( config['repo_dir'], repo )
		output_path = os.path.join( config['output_dir'], repo )

		if not os.path.exists(output_path):
			os.mkdir(output_path)

		path = os.getcwd()

		os.chdir( output_path )

		try:
			os.symlink(
			os.path.join(config['output_dir'], "favicon.png"),
			os.path.join(output_path,          "favicon.png"))
		except: pass

		try:
			os.symlink(
			os.path.join(config['output_dir'], "logo.png"),
			os.path.join(output_path,          "logo.png"))
		except: pass

		try:
			os.symlink(
			os.path.join(config['output_dir'], "style.css"),
			os.path.join(output_path,          "style.css"))
		except: pass

		call(["stagit", repo_path])

		os.chdir(path)

		repos.append(repo_path)

	
	os.chdir(config['output_dir'])

	f = open("index.html", "w")

	call(["stagit-index"] + repos, stdout=f)




