#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	C++ library for compression and CPU-GPU data transfer plugins
Name:		Pression
Version:	1.1.1
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	https://github.com/Eyescale/Pression/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0eef1d53cdfbf53feebff1dfe9980161
URL:		http://libcollage.net/
BuildRequires:	Lunchbox-devel >= 1.13.0
BuildRequires:	boost-devel >= 1.41.0
BuildRequires:	cmake >= 2.8
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Collage is a cross-platform C++ library for building heterogenous,
distributed applications. Among other things, it is the cluster
backend for the Equalizer parallel rendering framework. Collage
provides an abstraction of different network connections, peer-to-peer
messaging, node discovery, synchronization and high-performance,
object-oriented, versioned data distribution. Collage is designed for
low-overhead multi-threaded execution which allows applications to
easily exploit multi-core architectures.

%package devel
Summary:	Header files for Pression library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Pression
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Pression library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Pression.

%package apidocs
Summary:	Pression API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Pression
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Pression library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Pression.

%prep
%setup -q

ln -s %{_datadir}/Eyescale-CMake CMake/common
%{__rm} .gitexternals

%build
install -d build
cd build
CXXFLAGS="%{rpmcxxflags} -Wno-unused-variable"
%cmake .. \
	-DBUILDYARD_DISABLED=ON
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
%doc LICENSE.txt README.md doc/Changelog.md
%attr(755,root,root) %{_libdir}/libPression.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libPression.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libPression.so
%{_includedir}/pression
%dir %{_datadir}/Pression
%{_datadir}/Pression/CMake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
