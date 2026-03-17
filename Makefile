all:
	fedpkg --release f43 mockbuild --enable-network

tito:
	tito build --rpm --test

clean:
	rm -rf tmp
	rm -rf results_*
	rm -f tuxedo-drivers-no-light-kmod-4.13.1-0.fc43.src.rpm

unpack:
	mkdir -p tmp && \
		cd tmp && \
		rpm2cpio ../tuxedo-drivers-no-light-kmod-4.13.1-0.fc43.src.rpm | cpio -idmv
