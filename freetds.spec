%define	name	        freetds
%define	version	        1.00.86
%define prefix          /usr
# define with-unixodbc   /usr
# define with-openssl    /usr/lib64/openssl
# define enable-msdblib  yes
# This command shows the value returned for the Library Directory - rpm --eval '%{_libdir}'

# compute some additional dependency from vendor name
# 

# SUSE
%define tds_dep_suse glibc-locale

%undefine tds_builddep
%{expand:%%{expand:%%{?tds_builddep_%{?_vendor}:%%%%define tds_builddep %%{?tds_builddep_%{?_vendor}}}}}
%undefine tds_dep
%{expand:%%{expand:%%{?tds_dep_%{?_vendor}:%%%%define tds_dep %%{?tds_dep_%{?_vendor}}}}}
 
Name: %{name} 
Version: %{version} 
Release: 1 
Vendor: www.freetds.org 
License: LGPL 
Group: System Environment/Libraries 
Source: http://ibiblio.org/pub/Linux/ALPHA/freetds/stable/%{name}-%{version}.tar.bz2
# BuildRoot: %{_tmppath}/%{name}-buildroot
# BuildRequires: unixODBC-devel >= 2.0.0 gnutls-devel %{?tds_builddep}
# Requires: gnutls %{?tds_dep}
Summary: FreeTDS is a free re-implementation of the TDS (Tabular DataStream) protocol that is used by Sybase and Microsoft for their database products. 
 
%description 
FreeTDS is a project to document and implement the TDS (Tabular DataStream) 
protocol. TDS is used by Sybase and Microsoft for client to database server 
communications. FreeTDS includes call level interfaces for DB-Lib, CT-Lib, 
and ODBC.  
 
%package devel 
Group: Development/Libraries 
Summary: Include files needed for development with FreeTDS 
Requires: freetds = %{version}

%package unixodbc
Group: System Environment/Libraries
Summary: FreeTDS ODBC Driver for unixODBC
Requires: unixODBC >= 2.0.0
%{?tds_dep:Requires: %tds_dep}

%package doc
Group: Documentation
Summary: User documentation for FreeTDS
 
%description devel
The freetds-devel package contains the files necessary for development with 
the FreeTDS libraries. 

%description unixodbc
The freetds-unixodbc package contains ODBC driver build for unixODBC.

%description doc
The freetds-doc package contains the useguide and reference of FreeTDS 
and can be installed even if FreeTDS main package is not installed

%prep
%setup 
 
%build
ODBCDIR=/tmp/unixODBC-2.3.1-1
if test ! -r "$ODBCDIR/include/sql.h"; then
	ODBCDIR=/usr
fi
if test ! -r "$ODBCDIR/include/sql.h"; then
	ODBCDIR=/usr
fi
%configure --with-tdsver=auto --with-unixodbc=/usr --enable-msdblib --with-openssl=/usr/lib64/openssl
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"
 
%install 
rm -rf "$RPM_BUILD_ROOT"
make DESTDIR="$RPM_BUILD_ROOT" install
rm -rf "$RPM_BUILD_ROOT/%{_datadir}/doc/freetds"

%post 
/sbin/ldconfig 2> /dev/null

%postun
/sbin/ldconfig 2> /dev/null

%post unixodbc
echo "[FreeTDS]
Description = FreeTDS unixODBC Driver
Driver = /usr/lib64/libtdsodbc.so.0
Setup = /usr/lib64/libtdsodbc.so.0" | odbcinst -i -d -r > /dev/null 2>&1 || true
echo "[SQL Server]
Description = FreeTDS unixODBC Driver
Driver = /usr/lib64/libtdsodbc.so.0
Setup = /usr/lib64/libtdsodbc.so.0" | odbcinst -i -d -r > /dev/null 2>&1 || true

%preun unixodbc
odbcinst -u -d -n 'FreeTDS' > /dev/null 2>&1 || true
odbcinst -u -d -n 'SQL Server' > /dev/null 2>&1 || true

%clean 
rm -rf $RPM_BUILD_ROOT 
 
%files 
%defattr(-,root,root) 
%doc AUTHORS BUGS COPYING* ChangeLog INSTALL NEWS README TODO 
%{_bindir}/*
%{_mandir}/man?/*
%{_libdir}/libct.so.*
%{_libdir}/libsybdb.so.*
%config %{_sysconfdir}/*
 
%files devel 
%defattr (-,root,root) 
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*

%files unixodbc
%defattr(-,root,root)
%{_libdir}/libtdsodbc.so*

%files doc
%defattr (-,root,root)
%doc doc/userguide doc/images doc/reference
 

