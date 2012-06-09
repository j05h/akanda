DEV_DIR = ~/lab/DreamHost/dhc
PYPF_DIR = $(DEV_DIR)/pypf
PYPF_URL = git@github.com:dreamhost/pypf.git
USER = oubiwann

system-setup:
	pw user mod $(USER) -G wheel

install-ports:
	portsnap fetch
	portsnap extract

update-ports:
	portsnap fetch
	portsnap update

install-git:
	cd /usr/ports/devel/git && make install clean

install-twisted:
	cd /usr/ports/devel/py-twisted && make install clean

$(DEV_DIR):
	mkdir -p $(DEV_DIR)

$(PYPF_DIR):
	cd $(DEV_DIR) && git clone $(PYPF_URL)

# This assumes running as root
install-pypf: $(DEV_DIR) $(PYPF_DIR)
	cd $(PYPF_DIR) && python setup.py install
