%define 	apxs	/usr/sbin/apxs
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl):	ObsЁuga protokoЁu FastCGI dla serwera apache
Summary(ru):	FastCGI - более быстрая версия CGI
Summary(uk):	FastCGI - б╕льш швидка верс╕я CGI
Name:		apache-mod_fastcgi
Version:	2.2.12
Release:	1
License:	Open Market
Group:		Networking/Daemons
Source0:	http://www.FastCGI.com/dist/mod_fastcgi-%{version}.tar.gz
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
To jest moduЁ apache dodaj╠cy obsЁugЙ protokoЁu FastCGI. FastCGI jest
niezale©nym od jЙzyka, skalowalnym, otwartym rozszerzeniem CGI daj╠cym
du©╠ wydajno╤Ф bez ograniczania API specificznego dla serwera.

%description -l ru
FastCGI - расширение CGI, которое предоставляет возможность создавать
высокопроизводительные Internet-приложения без необходимости
использовать специфические для каждого web-сервера API.

Скорость API web-серверов со всеми преимуществами CGI.

%description -l uk
FastCGI - розширення CGI, яке нада╓ можлив╕сть створювати
високопродуктивн╕ Internet-програми без необх╕дност╕ використання
специф╕чних для кожного web-серверу API.

Швидк╕сть API web-сервер╕в з╕ вс╕ма перевагами CGI.

%prep
%setup -q -n mod_fastcgi-%{version}

%build
%{apxs} -D SUEXEC_BIN="\"\\\"%{_sbindir}/suexec\\\"\"" -o mod_fastcgi.so -c *.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libexecdir},%{_htmldocdir}}

install mod_fastcgi.so $RPM_BUILD_ROOT%{_libexecdir}

install docs/*.html $RPM_BUILD_ROOT%{_htmldocdir}

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
%doc docs/LICENSE.TERMS CHANGES
%doc %{_htmldocdir}/*
%attr(755,root,root) %{_libexecdir}/*
