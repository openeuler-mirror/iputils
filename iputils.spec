Name:            iputils
Version:         20190709
Release:         8
Summary:         Network monitoring tools including ping
License:         BSD and GPLv2+
URL:             https://github.com/iputils/iputils

Source0:         https://github.com/iputils/iputils/archive/s%{version}.tar.gz#/%{name}-s%{version}.tar.gz
Source1:         ifenslave.tar.gz
Source2:         rdisc.service
Source3:         ninfod.service
Source4:         bsd.txt
Source5:         https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

Patch100:        iputils-ifenslave.patch

Patch6000:       0001-iputils-arpings.patch
Patch6001:       0002-iputils-arpings-count.patch
Patch6002:       bugfix-arpping-make-update-neighbours-work-again.patch
Patch6003:       bugfix-rdisc-remove-PrivateUsers=yes-from-systemd-service-file.patch
Patch6004:       backport-fix-ARP-protocol-field-for-AX.25-and-NETROM.patch
Patch6005:       backport-ping-Fix-ping6-binding-to-VRF-and-address.patch
Patch6006:       backport-ping6-Avoid-binding-to-non-VRF.patch

Patch9000:       bugfix-fix-ping-dead-loop.patch
Patch9001:       bugfix-arping-w-does-not-take-effect.patch
Patch9002:       bugfix-fix-update-problem.patch

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

%patch100  -p1
%patch6000 -p1
%patch6001 -p1
%patch6002 -p1
%patch6003 -p1
%patch6004 -p1
%patch6005 -p1
%patch6006 -p1
%patch9000 -p1
%patch9001 -p1
%patch9002 -p1

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
* Sat May 14 2022 yanglu <yanglu72@h-partners.com> - 20190709-8
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix ping6 bingding to VRF and address
       Avoid binding to non-VRF
       Fix ARP protocol field for AX.25 and NETROM

* Mon May 17 2021 gaihuiying <gaihuiying1@huawei.com> - 20190709-7
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:sync 21.03 patch to fix rdisc service failed

* Thu Dec 10 2020 lunankun <lunankun@huawei.com> - 20190709-6
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: fix arping update neighbours

* Fri May 22 2020 liaichun <liaichun@huawei.com> - 20190709-5
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: fix arping's exit code for -U/A

* Thu Apr 23 2020 liaichun <liaichun@huawei.com> - 20190709-4
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: fix update problem

* Sat Mar 7 2020 liuzhikang <liuzhikang3@huawei.com> - 20190709-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:fix arping parameter -w does not take effect

* Tue Mar 3 2020 liuzhikang <liuzhikang3@huawei.com> - 20190709-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:update patches

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
