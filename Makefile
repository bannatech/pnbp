install :
	cp -r src /usr/local/bin/pnbp
	ln -s /usr/local/bin/pnbp/init.py /usr/local/bin/build
remove :
	rm -rf /usr/local/bin/pnbp /usr/local/bin/build
