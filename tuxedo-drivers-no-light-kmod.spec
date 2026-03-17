%global         modname                 tuxedo-drivers
%global         _sysconf_modprobe_d     %{_sysconfdir}/modprobe.d/
%global         buildforkernels         akmod
%global         AkmodsBuildRequires     make gcc sed gawk

%if 0%{?fedora}
%global         debug_package           %{nil}
%endif

Name:           %{modname}-no-light-kmod
Version:        4.13.1
Release:        0%{?dist}
Summary:        Tuxedo drivers not enabling light on touchpad
Group:          System Environment/Kernel
License:        GPL-2.0-or-later
URL:            https://github.com/tuxedocomputers/tuxedo-drivers
Source0:        https://github.com/tuxedocomputers/%{modname}/archive/refs/tags/v%{version}.tar.gz#/%{modname}-%{version}.tar.gz

Provides:       tuxedo-drivers = %{version}

BuildRequires:  kmodtool systemd-rpm-macros

# if built locally, this will fail
# percent_sign{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Tuxedo kernel Modules user package

%prep
# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

%setup -q -c -T -a 0
# %autosetup -C

# curl -LO https://github.com/tuxedocomputers/%{modname}/archive/refs/tags/v%{version}.tar.gz
# tar xzf v%{version}.tar.gz --strip-components=1

for kernel_version in %{?kernel_versions}; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  cp -a tuxedo-drivers-%{version} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
  pushd _kmod_build_${kernel_version%%___*}/%{name}-%{version}
    make -j1 -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*} modules
    # percent_sign{make_build} KERNELDIR="${kernel_version##*___}" modules
  popd
done

%install
for kernel_version in %{?kernel_versions}; do
    make -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*}/src INSTALL_MOD_PATH=${RPM_BUILD_ROOT} INSTALL_MOD_DIR=%{kmodinstdir_postfix} modules_install
done

install -D -m 644 tuxedo_keyboard.conf ${RPM_BUILD_ROOT}%{_sysconfdir}/modprobe.d/tuxedo_keyboard.conf
install -D -m 644 99-z-tuxedo-systemd-fix.rules ${RPM_BUILD_ROOT}%{_sysconfdir}/udev/rules.d/99-z-tuxedo-systemd-fix.rules
%{?akmod_install}

# is this needed?
# install -p -m 0755 -d %{buildroot}%{_modprobedir}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_sysconfdir}/modprobe.d/tuxedo_keyboard.conf
%{_sysconfdir}/udev/rules.d/99-z-tuxedo-systemd-fix.rules

%changelog
* Sun Mar 15 2026 indika-dev
- Update to version 4.13.1
* Mon May 13 2024 offlinehq
- Update to version 4.4.3
* Fri Mar 15 2024 offlinehq
- Add Provides for tuxedo-drivers
* Fri Mar 15 2024 offlinehq
- Update to version 4.3.2
* Mon Feb 05 2024 offlinehq
- Initial Fedora build
