%define 	apxs	/usr/sbin/apxs
Summary:	Support for the FastCGI protocol for apache webserver
Summary(pl):	Obs�uga protoko�u FastCGI dla serwera apache
Summary(ru):	FastCGI - ����� ������� ������ CGI
Summary(uk):	FastCGI - ¦��� ������ ���Ӧ� CGI
Name:		apache-mod_fastcgi
Version:	2.2.10
Release:	4
License:	Open Market
Group:		Networking/Daemons
Group(cs):	S�ov�/D�moni
Group(da):	Netv�rks/D�moner
Group(de):	Netzwerkwesen/Server
Group(es):	Red/Servidores
Group(fr):	R�seau/Serveurs
Group(is):	Net/P�kar
Group(it):	Rete/Demoni
Group(no):	Nettverks/Daemoner
Group(pl):	Sieciowe/Serwery
Group(pt):	Rede/Servidores
Group(ru):	����/������
Group(sl):	Omre�ni/Stre�niki
Group(sv):	N�tverk/Demoner
Group(uk):	������/������
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
To jest modu� apache dodaj�cy obs�ug� protoko�u FastCGI. FastCGI jest
niezale�nym od j�zyka, skalowalnym, otwartym rozszerzeniem CGI daj�cym
du�� wydajno�� bez ograniczania API specificznego dla serwera.

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
