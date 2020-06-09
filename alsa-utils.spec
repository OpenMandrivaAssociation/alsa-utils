%define alibversion %{version}
%define beta 0
%if %beta
%define fname %name-%{version}%beta
%else
%define fname %name-%{version}
%endif

Summary:	Advanced Linux Sound Architecture (ALSA) utilities
Name:		alsa-utils
Version:	1.2.3
%if %beta
Release:	1
%else
Release:	1
%endif
Source0:	ftp://ftp.alsa-project.org/pub/utils/%fname.tar.bz2
License:	GPL
Group:		Sound
Url:		http://www.alsa-project.org

BuildRequires:	kernel-headers >= 2.4.0
BuildRequires:	libalsa-devel >= %alibversion
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(udev)
BuildRequires:	xmlto
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	fftw-devel
BuildRequires:	systemd-macros
Requires:	alsa-lib >= 1:%alibversion
# dependancies for alsaconf:
Requires:	pciutils
Requires(pre):	filesystem
Requires(post):	rpm-helper

%description
Advanced Linux Sound Architecture (ALSA) utilities. Modularized architecture
with support for a large range of ISA and PCI cards. Fully compatible with
OSS/Lite (kernel sound drivers), but contains many enhanced features.

This is the utilities package, which allows you to manipulate ALSA settings.

%package -n speaker-test
Summary:	ALSA test tool
Group:		Sound
Requires:	alsa-utils
Conflicts:	alsa-utils < 1.0.9-4mdk

%description -n speaker-test
speaker-test is a tool that enables one to test his head phones.

%package -n alsaconf
Summary:	ALSA configuration tool
Group:		Sound
Requires:	alsa-utils
Requires:	whiptail
Requires:	cdialog
Conflicts:	alsa-utils < 1.0.9-4mdk

%description -n alsaconf
Alsaconf is a tool that enables one to configure his sound card with ALSA.
It's often not not needed as mandriva linux will autoconfigure sound cards.

%prep
%setup -q -n %fname

%build
%configure \
    --disable-rpath \
    --with-systemdsystemunitdir=%{_unitdir}

%make_build all

%install
%make_install mkdir_p="mkdir -p"

# Create /var/lib/alsa tree
mkdir -p -m 755 %{buildroot}%{_localstatedir}/lib/alsa
touch %{buildroot}%{_localstatedir}/lib/alsa/asound.state


# move alsactl in /sbin in order to reload mixer settings on bootstrapping:
mkdir %{buildroot}/sbin
mv %{buildroot}/{%{_sbindir},sbin}/alsactl

ln -s ../../sbin/alsactl %{buildroot}/%{_sbindir}

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-alsa.preset << EOF
enable alsa-state.service
enable alsa-restore.service
EOF

%find_lang alsaconf
%find_lang alsa-utils
cat alsa-utils.lang >> alsaconf.lang

%post
if [ -s /etc/asound.state -a ! -s /var/lib/alsa/asound.state ] ; then
    mv /etc/asound.state /var/lib/alsa/asound.state
fi

%files
%doc [A-Z][A-Z]*
%{_bindir}/[a-i]*
%{_sbindir}/alsactl
%{_sbindir}/alsa-info.sh
%{_sbindir}/alsabat-test.sh
/sbin/alsactl
%{_mandir}/man1/[a-i]*
%{_mandir}/man7/alsactl_init.7*
%{_datadir}/alsa/
%{_presetdir}/86-alsa.preset
%{_unitdir}/*.service
%{_unitdir}/*/*.service
/lib/udev/rules.d/*.rules
#%{_localstatedir}/lib/alsa
%ghost %{_localstatedir}/lib/alsa/asound.state

%files -n speaker-test
%{_bindir}/speaker-test
%{_mandir}/man1/speaker-test.*
%{_datadir}/sounds/alsa/

%files -n alsaconf -f alsaconf.lang
%{_sbindir}/alsaconf
%{_mandir}/man8/alsaconf.*
%lang(fr) %_mandir/fr/man8/alsaconf.*
