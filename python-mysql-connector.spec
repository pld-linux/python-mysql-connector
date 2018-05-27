# TODO:
# - c extension build is done in install phase (http://bugs.mysql.com/bug.php?id=78621)
#
# Conditional build:
%bcond_with		tests		# build with tests (requires mysql server)
%bcond_without	python3		# build without python3

%define		pname	mysql-connector
Summary:	The MySQL Client/Protocol implemented in Python
Name:		python-%{pname}
# check documentation to see which version is GA (we don't want devel releases)
# https://dev.mysql.com/downloads/connector/python/
Version:	8.0.11
Release:	1
License:	GPL v2
Group:		Libraries/Python
Source0:	http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-%{version}.zip
# Source0-md5:	d47704b39d794b287d146c3d772ab896
Patch0:		32bit.patch
URL:		http://dev.mysql.com/doc/connector-python/en/
BuildRequires:	mysql-devel
BuildRequires:	protobuf-devel
BuildRequires:	python-devel
BuildRequires:	python-modules
%{?with_python3:BuildRequires:	python3-modules}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL Connector/Python is implementing the MySQL Client/Server
protocol completely in Python. No MySQL libraries are needed, and no
compilation is necessary to run this Python DB API v2.0 compliant
driver. An interface to the popular MySQL database server for Python.

%package -n python3-%{pname}
Summary:	The MySQL Client/Protocol implemented in Python
Group:		Development/Languages/Python
Requires:	python3-modules

%description -n python3-%{pname}
MySQL Connector/Python is implementing the MySQL Client/Server
protocol completely in Python. No MySQL libraries are needed, and no
compilation is necessary to run this Python DB API v2.0 compliant
driver. An interface to the popular MySQL database server for Python.

%prep
%setup -q -n mysql-connector-python-%{version}
%patch0 -p1

%build
export MYSQLXPB_PROTOC=%{_bindir}/protoc
export MYSQLXPB_PROTOBUF_INCLUDE_DIR=%{_includedir}
export MYSQLXPB_PROTOBUF_LIB_DIR=%{_libdir}

%py_build
%{?with_tests:%{__python} setup.py test}

%if %{with python3}
%py3_build
%{?with_tests:%{__python3} setup.py test}
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

%if %{with python3}
%py3_install \
	--with-mysql-capi=%{_prefix}
%endif

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
%dir %{py_sitedir}/mysql/connector/fabric
%{py_sitedir}/mysql/connector/fabric/*.py[co]
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

%if %{with python3}
%files -n python3-%{pname}
%defattr(644,root,root,755)
%doc CHANGES.txt README.txt
%attr(755,root,root) %{py3_sitedir}/_mysql_connector.cpython-*.so
%{py3_sitedir}/mysql*.egg-info
%dir %{py3_sitedir}/mysql
%{py3_sitedir}/mysql/*.py
%dir %{py3_sitedir}/mysql/__pycache__
%{py3_sitedir}/mysql/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysql/connector
%{py3_sitedir}/mysql/connector/*.py
%dir %{py3_sitedir}/mysql/connector/__pycache__
%{py3_sitedir}/mysql/connector/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysql/connector/django
%{py3_sitedir}/mysql/connector/django/*.py
%dir %{py3_sitedir}/mysql/connector/django/__pycache__
%{py3_sitedir}/mysql/connector/django/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysql/connector/fabric
%{py3_sitedir}/mysql/connector/fabric/*.py
%dir %{py3_sitedir}/mysql/connector/fabric/__pycache__
%{py3_sitedir}/mysql/connector/fabric/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysql/connector/locales
%{py3_sitedir}/mysql/connector/locales/*.py
%dir %{py3_sitedir}/mysql/connector/locales/__pycache__
%{py3_sitedir}/mysql/connector/locales/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysql/connector/locales/eng
%{py3_sitedir}/mysql/connector/locales/eng/*.py
%dir %{py3_sitedir}/mysql/connector/locales/eng/__pycache__
%{py3_sitedir}/mysql/connector/locales/eng/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysqlx
%{py3_sitedir}/mysqlx/*.py
%dir %{py3_sitedir}/mysqlx/__pycache__
%{py3_sitedir}/mysqlx/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysqlx/locales
%{py3_sitedir}/mysqlx/locales/*.py
%dir %{py3_sitedir}/mysqlx/locales/__pycache__
%{py3_sitedir}/mysqlx/locales/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysqlx/locales/eng
%{py3_sitedir}/mysqlx/locales/eng/*.py
%dir %{py3_sitedir}/mysqlx/locales/eng/__pycache__
%{py3_sitedir}/mysqlx/locales/eng/__pycache__/*.py[co]
%dir %{py3_sitedir}/mysqlx/protobuf
%{py3_sitedir}/mysqlx/protobuf/*.py
%dir %{py3_sitedir}/mysqlx/protobuf/__pycache__
%{py3_sitedir}/mysqlx/protobuf/__pycache__/*.py[co]
%endif
