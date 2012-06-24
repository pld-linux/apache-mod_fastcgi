%define 	apxs	/usr/sbin/apxs
%define		_apache1        %(rpm -q apache-devel 2> /dev/null | grep -Eq '\\-2\\.[0-9]+\\.' && echo 0 || echo 1)
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl):	Obs�uga protoko�u FastCGI dla serwera apache
Summary(ru):	FastCGI - ����� ������� ������ CGI
Summary(uk):	FastCGI - ¦��� ������ ���Ӧ� CGI
Name:		apache-mod_fastcgi
Version:	2.4.2
Release:	1
License:	distributable
Group:		Networking/Daemons
Source0:	http://www.FastCGI.com/dist/mod_fastcgi-%{version}.tar.gz
# Source0-md5:	e994414304b535cb99e10b7d1cad1d1e
Source1:	70_mod_fastcgi.conf
URL:		http://www.FastCGI.com/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	libtool
Requires(post,preun):	%{apxs}
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
To jest modu� apache dodaj�cy obs�ug� protoko�u FastCGI. FastCGI jest
niezale�nym od j�zyka, skalowalnym, otwartym rozszerzeniem CGI daj�cym
du�� wydajno�� bez ograniczania API specyficznego dla serwera.

%description -l ru
FastCGI - ���������� CGI, ������� ������������� ����������� ���������
���������������������� Internet-���������� ��� �������������
������������ ������������� ��� ������� web-������� API.

�������� API web-�������� �� ����� �������������� CGI.

%description -l uk
FastCGI - ���������� CGI, ��� ����� �����צ��� ����������
���������������Φ Internet-�������� ��� ����Ȧ����Ԧ ������������
�����Ʀ���� ��� ������� web-������� API.

����˦��� API web-�����Ҧ� ڦ �Ӧ�� ���������� CGI.

%prep
%setup -q -n mod_fastcgi-%{version}

%build
%if %{_apache1}
%{apxs} -o mod_fastcgi.so -c *.c
%else
%{__make} -f Makefile.AP2 top_dir=%{_libexecdir} INCLUDES="-I%{_includedir}/apache"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libexecdir},%{_htmldocdir}}

%if %{_apache1}
install mod_fastcgi.so $RPM_BUILD_ROOT%{_libexecdir}
%else
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/httpd/httpd.conf
libtool --mode=install install mod_fastcgi.la $RPM_BUILD_ROOT%{_libexecdir}
install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/httpd.conf/
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
%attr(755,root,root) %{_libexecdir}/*
%if ! %{_apache1}
%config %{_sysconfdir}/httpd/httpd.conf/*.conf
%endif
