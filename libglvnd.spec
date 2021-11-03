%global __provides_exclude_from %{_libdir}/%{name}
%global __requires_exclude_from %{_libdir}/%{name}

%global optflags %{optflags} -O3 -Wstrict-aliasing=0

%define major 0
%define devname %mklibname glvnd -d

%define libEGL %mklibname EGL 1
%define libGLdispatch %mklibname GLdispatch 0
%define libGLESv1 %mklibname GLESv1_CM 1
%define libGLESv2 %mklibname GLESv2 2
%define libGL %mklibname GL 1
%define libGLX %mklibname GLX 0
%define libOpenGL %mklibname OpenGL 0

# libglvnd is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%define lib32EGL libEGL1
%define lib32GLdispatch libGLdispatch0
%define lib32GLESv1 libGLESv1_CM1
%define lib32GLESv2 libGLESv2_2
%define lib32GL libGL1
%define lib32GLX libGLX0
%define lib32OpenGL libOpenGL0
%define dev32name libglvnd-devel

Summary:	The GL Vendor-Neutral Dispatch library
Name:		libglvnd
Version:	1.3.4
Release:	2
License:	MIT
Group:		System/Libraries
Url:		https://gitlab.freedesktop.org/glvnd/libglvnd
Source0:	https://gitlab.freedesktop.org/glvnd/libglvnd/-/archive/v%{version}/%{name}-v%{version}.tar.bz2
BuildRequires:	meson
BuildRequires:	python-libxml2
BuildRequires:	pkgconfig(glproto)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xdmcp)
%if %{with compat32}
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXext)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
%endif

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
Requires:	(mesa-libEGL%{?_isa} >= 18.2.1 or mesa-libEGL >= 18.2.1)
Provides:	%{name}-egl%{?_isa} = %{EVRD}
Provides:	%{name}-egl = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n %{libEGL}
LibEGL wrapper from libglvnd.

%files -n %{libEGL}
%{_libdir}/libEGL.so.1*

#----------------------------------------------------------------------------
%package -n %{libGLdispatch}
Summary:	LibGL dispatcher from libglvnd
Requires:	%{libGL} = %{EVRD}
Provides:	%{name}-GLdispatch%{?_isa} = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n %{libGLdispatch}
LibGL dispatcher from libglvnd.

%files -n %{libGLdispatch}
%{_libdir}/libGLdispatch.so.0*

#----------------------------------------------------------------------------
%package -n %{libGLESv1}
Summary:	LibGLESv1 wrapper from libglvnd
Requires:	(mesa-libEGL%{?_isa} >= 18.2.1 or mesa-libEGL >= 18.2.1)
%rename %{_lib}glesv1_1
Provides:	%{name}-GLESv1_CM%{?_isa} = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n %{libGLESv1}
LibGLESv1 wrapper from libglvnd.

%files -n %{libGLESv1}
%{_libdir}/libGLESv1_CM.so.1*

#----------------------------------------------------------------------------
%package -n %{libGLESv2}
Summary:	LibGLESv2 wrapper from libglvnd
Requires:	(mesa-libEGL%{?_isa} >= 18.2.1 or mesa-libEGL >= 18.2.1)
%rename %{_lib}glesv2_2
Provides:	%{name}-GLESv2%{?_isa} = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n %{libGLESv2}
LibGLESv2 wrapper from libglvnd.

%files -n %{libGLESv2}
%{_libdir}/libGLESv2.so.2*

#----------------------------------------------------------------------------
%package -n %{libGL}
Summary:	LibGL wrapper from libglvnd
Requires:	(mesa-libGL%{?_isa} >= 18.2.1 or mesa-libGL >= 18.2.1)
%define oldgl %mklibname gl 1
%rename %{oldgl}
Provides:	%{name}-GL%{?_isa} = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n %{libGL}
LibGL wrapper from libglvnd.

%files -n %{libGL}
%{_libdir}/libGL.so.1*

#----------------------------------------------------------------------------
%package -n %{libGLX}
Summary:	LibGLX wrapper from libglvnd
Requires:	(mesa-libGL%{?_isa} >= 18.2.1 or mesa-libGL >= 18.2.1)
Provides:	%{name}-GLX%{?_isa} = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n %{libGLX}
LibGLX wrapper from libglvnd.

%files -n %{libGLX}
%{_libdir}/libGLX.so.0*

#----------------------------------------------------------------------------
%package -n %{libOpenGL}
Summary:	OpenGL wrapper from libglvnd
Provides:	%{name}-OpenGL%{?_isa} = %{EVRD}
Provides:	%{name}-GL = %{EVRD}
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

%if %{with compat32}
#----------------------------------------------------------------------------
%package -n %{lib32EGL}
Summary:	LibEGL wrapper from libglvnd (32-bit)
Requires:	%{name} = %{EVRD}

%description -n %{lib32EGL}
LibEGL wrapper from libglvnd.

%files -n %{lib32EGL}
%{_prefix}/lib/libEGL.so.1*

#----------------------------------------------------------------------------
%package -n %{lib32GLdispatch}
Summary:	LibGL dispatcher from libglvnd (32-bit)
Requires:	%{lib32GL} = %{EVRD}

%description -n %{lib32GLdispatch}
LibGL dispatcher from libglvnd.

%files -n %{lib32GLdispatch}
%{_prefix}/lib/libGLdispatch.so.0*

#----------------------------------------------------------------------------
%package -n %{lib32GLESv1}
Summary:	LibGLESv1 wrapper from libglvnd (32-bit)
Requires:	%{name} = %{EVRD}

%description -n %{lib32GLESv1}
LibGLESv1 wrapper from libglvnd.

%files -n %{lib32GLESv1}
%{_prefix}/lib/libGLESv1_CM.so.1*

#----------------------------------------------------------------------------
%package -n %{lib32GLESv2}
Summary:	LibGLESv2 wrapper from libglvnd (32-bit)
Requires:	%{name} = %{EVRD}

%description -n %{lib32GLESv2}
LibGLESv2 wrapper from libglvnd.

%files -n %{lib32GLESv2}
%{_prefix}/lib/libGLESv2.so.2*

#----------------------------------------------------------------------------
%package -n %{lib32GL}
Summary:	LibGL wrapper from libglvnd (32-bit)
Requires:	%{name} = %{EVRD}

%description -n %{lib32GL}
LibGL wrapper from libglvnd.

%files -n %{lib32GL}
%{_prefix}/lib/libGL.so.1*

#----------------------------------------------------------------------------
%package -n %{lib32GLX}
Summary:	LibGLX wrapper from libglvnd (32-bit)
Requires:	%{name} = %{EVRD}

%description -n %{lib32GLX}
LibGLX wrapper from libglvnd.

%files -n %{lib32GLX}
%{_prefix}/lib/libGLX.so.0*

#----------------------------------------------------------------------------
%package -n %{lib32OpenGL}
Summary:	OpenGL wrapper from libglvnd (32-bit)
Requires:	%{name} = %{EVRD}

%description -n %{lib32OpenGL}
OpenGL wrapper from libglvnd.

%files -n %{lib32OpenGL}
%{_prefix}/lib/libOpenGL.so.0*

#----------------------------------------------------------------------------

%package -n %{dev32name}
Summary:	Development files for %{name} (32-bit)
Group:		Development/C
Requires:	%{name} = %{EVRD}
Requires:	%{lib32EGL} = %{EVRD}
Requires:	%{lib32GLdispatch} = %{EVRD}
Requires:	%{lib32GLESv1} = %{EVRD}
Requires:	%{lib32GLESv2} = %{EVRD}
Requires:	%{lib32GL} = %{EVRD}
Requires:	%{lib32GLX} = %{EVRD}
Requires:	%{lib32OpenGL} = %{EVRD}
Requires:	%{devname} = %{EVRD}
# Pull in Mesa for OpenGL headers
Requires:	pkgconfig(gl)
# EGL headers include <X11/xlib.h>
Requires:	devel(libX11)

%description -n %{dev32name}
This package is a bootstrap trick for Mesa, which wants to build against
the libglvnd headers but does not link against any of its libraries (and,
initially, has file conflicts with them).

%files -n %{dev32name}
%{_prefix}/lib/pkgconfig/*.pc
%{_prefix}/lib/libEGL.so
%{_prefix}/lib/libGLdispatch.so
%{_prefix}/lib/libGLX.so
%{_prefix}/lib/libGL.so
%{_prefix}/lib/libGLESv1_CM.so
%{_prefix}/lib/libGLESv2.so
%{_prefix}/lib/libOpenGL.so
%endif

%prep
%autosetup -p1 -n %{name}-v%{version}

%if %{with compat32}
%meson32 \
	-Dasm=disabled \
	-Dx11=enabled \
	-Dglx=enabled \
	-Dtls=enabled
%endif

%meson \
%ifnarch %{riscv}
	-Dasm=enabled \
%else
	-Dasm=disabled \
%endif
	-Dx11=enabled \
	-Dglx=enabled \
	-Dtls=enabled

%build
%if %{with compat32}
%ninja_build -C build32
%endif
%meson_build

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%meson_install

# Create directory layout
mkdir -p %{buildroot}%{_sysconfdir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_sysconfdir}/egl/egl_external_platform.d
mkdir -p %{buildroot}%{_datadir}/egl/egl_external_platform.d
