%define 	apxs	/usr/sbin/apxs
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl):	Obs³uga protoko³u FastCGI dla serwera apache
Summary(ru):	FastCGI - ÂÏÌÅÅ ÂÙÓÔÒÁÑ ×ÅÒÓÉÑ CGI
Summary(uk):	FastCGI - Â¦ÌØÛ Û×ÉÄËÁ ×ÅÒÓ¦Ñ CGI
Name:		apache-mod_fastcgi
Version:	2.2.10
Release:	4
License:	Open Market
Group:		Networking/Daemons
Group(cs):	Sí»ové/Démoni
Group(da):	Netværks/Dæmoner
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	Réseau/Serveurs
Group(is):	Net/Púkar
Group(it):	Rete/Demoni
Group(no):	Nettverks/Daemoner
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Servidores
Group(ru):	óÅÔØ/äÅÍÏÎÙ
Group(sl):	Omre¾ni/Stre¾niki
Group(sv):	Nätverk/Demoner
Group(uk):	íÅÒÅÖÁ/äÅÍÏÎÉ
Source0:	http://www.FastCGI.com/dist/mod_fastcgi_%{version}.tar.gz
URL:		http://www.FastCGI.com/
BuildRequires:	apache-devel
BuildRequires:	%{apxs}
Prereq:		%{_sbindir}/apxs
Requires:	apache >= 1.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _libexecdir     %{_libdir}/apache
%define         _htmldocdir     /home/httpd/manual/mod

%description
This 3rd party module provides support for the FastCGI protocol.
FastCGI is a language independent, scalable, open extension to CGI
that provides high performance and persistence without the limitations
of server specific APIs.

%description -l pl
To jest modu³ apache dodaj±cy obs³ugê protoko³u FastCGI. FastCGI jest
niezale¿nym od jêzyka, skalowalnym, otwartym rozszerzeniem CGI daj±cym
du¿± wydajno¶æ bez ograniczania API specificznego dla serwera.

%description -l ru
FastCGI - ÒÁÓÛÉÒÅÎÉÅ CGI, ËÏÔÏÒÏÅ ÐÒÅÄÏÓÔÁ×ÌÑÅÔ ×ÏÚÍÏÖÎÏÓÔØ ÓÏÚÄÁ×ÁÔØ
×ÙÓÏËÏÐÒÏÉÚ×ÏÄÉÔÅÌØÎÙÅ Internet-ÐÒÉÌÏÖÅÎÉÑ ÂÅÚ ÎÅÏÂÈÏÄÉÍÏÓÔÉ
ÉÓÐÏÌØÚÏ×ÁÔØ ÓÐÅÃÉÆÉÞÅÓËÉÅ ÄÌÑ ËÁÖÄÏÇÏ web-ÓÅÒ×ÅÒÁ API.

óËÏÒÏÓÔØ API web-ÓÅÒ×ÅÒÏ× ÓÏ ×ÓÅÍÉ ÐÒÅÉÍÕÝÅÓÔ×ÁÍÉ CGI.

%description -l uk
FastCGI - ÒÏÚÛÉÒÅÎÎÑ CGI, ÑËÅ ÎÁÄÁ¤ ÍÏÖÌÉ×¦ÓÔØ ÓÔ×ÏÒÀ×ÁÔÉ
×ÉÓÏËÏÐÒÏÄÕËÔÉ×Î¦ Internet-ÐÒÏÇÒÁÍÉ ÂÅÚ ÎÅÏÂÈ¦ÄÎÏÓÔ¦ ×ÉËÏÒÉÓÔÁÎÎÑ
ÓÐÅÃÉÆ¦ÞÎÉÈ ÄÌÑ ËÏÖÎÏÇÏ web-ÓÅÒ×ÅÒÕ API.

û×ÉÄË¦ÓÔØ API web-ÓÅÒ×ÅÒ¦× Ú¦ ×Ó¦ÍÁ ÐÅÒÅ×ÁÇÁÍÉ CGI.

%prep
%setup -q -n mod_fastcgi_%{version}

%build
%{apxs} -D SUEXEC_BIN="\"\\\"%{_sbindir}/suexec\\\"\"" -o mod_fastcgi.so -c *.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libexecdir},%{_htmldocdir}}

install mod_fastcgi.so $RPM_BUILD_ROOT%{_libexecdir}

install docs/*.html $RPM_BUILD_ROOT%{_htmldocdir}

gzip -9nf docs/LICENSE.TERMS CHANGES

%post
%{_sbindir}/apxs -e -a -n fastcgi %{_libexecdir}/mod_fastcgi.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/apxs -e -A -n fastcgi %{_libexecdir}/mod_fastcgi.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*.gz *.gz
%doc %{_htmldocdir}
%attr(755,root,root) %{_libexecdir}/*
