Summary:	Support for the FastCGI protocol for apache webserver
Name:		apache-mod_fastcgi
Version:	2.2.10
Release:	1
Copyright:	Open Market
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	http://www.FastCGI.com/dist/mod_fastcgi_%{version}.tar.gz
URL:		http://www.FastCGI.com/
BuildRequires:	apache-devel
Requires:	apache >= 1.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _libexecdir     %{_libdir}/apache
%define         _htmldocdir     /home/httpd/html/docs/%{name}_%{version}

%description
This 3rd party module provides support for the FastCGI protocol.
FastCGI is a language independent, scalable, open extension to CGI
that provides high performance and persistence without the limitations
of server specific APIs.

%prep
%setup -q -n mod_fastcgi_%{version}

%build
apxs -D SUEXEC_BIN="\"\\\"/usr/sbin/suexec\\\"\"" -o mod_fastcgi.so -c *.c
strip mod_fastcgi.so

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
