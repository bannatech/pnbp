install :
	cp -r src /usr/local/pnbp
	ln -s /usr/local/pnbp/pnbp.py /usr/local/bin/pbuild
remove :
	rm -rf /usr/local/bin/pnbp /usr/local/bin/pbuild
