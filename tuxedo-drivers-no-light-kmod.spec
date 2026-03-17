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
Summary:        Tuxedo drivers not enabling light on touchpad as akmod
Group:          System Environment/Kernel
License:        GPL-2.0-or-later
URL:            https://gitlab.com/tuxedocomputers/development/packages/%{modname}

Source:         %{url}/-/archive/v%{version}/tuxedo-drivers-v%{version}.tar.gz

BuildRequires: kmodtool
BuildRequires: kernel-devel
BuildRequires: make
BuildRequires: gcc

Provides: %{modname}-no-light = %{version}
Obsoletes: %{modname}-no-light < 4.0.0

%description
Tuxedo drivers as kmod

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
echo "Prepare stage -----------------------------------------------------------------------------------------------"
%setup -q -c -T -a 0

for kernel_version  in %{?kernel_versions} ; do
  cp -a src _kmod_build_${kernel_version%%___*}
done

%build
echo "Build stage -----------------------------------------------------------------------------------------------"

for kernel_version in %{?kernel_versions}; do
  make V=1 %{?_smp_mflags} -C /lib/modules/${kernel_version%%___*}/build M=${PWD}/_kmod_build_${kernel_version%%___*} modules
done

%install
echo "Install stage ---------------------------------------------------------------------------------------------"

for kernel_version in %{?kernel_versions}; do
  mkdir -p %{buildroot}/lib/modules/${kernel_version%%___*}/extra/%{modname}/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/**/*.ko %{buildroot}/lib/modules/${kernel_version%%___*}/extra/%{modname}/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/*.ko %{buildroot}/lib/modules/${kernel_version%%___*}/extra/%{modname}/
  chmod a+x %{buildroot}/lib/modules/${kernel_version%%___*}/extra/%{modname}/*.ko
done

# Copy configs
mkdir -p %{buildroot}/usr/lib/modprobe.d/

# Copy udev rules
mkdir -p %{buildroot}/usr/lib/udev/rules.d/
ls -al
cp %{modname}-%{version}/99-infinityflex-touchpanel-toggle.rules %{buildroot}/usr/lib/udev/rules.d/
cp %{modname}-%{version}/99-z-tuxedo-systemd-fix.rules %{buildroot}/usr/lib/udev/rules.d/

# Copy udev hwdb
mkdir -p %{buildroot}/usr/lib/udev/hwdb.d/
cp %{modname}-%{version}/61-sensor-tuxedo.hwdb %{buildroot}/usr/lib/udev/hwdb.d/
cp %{modname}-%{version}/61-keyboard-tuxedo.hwdb %{buildroot}/usr/lib/udev/hwdb.d/

%{?akmod_install}

%files
/usr/lib/udev/rules.d/99-infinityflex-touchpanel-toggle.rules
/usr/lib/udev/rules.d/99-z-tuxedo-systemd-fix.rules
/usr/lib/udev/hwdb.d/61-sensor-tuxedo.hwdb
/usr/lib/udev/hwdb.d/61-keyboard-tuxedo.hwdb
# %doc README.md
# %license debian/copyright

%changelog
