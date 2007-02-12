# TODO
# - cc, cflags
#
# Conditional build:
%bcond_without	version		# show shorter version string answering the version query
#
Summary:	ICQ transport daemon for Jabber
Summary(pl.UTF-8):   Demon transportowy ICQ dla systemu Jabber
Name:		jit
Version:	1.1.7
Release:	2
License:	GPL
Group:		Applications/Communications
#Source0:	http://files.jabberstudio.org/jit/%{name}-%{version}.tar.gz
Source0:	http://www.jabber.ru/files/jit/%{name}-%{version}.tar.gz
# Source0-md5:	5400bd79d5014fef35fed2195967e5ae
Source1:	%{name}.xml
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-version.patch
URL:		http://jit.jabberstudio.org/
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	jabber-common
Requires(post):	sed >= 4.0
Requires(post):	textutils
Requires(post,preun):	/sbin/chkconfig
Requires:	jabber-common
Requires:	rc-scripts
Obsoletes:	jabber-icq-transport
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This daemon allows Jabber to communicate with ICQ servers.

%description -l pl.UTF-8
Demon ten umożliwia użytkownikom Jabbera komunikowanie się z
użytkownikami ICQ.

%prep
%setup -q
%{!?with_version:%patch0 -p1}

%build
%configure
%{__make}
%{__make} -C xdb_file

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/jabber,%{_libdir}/jit,/var/log/%{name}} \
	$RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},/var/lib/%{name}}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabber
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

install jabberd/jabberd-jit $RPM_BUILD_ROOT%{_sbindir}/jit
install jit/jit.so xdb_file/xdb_file.so $RPM_BUILD_ROOT%{_libdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_sysconfdir}/jabber/secret ] ; then
	SECRET=`cat %{_sysconfdir}/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in jit.xml..."
		%{__sed} -i -e "s/>secret</>$SECRET</" %{_sysconfdir}/jabber/jit.xml
	fi
fi
/sbin/chkconfig --add jit
%service jit restart "Jabber ICQ transport daemon"

%preun
if [ "$1" = "0" ]; then
	%service jit stop
	/sbin/chkconfig --del jit
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS jit/ChangeLog README jit/TODO jit/INSTALL doc/FAQ
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/jabber/jit.xml
%attr(754,root,root) /etc/rc.d/init.d/jit
%{_libdir}/jit
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jit
%attr(770,root,jabber) /var/log/%{name}
%attr(770,root,jabber) /var/lib/%{name}
