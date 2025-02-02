Name:            iputils
Version:         20221126
Release:         1
Summary:         Network monitoring tools including ping
License:         BSD and GPLv2+
URL:             https://github.com/iputils/iputils

Source0:         https://github.com/iputils/iputils/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:         ifenslave.tar.gz
Source2:         bsd.txt
Source3:         https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

Patch0000:       iputils-ifenslave.patch
Patch0001:       iputils-ifenslave-CWE-170.patch

BuildRequires:   gcc meson libidn2-devel openssl-devel libcap-devel libxslt
BuildRequires:   docbook5-style-xsl systemd iproute glibc-kernheaders gettext
%{?systemd_ordering}
Provides:        /bin/ping /bin/ping6 /sbin/arping

%description
The iputils package contains basic utilities for monitoring a network,
including ping. The ping command sends a series of ICMP protocol
ECHO_REQUEST packets to a specified network host to discover whether
the target machine is alive and receiving network traffic.

%package_help

%prep
%setup -q -a 1 -n %{name}-%{version}
cp %{SOURCE2} %{SOURCE3} .

%autopatch -p1

%build
  export CFLAGS="-fpie"
  export LDFLAGS="-pie -Wl,-z,relro,-z,now"

%meson
%meson_build
gcc -Wall $RPM_OPT_FLAGS $CFLAGS $RPM_LD_FLAGS $LDFLAGS ifenslave.c -o ifenslave

%install
%meson_install

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
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

%preun

%postun

%files
%defattr(-,root,root)
%license bsd.txt gpl-2.0.txt LICENSE
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/clockdiff
%attr(0755,root,root) %caps(cap_net_raw=p) %{_bindir}/arping
%attr(0755,root,root) %caps(cap_net_raw=p cap_net_admin=p) %{_bindir}/ping
%{_datadir}/locale/*
%{_sbindir}/ifenslave
%{_bindir}/tracepath
%{_sbindir}/ping
%{_sbindir}/ping6
%{_sbindir}/tracepath
%{_sbindir}/tracepath6
%{_sbindir}/arping
%{_bindir}/tracepath

%files help
%defattr(-,root,root)
%doc README.bonding
%{_mandir}/man8/*.8.gz
 
%changelog
* Mon Feb 6 2023 zhongxuan <zhongxuan2@huawei.com> - 20221126-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC: update iputils to 20221126

* Mon Jul 11 2022 yinyongkang <yinyongkang@kylinos.cn> - 20211215-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC: update iputils to 20211215

* Mon Jun 20 2022 lvgenggeng <lvgenggeng@uniontech.com> - 20210722-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:backport to fix potential memory leakage on -p option

* Sat May 07 2022 eaglegai <eaglegai@163.com> - 20210722-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:backport to fix no reply when ping6 from Subnet-Router anycast address

* Fri May 06 2022 eaglegai <eaglegai@163.com> - 20210722-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: fix exit code on -w option when count*interval > timeout

* Tue Apr 26 2022 zengweifeng <zwfeng@huawei.com> - 20210722-3
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: fix ping2 bingding to VRF and address
        Avoid binding to non-VRF
        Fix ARP protocol field for AX.25 and NETROM

* Fri Feb 18 2022 xinghe <xinghe2@h-partners.com> - 20210722-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix arping -w command return error
       remove old tar package

* Tue Dec 07 2021 xihaochen <xihaochen@huawei.com> - 20210722-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC: update iputils to 20210722

* Mon Mar 8 2021 xuxiaolong <xuxiaolong23@huawei.com> - 20200821-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix rdisc: remove PrivateUsers=yes from systemd service file 

* Thu Jan 28 2021 xihaochen <xihaochen@huawei.com> - 20200821-1
- Type:requirements
- ID:NA
- SUG:NA
- DESC: update iputils to 20200821

* Thu Dec 10 2020 lunankun <lunankun@huawei.com> - 20190709-7
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: fix arping update neighbours

* Sun Nov 29 2020 openEuler Buildteam <buildteam@openeuler.org> - 20190709-6
- append patch file of upstream repository from <2583fb77dd57c5183998177a3fa13a680b573005> to <78e3d25a50537a842fd3b18eab971d63d5891350>

* Tue Nov 3 2020 openEuler Buildteam <buildteam@openeuler.org> - 20190709-5
- append patch file of upstream repository from <86ed08936d49e2c81ef49dfbd02aca1c74d0c098> to <86ed08936d49e2c81ef49dfbd02aca1c74d0c098>

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
