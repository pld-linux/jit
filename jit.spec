#
# Conditional build:
#
# _without_version	- show shorter version string answering the
#                         version query

Summary:	ICQ transport daemon for Jabber
Summary(pl):	Demon transportowy ICQ dla systemu Jabber
Name:		jit
Version:	1.1.6
Release:	1
License:	GPL
Group:		Applications/Communications
Source0:	http://files.jabberstudio.org/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	950f6b82ab5e0542535108fd54409363
Source1:	%{name}.xml
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-version.patch
URL:		http://jit.jabberstudio.org/
Requires(post):	jabber-common
Requires(post,preun):	/sbin/chkconfig
Requires(post):	fileutils
Requires:	jabber-common
Obsoletes:	jabber-icq-transport
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This daemon allows Jabber to communicate with ICQ servers.

%description -l pl
Demon ten umo¿liwia u¿ytkownikom Jabbera komunikowanie siê z
u¿ytkownikami ICQ.

%prep
%setup -q
%{?_without_version:%patch0 -p1}

%build
%configure
%{__make}
cd xdb_file
%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}/jabber,%{_libdir}/jit,/var/log/%{name}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}{/rc.d/init.d,/sysconfig},/var/lib/%{name}}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/jabber
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

install jabberd/jabberd $RPM_BUILD_ROOT%{_sbindir}/jit
install jit/jit.so xdb_file/xdb_file.so $RPM_BUILD_ROOT%{_libdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
        	echo "Updating component authentication secret in jit.xml..."
		perl -pi -e "s/>secret</>$SECRET</" /etc/jabber/jit.xml
	fi
fi
/sbin/chkconfig --add jit
if [ -r /var/lock/subsys/jit ]; then
	/etc/rc.d/init.d/jit restart >&2
else
	echo "Run \"/etc/rc.d/init.d/jit start\" to start Jabber ICQ transport daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jit ]; then
		/etc/rc.d/init.d/jit stop >&2
	fi
	/sbin/chkconfig --del jit
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS jit/ChangeLog README jit/TODO jit/INSTALL doc/FAQ
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/jit.xml
%attr(754,root,root) /etc/rc.d/init.d/jit
%{_libdir}/jit
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jit
%attr(770,root,jabber) /var/log/%{name}
%attr(770,root,jabber) /var/lib/%{name}
