%global         modname                 tuxedo-drivers
%global         _sysconf_modprobe_d     %{_sysconfdir}/modprobe.d/
%define         buildforkernels         akmod
%define        __libdir  /usr/lib
%global         AkmodsBuildRequires     make gcc sed gawk

%if 0%{?fedora}
%global         debug_package           %{nil}
%endif

Name:           %{modname}-no-light-kmod
Version:        4.13.1
Release:        4%{?dist}
Summary:        Tuxedo drivers not enabling light on touchpad as akmod
Group:          System Environment/Kernel
License:        GPL-2.0-or-later
URL:            https://github.com/tuxedocomputers/tuxedo-drivers

Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: kmodtool
BuildRequires: kernel-devel
BuildRequires: make
BuildRequires: gcc

Provides: %{name} = %{version}
Provides: %{modname} = %{version}
Obsoletes: %{name} < 4.0.0

%description
Tuxedo drivers as kmod

%{!?kernels:BuildRequires: buildsys-build-%{repo}-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
echo "Prepare stage -----------------------------------------------------------------------------------------------"
%setup -q -c -T -a 0

for kernel_version  in %{?kernel_versions} ; do
  # prepare kernel build
  rm -rf _kmod_build_${kernel_version%%___*}
  mkdir -p _kmod_build_${kernel_version%%___*}
  tar xzf %{SOURCE0} --strip-components=1 -C _kmod_build_${kernel_version%%___*}
  # prepare common installation
  rm -rf %{modname}-%{version}
  mkdir -p %{modname}-%{version}
  tar xzf %{SOURCE0} --strip-components=1 -C %{modname}-%{version}
done

%build
echo "Build stage -----------------------------------------------------------------------------------------------"

for kernel_version in %{?kernel_versions}; do
  make V=1 %{?_smp_mflags} -C /lib/modules/${kernel_version%%___*}/build M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
echo "Install stage ---------------------------------------------------------------------------------------------"

for kernel_version in %{?kernel_versions}; do
  mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  find _kmod_build_${kernel_version%%___*} -type f -name "*.ko" -exec install -D -m 755 {} %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/ \;
done

# Copy configs
mkdir -p %{buildroot}/etc/modprobe.d/

cp %{modname}-%{version}/tuxedo_keyboard.conf %{buildroot}/etc/modprobe.d/

# Copy udev rules
mkdir -p %{buildroot}%{__libdir}/udev/rules.d/
install -D -m 644 %{modname}-%{version}/99-infinityflex-touchpanel-toggle.rules %{buildroot}%{__libdir}/udev/rules.d/
install -D -m 644 %{modname}-%{version}/99-z-tuxedo-systemd-fix.rules %{buildroot}%{__libdir}/udev/rules.d/

# Copy udev hwdb
mkdir -p %{buildroot}/usr/lib/udev/hwdb.d/
install -D -m 644 %{modname}-%{version}/61-sensor-tuxedo.hwdb %{buildroot}%{__libdir}/udev/hwdb.d/
install -D -m 644 %{modname}-%{version}/61-keyboard-tuxedo.hwdb %{buildroot}%{__libdir}/udev/hwdb.d/

%{?akmod_install}

%files

%changelog

%package common
Summary:  Tuxedo drivers kmod common files
BuildRequires: systemd-rpm-macros

%description common
Tuxedo drivers kmod common files

%files common
%config(noreplace) /etc/modprobe.d/tuxedo_keyboard.conf
%{__libdir}/udev/rules.d/99-infinityflex-touchpanel-toggle.rules
%{__libdir}/udev/rules.d/99-z-tuxedo-systemd-fix.rules
%{__libdir}/udev/hwdb.d/61-sensor-tuxedo.hwdb
%{__libdir}/udev/hwdb.d/61-keyboard-tuxedo.hwdb
# %doc README.md
# %license debian/copyright

%changelog common
