%global __provides_exclude_from %{_libdir}/%{name}
%global __requires_exclude_from %{_libdir}/%{name}

%define _disable_ld_as_needed 1
%global optflags %{optflags} -O3 -Wstrict-aliasing=0
# (tpg) 2019-10-04 https://github.com/NVIDIA/libglvnd/issues/191
%ifnarch %{riscv}
%global ldflags %{ldflags} -fuse-ld=gold
%endif

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
Version:	1.2.0
Release:	4
License:	MIT
Group:		System/Libraries
Url:		https://github.com/NVIDIA/libglvnd
Source0:	https://github.com/NVIDIA/libglvnd/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch0:		update-gl-h-to-match-mesa.patch
Patch1:		egl-sync-with-khronos.patch
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
Requires:	mesa-libEGL%{?_isa} >= 18.2.1
Provides:	%{name}-egl
Requires:	%{name} = %{EVRD}

%description -n %{libEGL}
LibEGL wrapper from libglvnd.

%files -n %{libEGL}
%{_libdir}/libEGL.so.1*


#----------------------------------------------------------------------------
%package -n %{libGLdispatch}
Summary:	LibGL dispatcher from libglvnd
Requires:	%{libGL} = %{EVRD}
Provides:	%{name}-GLdispatch
Requires:	%{name} = %{EVRD}

%description -n %{libGLdispatch}
LibGL dispatcher from libglvnd.

%files -n %{libGLdispatch}
%{_libdir}/libGLdispatch.so.0*


#----------------------------------------------------------------------------
%package -n %{libGLESv1}
Summary:	LibGLESv1 wrapper from libglvnd
Requires:	mesa-libEGL%{?_isa} >= 18.2.1
%rename %{_lib}glesv1_1
Provides:	%{name}-GLESv1_CM
Requires:	%{name} = %{EVRD}

%description -n %{libGLESv1}
LibGLESv1 wrapper from libglvnd.

%files -n %{libGLESv1}
%{_libdir}/libGLESv1_CM.so.1*


#----------------------------------------------------------------------------
%package -n %{libGLESv2}
Summary:	LibGLESv2 wrapper from libglvnd
Requires:	mesa-libEGL%{?_isa} >= 18.2.1
%rename %{_lib}glesv2_2
Provides:	%{name}-GLESv2
Requires:	%{name} = %{EVRD}

%description -n %{libGLESv2}
LibGLESv2 wrapper from libglvnd.

%files -n %{libGLESv2}
%{_libdir}/libGLESv2.so.2*


#----------------------------------------------------------------------------
%package -n %{libGL}
Summary:	LibGL wrapper from libglvnd
Requires:	mesa-libGL%{?_isa} >= 18.2.1
%define oldgl %mklibname gl 1
%rename %{oldgl}
Provides:	%{name}-GL
Requires:	%{name} = %{EVRD}

%description -n %{libGL}
LibGL wrapper from libglvnd.

%files -n %{libGL}
%{_libdir}/libGL.so.1*


#----------------------------------------------------------------------------
%package -n %{libGLX}
Summary:	LibGLX wrapper from libglvnd
Requires:	mesa-libGL%{?_isa} >= 18.2.1
Provides:	%{name}-GLX
Requires:	%{name} = %{EVRD}

%description -n %{libGLX}
LibGLX wrapper from libglvnd.

%files -n %{libGLX}
%{_libdir}/libGLX.so.0*


#----------------------------------------------------------------------------
%package -n %{libOpenGL}
Summary:	OpenGL wrapper from libglvnd
Provides:	%{name}-OpenGL
Requires:	%{name} = %{EVRD}

%description -n %{libOpenGL}
OpenGL wrapper from libglvnd.

%files -n %{libOpenGL}
%{_libdir}/libOpenGL.so.0*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{libEGL} = %{EVRD}
Requires:	%{libGLdispatch} = %{EVRD}
Requires:	%{libGLESv1} = %{EVRD}
Requires:	%{libGLESv2} = %{EVRD}
Requires:	%{libGL} = %{EVRD}
Requires:	%{libGLX} = %{EVRD}
Requires:	%{libOpenGL} = %{EVRD}
# Pull in Mesa for OpenGL headers
Requires:	pkgconfig(gl)
# EGL headers include <X11/xlib.h>
Requires:	pkgconfig(x11)

%description -n %{devname}
This package is a bootstrap trick for Mesa, which wants to build against
the libglvnd headers but does not link against any of its libraries (and,
initially, has file conflicts with them).

%files -n %{devname}
%dir %{_includedir}/glvnd
%{_includedir}/glvnd/*.h
%dir %{_includedir}/EGL
%{_includedir}/EGL/*.h
%dir %{_includedir}/GL
%{_includedir}/GL/*.h
%dir %{_includedir}/GLES
%{_includedir}/GLES/*.h
%dir %{_includedir}/GLES2
%{_includedir}/GLES2/*.h
%dir %{_includedir}/GLES3
%{_includedir}/GLES3/*.h
%dir %{_includedir}/KHR
%{_includedir}/KHR/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libEGL.so
%{_libdir}/libGLdispatch.so
%{_libdir}/libGLX.so
%{_libdir}/libGL.so
%{_libdir}/libGLESv1_CM.so
%{_libdir}/libGLESv2.so
%{_libdir}/libOpenGL.so


#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
autoreconf -vif
%configure \
	--disable-static \
	--enable-asm \
	--enable-tls

%make_build

%install
%make_install

# Create directory layout
mkdir -p %{buildroot}%{_sysconfdir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_sysconfdir}/egl/egl_external_platform.d
mkdir -p %{buildroot}%{_datadir}/egl/egl_external_platform.d
