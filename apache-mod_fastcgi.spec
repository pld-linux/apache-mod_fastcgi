%define		mod_name	fastcgi
%define 	apxs		/usr/sbin/apxs
%define		_apache1        %(rpm -q apache-devel 2> /dev/null | grep -Eq '\\-2\\.[0-9]+\\.' && echo 0 || echo 1)
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl):	ObsЁuga protokoЁu FastCGI dla serwera apache
Summary(ru):	FastCGI - более быстрая версия CGI
Summary(uk):	FastCGI - б╕льш швидка верс╕я CGI
Name:		apache-mod_%{mod_name}
Version:	2.4.2
Release:	2
License:	distributable
Group:		Networking/Daemons
Source0:	http://www.FastCGI.com/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	e994414304b535cb99e10b7d1cad1d1e
Patch0:		%{name}-allow-uid-gid.patch
Source1:	70_mod_%{mod_name}.conf
URL:		http://www.FastCGI.com/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	libtool
Requires(post,preun):	%{apxs}
Requires:	apache >= 1.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_htmldocdir	/home/httpd/manual/mod

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

%build
%if %{_apache1}
%{apxs} -o mod_%{mod_name}.so -c *.c
%else
%{__make} -f Makefile.AP2 top_dir=%{_pkglibdir} INCLUDES="-I%(%{apxs} -q INCLUDEDIR)"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_htmldocdir}}

%if %{_apache1}
install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
%else
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
libtool --mode=install install mod_%{mod_name}.la $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd.conf/
%endif

install docs/*.html $RPM_BUILD_ROOT%{_htmldocdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{_apache1}
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
%endif
if [ -f /var/lock/subsys/httpd ]; then
        /etc/rc.d/init.d/httpd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
fi
 
%preun
if [ "$1" = "0" ]; then
%if %{_apache1}
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
%endif
        if [ -f /var/lock/subsys/httpd ]; then
                /etc/rc.d/init.d/httpd restart 1>&2
        fi
fi
 
%files
%defattr(644,root,root,755)
%doc docs/LICENSE.TERMS CHANGES
%doc %{_htmldocdir}/*
%attr(755,root,root) %{_pkglibdir}/*.so
%if ! %{_apache1}
%config %{_sysconfdir}/httpd.conf/*.conf
%endif
