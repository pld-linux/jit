Summary:	ICQ transport daemon for Jabber
Summary(pl):	Demon transportowy ICQ dla systemu Jabber
Name:		jit
Version:	1.0.9
Release:	0.2
License:	GPL
Group:		Applications/Communications
Source0:	http://telia.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.xml
Source2:    %{name}.init
Source3:    %{name}.sysconfig
Requires:	jabber-icq-transport
URL:		http://jit.sourceforge.net/

BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This daemon allows Jabber to communicate with ICQ servers.

%description -l pl
Demon ten umo¿liwia u¿ytkownikom Jabbera komunikowanie siê z
u¿ytkownikami ICQ.

%prep
%setup -q

%build
./configure --icq
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},/var/log/%{name}} \
	$RPM_BUILD_ROOT%{_sysconfdir}{/rc.d/init.d,/sysconfig}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}

install jabberd/jabberd-icq $RPM_BUILD_ROOT%{_sbindir}/jit

%clean
rm -rf $RPM_BUILD_ROOT

%post
mv -f /etc/jabberd/icqtrans.xml /etc/jabberd/icqtrans.xml.off
echo "WARNING: Jabber ICQ transport *module* has been disabled for the *daemon*"
echo "to work correctly."
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
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO INSTALL doc/FAQ
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jit.xml
%attr(754,root,root) /etc/rc.d/init.d/jit
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/jit
%attr(770,root,jabber) /var/log/%{name}
