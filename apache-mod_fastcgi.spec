%define		mod_name	fastcgi
%define 	apxs		/usr/sbin/apxs
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl):	ObsЁuga protokoЁu FastCGI dla serwera apache
Summary(ru):	FastCGI - более быстрая версия CGI
Summary(uk):	FastCGI - б╕льш швидка верс╕я CGI
Name:		apache-mod_%{mod_name}
# NOTE: remember about apache1-mod_fastcgi.spec when messing here
Version:	2.4.2
Release:	8
License:	distributable
Group:		Networking/Daemons
Source0:	http://www.FastCGI.com/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	e994414304b535cb99e10b7d1cad1d1e
Patch0:		%{name}-apr1.patch
Patch1:		%{name}-allow-uid-gid.patch
Patch2:		%{name}-socketdir.patch
Patch3:		%{name}-apache22.patch
Source1:	%{name}.conf
URL:		http://www.FastCGI.com/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)
%define		_socketdir	/var/run/httpd/fastcgi

%description
This 3rd party module provides support for the FastCGI protocol.
FastCGI is a language independent, scalable, open extension to CGI
that provides high performance and persistence without the limitations
of server specific APIs.

%description -l pl
To jest moduЁ apache dodaj╠cy obsЁugЙ protokoЁu FastCGI. FastCGI jest
niezale©nym od jЙzyka, skalowalnym, otwartym rozszerzeniem CGI daj╠cym
du©╠ wydajno╤Ф bez ograniczania API specyficznego dla serwera.

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
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} -f Makefile.AP2 \
	top_dir=%{_pkglibdir} \
	INCLUDES="-I%(%{apxs} -q INCLUDEDIR)" \
	EXTRA_CFLAGS='-DAPACHE22'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf,%{_socketdir}/dynamic}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%preun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc docs/LICENSE.TERMS CHANGES docs/*.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
%dir %attr(770,root,http) %{_socketdir}
%dir %attr(770,root,http) %{_socketdir}/dynamic
