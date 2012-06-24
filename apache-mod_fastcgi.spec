%define		mod_name	fastcgi
%define 	apxs		/usr/sbin/apxs
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl):	Obs�uga protoko�u FastCGI dla serwera apache
Summary(ru):	FastCGI - ����� ������� ������ CGI
Summary(uk):	FastCGI - ¦��� ������ ���Ӧ� CGI
Name:		apache-mod_%{mod_name}
Version:	2.4.2
Release:	3
License:	distributable
Group:		Networking/Daemons
Source0:	http://www.FastCGI.com/dist/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	e994414304b535cb99e10b7d1cad1d1e
Patch0:		%{name}-allow-uid-gid.patch
Source1:	%{name}.conf
URL:		http://www.FastCGI.com/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2
BuildRequires:	libtool
Requires(post,preun):	%{apxs}
Requires:	apache >= 2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

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
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{__make} -f Makefile.AP2 \
	top_dir=%{_pkglibdir} \
	INCLUDES="-I%(%{apxs} -q INCLUDEDIR)"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd.conf/

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
 
%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi
 
%files
%defattr(644,root,root,755)
%doc docs/LICENSE.TERMS CHANGES docs/*.html
%attr(755,root,root) %{_pkglibdir}/*.so
%config %{_sysconfdir}/httpd.conf/*.conf
