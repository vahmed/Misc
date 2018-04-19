Name:           asterisk-certified
Version:        13.13
Release:        1%{?dist}
Summary:        Asterisk pbx server

Group:          Applications/Communications
License:        GPL
URL:            http://www.asterisk.org/
Source:         asterisk-certified-13.13-current.tar.gz
%define         debug_package %{nil}

requires: jansson >= 2.10, unixODBC  >= 2.2.14, speex >= 1.2, sqlite >= 3.3.0
BuildRequires: openssl-devel, zlib-devel, perl, bison, speex-devel, doxygen, newt-devel, ncurses-devel, libuuid-devel, curl-devel, sqlite-devel

%description
The Asterisk call server with SIP and G722 support.

%package devel
Summary:  Asterisk development files
Group:    Applications/Communications
Provides: aterisk-devel

%description devel
The Asterisk development headers

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --libdir=/usr/lib64 --prefix=%{_prefix} --mandir=%{_mandir} --sysconfdir=%{_sysconfdir}
#make menuselect.makeopts
make -j2 %{?_smp_mflags}

%install
%make_install

%if 0%{?rhel} >= 7
mkdir -p %{buildroot}/etc/systemd/system
cp %{_builddir}/%{name}-%{version}/contrib/init.d/sys.redhat.asterisk.service %{buildroot}/etc/systemd/system/asterisk.service
%else
mkdir -p %{buildroot}/etc/init.d
cp %{_builddir}/%{name}-%{version}/contrib/init.d/rc.redhat.asterisk %{buildroot}/etc/init.d/asterisk
%endif
mkdir -p ${buildroot}/var/lib/asterisk/sounds/en
cp %{_builddir}/%{name}-%{version}/sounds/en/macroform-the_simplicity.wav %{buildroot}/var/lib/asterisk/sounds/en

%files
%defattr(-,root,root)
/etc/asterisk
/usr/sbin/*
/usr/share/man/man8/*
/usr/lib64/asterisk
/usr/lib64/libasteriskssl.so
/usr/lib64/libasteriskssl.so.1
/var/lib/asterisk
/var/log/asterisk
/var/spool/asterisk
/var/lib/asterisk/sounds/en/
/var/lib/asterisk/moh
%if 0%{?rhel} >= 7
%attr(0644,root,root) /etc/systemd/system/asterisk.service
%else
%attr(0755,root,root) /etc/init.d/asterisk
%endif

%post
%if 0%{?rhel} >= 7
systemctl enable asterisk
%else
chkconfig --add asterisk
%endif

%postun

%files devel
/usr/include/asterisk.h
/usr/include/asterisk

%changelog
* Tue Nov 07 2017 Nasir Ahmed 13.13
- Initial RPM Release

%clean
rm -rf %{buildroot}
