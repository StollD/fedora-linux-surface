.ONESHELL:
%.spec:
	cd $*
	rpmdev-setuptree
	spectool -g -R $@
	rpmbuild -bb $@
