#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	C++ library for compression and CPU-GPU data transfer plugins
Summary(pl.UTF-8):	Biblioteka C++ do wtyczek kompresji i przesyłu danych CPU-GPU
Name:		Pression
Version:	2.0.0
Release:	6
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://github.com/Eyescale/Pression/releases
Source0:	https://github.com/Eyescale/Pression/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7b1546fa85838934a302776e5741b7f4
Source1:	https://github.com/facebook/zstd/archive/83543a7/zstd-83543a7.tar.gz
# Source1-md5:	81cd6ac24a536b544e78683a373bfeec
Source2:	https://github.com/google/snappy/archive/32d6d7d/snappy-32d6d7d.tar.gz
# Source2-md5:	e3c76d092a1405db503b92db2d65c81f
URL:		https://eyescale.github.io/
BuildRequires:	Eyescale-CMake >= 2017.05
BuildRequires:	Lunchbox-devel >= 1.16.0
# just to satisfy cmake projects stupidity (FIXME)
BuildRequires:	Servus-qt-devel
BuildRequires:	boost-devel >= 1.41.0
BuildRequires:	cmake >= 2.8
BuildRequires:	gcc-c++ >= 6:4.2
BuildRequires:	libgomp-devel
BuildRequires:	libstdc++-devel
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
C++ library for implementing and loading compression and CPU-GPU data
transfer plugins.

%description -l pl.UTF-8
Biblioteka C++ do implementowania i ładowania wtyczek kompresji oraz
przesyłu danych CPU-GPU.

%package devel
Summary:	Header files for Pression library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Pression
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Lunchbox-devel >= 1.16.0
Requires:	boost-devel >= 1.41.0

%description devel
Header files for Pression library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Pression.

%package apidocs
Summary:	Pression API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Pression
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Pression library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Pression.

%prep
%setup -q -a1 -a2

%{__mv} zstd-83543a7*/* pression/data/zstd/
%{__mv} snappy-32d6d7d*/* pression/data/snappy/

rmdir CMake/common
ln -s %{_datadir}/Eyescale-CMake CMake/common

%build
install -d build
cd build
%cmake .. \
	-DCOMMON_DISABLE_WERROR=ON

%{__make}

%if %{with apidocs}
doxygen doc/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/Pression/{doc,tests}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS.txt LICENSE.txt README.md doc/Changelog.md
%attr(755,root,root) %{_libdir}/libPression.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libPression.so.3
%attr(755,root,root) %{_libdir}/libPressionData.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libPressionData.so.3
%dir %{_datadir}/Pression
%{_datadir}/Pression/benchmarks

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libPression.so
%attr(755,root,root) %{_libdir}/libPressionData.so
%{_includedir}/pression
%{_datadir}/Pression/CMake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
