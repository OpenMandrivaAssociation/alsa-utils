Summary:	Advanced Linux Sound Architecture (ALSA) utilities
Name:		alsa-utils
Version:	1.2.14
Release:	1
Source0:	http://www.alsa-project.org/files/pub/utils/alsa-utils-%{version}.tar.bz2
License:	GPL
Group:		Sound
Url:		https://www.alsa-project.org

BuildRequires:  gettext
BuildRequires:	kernel-headers >= 2.4.0
BuildRequires:	pkgconfig(alsa) >= %{version}
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(udev)
BuildRequires:	xmlto
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	systemd-rpm-macros
Requires:	alsa-lib >= %{version}
# dependancies for alsaconf:
Requires:	pciutils
%systemd_requires

%patchlist

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
%autosetup -p1

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

# Whatever owns alsaucm should also own the directory
mkdir -p %{buildroot}%{_datadir}/alsa/ucm2

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-alsa.preset << EOF
enable alsa-state.service
enable alsa-restore.service
EOF

%find_lang alsaconf
%find_lang alsa-utils
cat alsa-utils.lang >> alsaconf.lang

%post
if [ -s /etc/asound.state ] && [ ! -s /var/lib/alsa/asound.state ]; then
    mv /etc/asound.state /var/lib/alsa/asound.state
fi

%systemd_post alsa-state.service alsa-restore.service

%preun
%systemd_preun alsa-state.service alsa-restore.service

%postun
%systemd_postun_with_restart alsa-state.service alsa-restore.service

%files
%doc [A-Z][A-Z]*
%{_bindir}/[a-i]*
%{_bindir}/nhlt-dmic-info
%doc %{_mandir}/man1/[a-i]*
%doc %{_mandir}/man1/nhlt-dmic-info.1.*
%doc %{_mandir}/man7/alsactl_init.7*
%doc %{_mandir}/man8/alsa-info.sh.8*
%{_datadir}/alsa/
%{_presetdir}/86-alsa.preset
%{_unitdir}/*.service
%{_unitdir}/*/*.service
%{_udevrulesdir}/*.rules
%ghost %{_localstatedir}/lib/alsa/asound.state
%{_libdir}/alsa-topology/libalsatplg_module_nhlt.so

%files -n speaker-test
%{_bindir}/speaker-test
%doc %{_mandir}/man1/speaker-test.*
%{_datadir}/sounds/alsa/

%files -n alsaconf -f alsaconf.lang
%{_sbindir}/alsaconf
%doc %{_mandir}/man8/alsaconf.*
%lang(fr) %{_mandir}/fr/man8/alsaconf.*
