%global         modname                 tuxedo-drivers
%global         _sysconf_modprobe_d     %{_sysconfdir}/modprobe.d/
%define         buildforkernels         akmod
%define        __libdir  /usr/lib
%global         AkmodsBuildRequires     make gcc sed gawk
%global short tuxedo-drivers
%global module_names tuxedo_compatibility_check tuxedo_keyboard clevo_acpi clevo_wmi uniwill_wmi tuxedo_io tuxedo_nb02_nvidia_power_ctrl ite_8291 ite_8291_lb ite_8297 ite_829x tuxedo_nb05_ec tuxedo_nb05_power_profiles tuxedo_nb05_sensors tuxedo_nb05_keyboard tuxedo_nb05_kbd_backlight tuxedo_nb05_fan_control tuxedo_nb04_keyboard tuxedo_nb04_wmi_ab tuxedo_nb04_wmi_bs tuxedo_nb04_sensors tuxedo_nb04_power_profiles tuxedo_nb04_kbd_backlight stk8321 gxtp7380 tuxedo_tuxi_fan_control tuxi_acpi

%if 0%{?fedora}
%global         debug_package           %{nil}
%endif

Name:           %{modname}-no-light-kmod
Version:        4.13.1
Release:        2%{?dist}
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
Obsoletes: %{name} < 4.0.0

%description
Tuxedo drivers as kmod

%{!?kernels:BuildRequires: buildsys-build-%{repo}-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%prep
echo "Prepare stage -----------------------------------------------------------------------------------------------"
%setup -q -c -T -a 0

for kernel_version  in %{?kernel_versions} ; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  tar xzf %{SOURCE0} --strip-components=1 -C _kmod_build_${kernel_version%%___*}
  # cp -a %{modname}-%{version} _kmod_build_${kernel_version%%___*}
  ls -alR
done

%build
echo "Build stage -----------------------------------------------------------------------------------------------"

for kernel_version in %{?kernel_versions}; do
  #  make V=1 %{?_smp_mflags} -C /lib/modules/${kernel_version%%___*}/build M=${PWD}/%{modname}-%{version}/_kmod_build_${kernel_version%%___*} modules
  #  make V=1 %{?_smp_mflags} -C /lib/modules/${kernel_version%%___*}/build M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules 
  cd _kmod_build_${kernel_version%%___*}
  ls -alR
  make
  cd ..
done

%install
echo "Install stage ---------------------------------------------------------------------------------------------"

for kernel_version in %{?kernel_versions}; do
  mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/**/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  install -D -m 755 _kmod_build_${kernel_version%%___*}/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
  chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/*.ko
done

# install for common
# mkdir -p %{buildroot}%{_modulesloaddir}
# for module in %{module_names}; do
#    echo "$module" > ${module}.conf
#    install -D -m 0644 ${module}.conf %{buildroot}%{__libdir}/modules-load.d/${module}.conf
# done


# Copy configs
mkdir -p %{buildroot}/etc/modprobe.d/

cp %{modname}-%{version}/tuxedo_keyboard.conf %{buildroot}/etc/modprobe.d/

# Copy udev rules
mkdir -p %{buildroot}%{__libdir}/udev/rules.d/
ls -al
cp %{modname}-%{version}/99-infinityflex-touchpanel-toggle.rules %{buildroot}%{__libdir}/udev/rules.d/
cp %{modname}-%{version}/99-z-tuxedo-systemd-fix.rules %{buildroot}%{__libdir}/udev/rules.d/

# Copy udev hwdb
mkdir -p %{buildroot}/usr/lib/udev/hwdb.d/
cp %{modname}-%{version}/61-sensor-tuxedo.hwdb %{buildroot}%{__libdir}/udev/hwdb.d/
cp %{modname}-%{version}/61-keyboard-tuxedo.hwdb %{buildroot}%{__libdir}/udev/hwdb.d/

%{?akmod_install}

%files

%changelog

%package common
Summary:  Tuxedo drivers kmod common files
Requires: %{name}-kmod-common >= %{version}
BuildRequires: systemd-rpm-macros

%description common
Tuxedo drivers kmod common files

%files common
/etc/modprobe.d/tuxedo_keyboard.conf
%{__libdir}/udev/rules.d/99-infinityflex-touchpanel-toggle.rules
%{__libdir}/udev/rules.d/99-z-tuxedo-systemd-fix.rules
%{__libdir}/udev/hwdb.d/61-sensor-tuxedo.hwdb
%{__libdir}/udev/hwdb.d/61-keyboard-tuxedo.hwdb
# %doc README.md
# %license debian/copyright

%changelog common
