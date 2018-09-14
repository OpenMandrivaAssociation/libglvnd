%global __provides_exclude_from %{_libdir}/%{name}
%global __requires_exclude_from %{_libdir}/%{name}

%define _disable_ld_as_needed 1

%define major 0
%define libgldispatch %mklibname gldispatch %{major}
%define libopengl %mklibname opengl %{major}
%define devname %mklibname glvnd -d

%define libEGL %mklibname EGL 1
%define libGLdispatch %mklibname GLdispatch 0
%define libGLESv1 %mklibname GLESv1_CM 1
%define libGLESv2 %mklibname GLESv2 2
%define libGL %mklibname GL 1
%define libGLX %mklibname GLX 0
%define libOpenGL %mklibname OpenGL 0

Summary:	The GL Vendor-Neutral Dispatch library
Name:		libglvnd
Version:	1.1.0
Release:	4
License:	MIT
Group:		System/Libraries
Url:		https://github.com/NVIDIA/libglvnd
Source0:	https://github.com/NVIDIA/libglvnd/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	python-libxml2
BuildRequires:	pkgconfig(glproto)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)

%description
libglvnd is an implementation of the vendor-neutral dispatch layer for
arbitrating OpenGL API calls between multiple vendors on a per-screen basis.

%files
%doc README.md
%dir %{_sysconfdir}/glvnd
%dir %{_datadir}/glvnd
%dir %{_sysconfdir}/glvnd/egl_vendor.d
%dir %{_datadir}/glvnd/egl_vendor.d
%dir %{_sysconfdir}/egl/egl_external_platform.d/
%dir %{_datadir}/egl/egl_external_platform.d/

#----------------------------------------------------------------------------
%package -n %{libEGL}
Summary:	LibEGL wrapper from libglvnd
Recommends:	mesa-libEGL%{?_isa}
Provides:	libglvnd-egl

%description -n %{libEGL}
LibEGL wrapper from libglvnd

%files -n %{libEGL}
%{_libdir}/libEGL.so.1*


#----------------------------------------------------------------------------
%package -n %{libGLdispatch}
Summary:	LibGL dispatcher from libglvnd
Requires:	%{libGL} = %{EVRD}
Provides:	libglvnd-GLdispatch

%description -n %{libGLdispatch}
LibGL dispatcher from libglvnd

%files -n %{libGLdispatch}
%{_libdir}/libGLdispatch.so.0*


#----------------------------------------------------------------------------
%package -n %{libGLESv1}
Summary:	LibGLESv1 wrapper from libglvnd
Recommends:	mesa-libGLESv1%{?_isa}
%rename %{_lib}glesv1_1
Provides:	libglvnd-GLESv1_CM

%description -n %{libGLESv1}
LibGLESv1 wrapper from libglvnd

%files -n %{libGLESv1}
%{_libdir}/libGLESv1_CM.so.1*


#----------------------------------------------------------------------------
%package -n %{libGLESv2}
Summary:	LibGLESv2 wrapper from libglvnd
Recommends:	mesa-libGLESv2%{?_isa}
%rename %{_lib}glesv2_2
Provides:	libglvnd-GLESv2

%description -n %{libGLESv2}
LibGLESv2 wrapper from libglvnd

%files -n %{libGLESv2}
%{_libdir}/libGLESv2.so.2*


#----------------------------------------------------------------------------
%package -n %{libGL}
Summary:	LibGL wrapper from libglvnd
Recommends:	mesa-libGL%{?_isa}
%define oldgl %mklibname gl 1
%rename %{oldgl}
Provides:	libglvnd-GL

%description -n %{libGL}
LibGL wrapper from libglvnd

%files -n %{libGL}
%{_libdir}/libGL.so.1*


#----------------------------------------------------------------------------
%package -n %{libGLX}
Summary:	LibGLX wrapper from libglvnd
Recommends:	mesa-libGL%{?_isa}
Provides:	libglvnd-GLX

%description -n %{libGLX}
LibGLX wrapper from libglvnd

%files -n %{libGLX}
%{_libdir}/libGLX.so.0*


#----------------------------------------------------------------------------
%package -n %{libOpenGL}
Summary:	OpenGL wrapper from libglvnd
Provides:	libglvnd-OpenGL

%description -n %{libOpenGL}
OpenGL wrapper from libglvnd

%files -n %{libOpenGL}
%{_libdir}/libOpenGL.so.0*


#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libEGL} = %{EVRD}
Requires:	%{libGLdispatch} = %{EVRD}
Requires:	%{libGLESv1} = %{EVRD}
Requires:	%{libGLESv2} = %{EVRD}
Requires:	%{libGL} = %{EVRD}
Requires:	%{libGLX} = %{EVRD}
Requires:	%{libOpenGL} = %{EVRD}

%description -n %{devname}
This package is a bootstrap trick for Mesa, which wants to build against
the libglvnd headers but does not link against any of its libraries (and,
initially, has file conflicts with them).

%files -n %{devname}
%dir %{_includedir}/glvnd
%{_includedir}/glvnd/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libEGL.so
%{_libdir}/libGLdispatch.so
%{_libdir}/libGLX.so
%{_libdir}/libGL.so
%{_libdir}/libOpenGL.so


#----------------------------------------------------------------------------

%prep
%setup -q

%build
%global optflags %{optflags} -Wstrict-aliasing=0
autoreconf -vif
%configure \
	--disable-static \
	--enable-asm \
	--enable-tls

%make

%install
%makeinstall_std

# Create directory layout
mkdir -p %{buildroot}%{_sysconfdir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_sysconfdir}/egl/egl_external_platform.d
mkdir -p %{buildroot}%{_datadir}/egl/egl_external_platform.d

# *.so symlinks are useless because the headers live
# in mesa anyway -- let's put the *.so files with the headers.
rm -f	%{buildroot}%{_libdir}/libGLESv1_CM.so \
	%{buildroot}%{_libdir}/libGLESv2.so
