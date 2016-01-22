import sys, os

from subprocess import call

def stagit(config):
	config['output_dir'] = config.get("output_dir", "html/")

	config['repo_dir'] = config.get("repo_dir", "src/")

	repo_string = ""

	for repo in os.listdir(config['repo_dir']):
		repo_path = os.path.join( config['output_dir'], repo )

		os.mkdir(repo_path)

		path = os.getcwd()

		os.chdir( repo_path )

		call(["stagit", repo_path])

		os.chdir(path)

		repo_string = " ".join(repo_string, repo)
	
	os.chdir(config['output_dir'])

	call(["stagit-index", repo_string])


