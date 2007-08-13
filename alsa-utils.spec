%define beta 0
%if %beta
%define fname %name-%{version}%beta
%else
%define fname %name-%{version}
%endif
%define req_lib 0.1


Summary: Advanced Linux Sound Architecture (ALSA) utilities
Name:    alsa-utils
Version: 1.0.14
%if %beta
Release: %mkrel 0.%{beta}.2
%else
Release: %mkrel 2
%endif
Source:  ftp://ftp.alsa-project.org/pub/utils/%fname.tar.bz2
License: GPL
BuildRoot: %_tmppath/%name-buildroot
Group: Sound
Url:   http://www.alsa-project.org

BuildRequires: kernel-headers >= 2.4.0
BuildRequires: libalsa-devel >= %version-%req_lib
BuildRequires: ncurses-devel
Requires: alsa-lib >= 1:%version
# dependancies for alsaconf:
Requires: pciutils

%description
Advanced Linux Sound Architecture (ALSA) utilities. Modularized architecture
with support for a large range of ISA and PCI cards. Fully compatible with
OSS/Lite (kernel sound drivers), but contains many enhanced features.

This is the utilities package, which allows you to manipulate ALSA settings.

%package -n speaker-test
Summary: ALSA test tool
Group: Sound
Requires: alsa-utils
Conflicts: alsa-utils < 1.0.9-4mdk

%description -n speaker-test
speaker-test is a tool that enables one to test his head phones.

%package -n alsaconf
Summary: ALSA configuration tool
Group: Sound
Requires: alsa-utils whiptail cdialog
Conflicts: alsa-utils < 1.0.9-4mdk

%description -n alsaconf
Alsaconf is a tool that enables one to configure his sound card with ALSA.
It's often not not needed as mandriva linux will autoconfigure sound cards.

%prep
%setup -q -n %fname

%build
%configure2_5x
make all

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std mkdir_p="mkdir -p"

# move alsactl in /sbin in order to reload mixer settings on bootstrapping:
mkdir $RPM_BUILD_ROOT/sbin
mv $RPM_BUILD_ROOT/{%_sbindir,sbin}/alsactl
ln -s ../../sbin/alsactl $RPM_BUILD_ROOT/%_sbindir

%find_lang alsaconf
%find_lang alsa-utils
cat alsa-utils.lang >> alsaconf.lang

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc [A-Z][A-Z]*
%_bindir/[a-i]*
%_sbindir/alsactl
/sbin/alsactl
%_mandir/man1/[a-i]*
%_datadir/alsa/

%files -n speaker-test
%_bindir/speaker-test
%_mandir/man1/speaker-test.*
%_datadir/sounds/alsa/

%files -n alsaconf -f alsaconf.lang
%_sbindir/alsaconf
%_mandir/man8/alsaconf.*
%lang(fr) %_mandir/fr/man8/alsaconf.*


