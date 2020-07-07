Name:            iputils
Version:         20190709
Release:         4
Summary:         Network monitoring tools including ping
License:         BSD and GPLv2+
URL:             https://github.com/iputils/iputils

Source0:         https://github.com/iputils/iputils/archive/s%{version}.tar.gz#/%{name}-s%{version}.tar.gz
Source1:         ifenslave.tar.gz
Source2:         rdisc.service
Source3:         ninfod.service
Source4:         bsd.txt
Source5:         https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

Patch0001:       iputils-ifenslave.patch
Patch0002:       0001-iputils-arpings.patch
Patch0003:       0002-iputils-arpings-count.patch
Patch0004:       bugfix-arping-w-does-not-take-effect.patch
Patch0005:       0003-ninfod-change-variable-name-to-avoid-colliding.patch

BuildRequires:   gcc meson libidn2-devel openssl-devel libcap-devel libxslt
BuildRequires:   docbook5-style-xsl systemd glibc-kernheaders gettext
%{?systemd_ordering}
Provides:        /bin/ping /bin/ping6 /sbin/arping /sbin/rdisc
Provides:        %{name}-ninfod
Obsoletes:       %{name}-ninfod
Provides:        %{_sbindir}/ninfod

%description
The iputils package contains basic utilities for monitoring a network,
including ping. The ping command sends a series of ICMP protocol
ECHO_REQUEST packets to a specified network host to discover whether
the target machine is alive and receiving network traffic.

%package_help

%prep
%setup -q -a 1 -n %{name}-s%{version}
cp %{SOURCE4} %{SOURCE5} .

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1

%build
  export CFLAGS="-fpie"
  export LDFLAGS="-pie -Wl,-z,relro,-z,now"

%meson -DBUILD_TFTPD=false
%meson_build
gcc -Wall $RPM_OPT_FLAGS $CFLAGS $LDFLAGS ifenslave.c -o ifenslave

%install
%meson_install

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
ln -sf ../bin/ping ${RPM_BUILD_ROOT}%{_sbindir}/ping
ln -sf ../bin/ping ${RPM_BUILD_ROOT}%{_sbindir}/ping6
ln -sf ../bin/tracepath ${RPM_BUILD_ROOT}%{_sbindir}/tracepath
ln -sf ../bin/tracepath ${RPM_BUILD_ROOT}%{_sbindir}/tracepath6
ln -sf ../bin/arping ${RPM_BUILD_ROOT}%{_sbindir}/arping
ln -sf ping.8.gz ${RPM_BUILD_ROOT}%{_mandir}/man8/ping6.8.gz
ln -sf tracepath.8.gz ${RPM_BUILD_ROOT}%{_mandir}/man8/tracepath6.8.gz
install -cp ifenslave ${RPM_BUILD_ROOT}%{_sbindir}/
install -cp ifenslave.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/

%post
%systemd_post rdisc.service
%systemd_post ninfod.service

%preun
%systemd_preun rdisc.service
%systemd_preun ninfod.service

%postun
%systemd_postun_with_restart rdisc.service
%systemd_postun_with_restart ninfod.service

%files
%defattr(-,root,root)
%license bsd.txt gpl-2.0.txt LICENSE
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/clockdiff
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/arping
%attr(0755,root,root) %caps(cap_net_raw=p cap_net_admin=p) %{_bindir}/ping
%attr(0755,root,root) %caps(cap_net_raw=ep) %{_sbindir}/ninfod
%{_datadir}/locale/*
%{_sbindir}/*
%{_bindir}/tracepath
%{_unitdir}/rdisc.service
%{_unitdir}/ninfod.service

%files help
%defattr(-,root,root)
%doc README.bonding
%{_mandir}/man8/*.8.gz

%changelog
* Tue Jul 07 2020 gaihuiying <gaihuiying1@huawei.com> - 20190709-4
- Type:bugfix
- Id:NA
- SUG:restart
- DESC:fix building error with libcap's new version

* Mon May 18 2020 openEuler Buildteam <buildteam@openeuler.org> - 20190709-3
- Type:bugfix
- Id:NA
- SUG:restart
- DESC:bugfix arping's exit code for -U/A

* Wed Mar 11 2020 openEuler Buildteam <buildteam@openeuler.org> - 20190709-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:bugfix the arping

* Wed Oct 9 2019 openEuler Buildteam <buildteam@openeuler.org> - 20190709-1
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:bugfix the arping and ping6

* Mon Sep 30 2019 openEuler Buildteam <buildteam@openeuler.org> - 20190515-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add the softlink for arping

* Wed Sep 18 2019 openEuler Buildteam <buildteam@openeuler.org> - 20190515-1
- Package init
