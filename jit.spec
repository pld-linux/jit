Summary:	ICQ transport daemon for Jabber
Summary(pl):	Demon transportowy ICQ dla systemu Jabber
Name:		jit
Version:	1.0.9
Release:	0.1
License:	GPL
Group:		Applications/Communications
Source0:	http://telia.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	jit.xml
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
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir}}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install jabberd/jabberd-icq $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO INSTALL doc/FAQ
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
