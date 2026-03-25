all: rpm build
	
rpm:
	spectool -g ${PWD}/tuxedo-drivers-no-light.spec
	fedpkg --release f43 mockbuild --enable-network

build:
	sudo akmods --akmod tuxedo-drivers-no-light

lint:
	rpm -q --specfile tuxedo-drivers-no-light.spec

clean:
	rm -rf tmp
	rm -rf results_*
	rm -f *.src.rpm
	rm -f *.tar.gz
	rm -f results_tuxedo-drivers-no-light

unpack:
	mkdir -p tmp && \
		cd tmp && \
		rpm2cpio ../tuxedo-drivers-no-light-kmod-4.13.1-0.fc43.src.rpm | cpio -idmv
