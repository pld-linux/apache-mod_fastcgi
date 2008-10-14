%define		mod_name	fastcgi
%define 	apxs		/usr/sbin/apxs
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl.UTF-8):	Obsługa protokołu FastCGI dla serwera apache
Summary(ru.UTF-8):	FastCGI - более быстрая версия CGI
Summary(uk.UTF-8):	FastCGI - більш швидка версія CGI
Name:		apache-mod_%{mod_name}
# NOTE: remember about apache1-mod_fastcgi.spec when messing here
Version:	2.4.6
Release:	5
License:	distributable
Group:		Networking/Daemons
Source0:	http://www.FastCGI.com/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	a21a613dd5dacf4c8ad88c8550294fed
Patch0:		%{name}-allow-uid-gid.patch
Patch1:		%{name}-socketdir.patch
Patch3:		%{name}-segv-onload.patch
Patch4:		%{name}-apr1.patch
Patch5:		%{name}-apache22.patch
Source1:	%{name}.conf
URL:		http://www.FastCGI.com/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		apacheconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d
%define		apachelibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_socketdir	/var/run/httpd/fastcgi

%description
This 3rd party module provides support for the FastCGI protocol.
FastCGI is a language independent, scalable, open extension to CGI
that provides high performance and persistence without the limitations
of server specific APIs.

%description -l pl.UTF-8
To jest moduł apache dodający obsługę protokołu FastCGI. FastCGI jest
niezależnym od języka, skalowalnym, otwartym rozszerzeniem CGI dającym
dużą wydajność bez ograniczania API specyficznego dla serwera.

%description -l ru.UTF-8
FastCGI - расширение CGI, которое предоставляет возможность создавать
высокопроизводительные Internet-приложения без необходимости
использовать специфические для каждого web-сервера API.

Скорость API web-серверов со всеми преимуществами CGI.

%description -l uk.UTF-8
FastCGI - розширення CGI, яке надає можливість створювати
високопродуктивні Internet-програми без необхідності використання
специфічних для кожного web-серверу API.

Швидкість API web-серверів зі всіма перевагами CGI.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__make} -f Makefile.AP2 \
	top_dir=%{apachelibdir} \
	INCLUDES="-I%(%{apxs} -q INCLUDEDIR)" \
	EXTRA_CFLAGS='-DAPACHE22'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{apachelibdir},%{apacheconfdir},%{_socketdir}/dynamic}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{apachelibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{apacheconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc docs/LICENSE.TERMS CHANGES docs/*.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{apacheconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{apachelibdir}/*.so
%dir %attr(770,root,http) %{_socketdir}
%dir %attr(770,root,http) %{_socketdir}/dynamic
