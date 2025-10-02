# TODO:
# - c extension build is done in install phase (http://bugs.mysql.com/bug.php?id=78621)
#
# Conditional build:
%bcond_with	tests		# build with tests (requires mysql server)

%define		pname	mysql-connector
Summary:	The MySQL Client/Protocol implemented in Python
Summary(pl.UTF-8):	Protokół kliencki MySQL zaimplementowany w Pythonie
Name:		python-%{pname}
# check documentation to see which version is GA (we don't want devel releases)
# https://dev.mysql.com/downloads/connector/python/
# python3 version in python3-mysql-connector.spec
Version:	8.0.23
Release:	3
License:	GPL v2
Group:		Libraries/Python
# Source0:	http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-%{version}-src.tar.gz
Source0:	https://pypi.debian.net/mysql-connector-python/mysql-connector-python-%{version}.tar.gz
# Source0-md5:	798f57c5e577a34787342821a0cb3a87
Patch0:		force-capi.patch
Patch1:		tests.patch
Patch2:		build.patch
Patch3:		py10.patch
URL:		http://dev.mysql.com/doc/connector-python/en/
BuildRequires:	mysql-devel
BuildRequires:	protobuf-devel >= 3.0.0
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with tests}
BuildRequires:	mysql
%endif
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL Connector/Python is implementing the MySQL Client/Server
protocol completely in Python. No MySQL libraries are needed, and no
compilation is necessary to run this Python DB API v2.0 compliant
driver.

%description -l pl.UTF-8
MySQL Connector/Python to protokół klient-serwer MySQL-a
zaimplementowany całkowicie w Pythonie. Do uruchomienia tego
sterownika, zgodnego z DB API v2.0 Pythona, nie są potrzebne
biblioteki MySQL-a, ani żadna kompilacja.

%prep
%setup -q -n mysql-connector-python-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
export MYSQLXPB_PROTOC=%{_bindir}/protoc
export MYSQLXPB_PROTOBUF_INCLUDE_DIR=%{_includedir}
export MYSQLXPB_PROTOBUF_LIB_DIR=%{_libdir}

%py_build
%if %{with tests}
export PYTHONPATH="$(pwd)/$(echo build-2/lib*)"
%{__python} unittests.py \
	--verbosity 1 \
	--keep --stats \
	--skip-install \
	--with-mysql=%{_prefix} \
	--with-mysql-share=%{_datadir}/mysql
%endif

%install
rm -rf $RPM_BUILD_ROOT

# see NOTE on beginning of the spec
export MYSQLXPB_PROTOC=%{_bindir}/protoc
export MYSQLXPB_PROTOBUF_INCLUDE_DIR=%{_includedir}
export MYSQLXPB_PROTOBUF_LIB_DIR=%{_libdir}

%py_install \
	--with-mysql-capi=%{_prefix}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt
%attr(755,root,root) %{py_sitedir}/_mysql_connector.so
%dir %{py_sitedir}/mysql
%{py_sitedir}/mysql/*.py[co]
%dir %{py_sitedir}/mysql/connector
%{py_sitedir}/mysql/connector/*.py[co]
%dir %{py_sitedir}/mysql/connector/django
%{py_sitedir}/mysql/connector/django/*.py[co]
%dir %{py_sitedir}/mysql/connector/locales
%{py_sitedir}/mysql/connector/locales/*.py[co]
%dir %{py_sitedir}/mysql/connector/locales/eng
%{py_sitedir}/mysql/connector/locales/eng/*.py[co]
%dir %{py_sitedir}/mysqlx
%{py_sitedir}/mysqlx/*.py[co]
%dir %{py_sitedir}/mysqlx/protobuf
%{py_sitedir}/mysqlx/protobuf/*.py[co]
%dir %{py_sitedir}/mysqlx/locales
%{py_sitedir}/mysqlx/locales/*.py[co]
%dir %{py_sitedir}/mysqlx/locales/eng
%{py_sitedir}/mysqlx/locales/eng/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitedir}/mysql_connector_python-*.egg-info
%endif
