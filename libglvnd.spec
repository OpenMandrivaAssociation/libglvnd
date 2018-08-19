%global __provides_exclude_from %{_libdir}/%{name}
%global __requires_exclude_from %{_libdir}/%{name}

%define _disable_ld_as_needed 1

%define major 0
%define libgldispatch %mklibname gldispatch %{major}
%define libopengl %mklibname opengl %{major}
%define devname %mklibname glvnd -d

# Don't apply library packaging policy here as we don't link with these libraries
%define libname_egl %mklibname glvnd-egl
%define libname_gles %mklibname glvnd-gles
%define libname_glx %mklibname glvnd-glx

Summary:	The GL Vendor-Neutral Dispatch library
Name:		libglvnd
Version:	1.1.0
Release:	1
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

%package -n %{libgldispatch}
Summary:	Main shared library for libglvnd
Group:		System/Libraries
Requires:	%{name}

%description -n %{libgldispatch}
Main shared library for libglvnd.

%files -n %{libgldispatch}
%{_libdir}/libGLdispatch.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libopengl}
Summary:	OpenGL support for libglvnd
Group:		System/Libraries
Requires:	%{name}

%description -n %{libopengl}
libOpenGL is the common dispatch interface for the workstation OpenGL API.

%files -n %{libopengl}
%{_libdir}/libOpenGL.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libname_egl}
Summary:	EGL support for libglvnd
Group:		System/Libraries
Requires:	%{name}
Provides:	glvnd-egl = %{EVRD}

%description -n %{libname_egl}
libEGL are the common dispatch interface for the EGL API.

%files -n %{libname_egl}
%{_libdir}/%{name}/libEGL.so.1*

#----------------------------------------------------------------------------

%package -n %{libname_gles}
Summary:	GLES support for libglvnd
Group:		System/Libraries
Requires:	%{name}
Provides:	glvnd-gles = %{EVRD}

%description -n %{libname_gles}
libGLES are the common dispatch interface for the GLES API.

%files -n %{libname_gles}
%{_libdir}/%{name}/libGLESv1_CM.so.1*
%{_libdir}/%{name}/libGLESv2.so.2*

#----------------------------------------------------------------------------

%package -n %{libname_glx}
Summary:	GLX support for libglvnd
Group:		System/Libraries
Requires:	%{name}
Provides:	glvnd-glx = %{EVRD}

%description -n %{libname_glx}
libGL and libGLX are the common dispatch interface for the GLX API.

%files -n %{libname_glx}
%{_libdir}/%{name}/libGL.so.1*
%{_libdir}/%{name}/libGLX.so.0*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C

%description -n %{devname}
This package is a bootstrap trick for Mesa, which wants to build against
the libglvnd headers but does not link against any of its libraries (and,
initially, has file conflicts with them).

%files -n %{devname}
%dir %{_includedir}/glvnd
%{_includedir}/glvnd/*.h
%{_libdir}/pkgconfig/*.pc

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

# Kill development symlinks, we use Mesa instead
rm -rf %{buildroot}%{_libdir}/*.so

# Avoid conflict with mesa-libGL
mkdir -p %{buildroot}%{_libdir}/%{name}
for l in libEGL libGL libGLX libGLESv1_CM libGLESv2 ; do
  mv %{buildroot}%{_libdir}/${l}.so* \
    %{buildroot}%{_libdir}/%{name}
done

# Create directory layout
mkdir -p %{buildroot}%{_sysconfdir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d
mkdir -p %{buildroot}%{_sysconfdir}/egl/egl_external_platform.d
mkdir -p %{buildroot}%{_datadir}/egl/egl_external_platform.d
