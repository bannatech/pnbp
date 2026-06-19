PREFIX ?= /usr/local/lib
BINDIR ?= /usr/local/bin
install :
	cp -r src $(PREFIX)/pnbp
	ln -s $(PREFIX)/pnbp/pnbp.py $(BINDIR)/pbuild
remove :
	rm -rf $(PREFIX)/pnbp $(BINDIR)/pbuild
