%global glib2_version 2.31.0
%global gtk3_version 3.5.13
%global csd_version 2.3.0
%global gnome_desktop_version 3.5.91
%global desktop_file_utils_version 0.9
%global gnome_menus_version 2.11.1
%global libXrandr_version 1.2.99

%define major 1
%define libname %mklibname cinnamon-control-center %major

Summary: Utilities to configure the Cinnamon desktop
Name:    cinnamon-control-center
Version: 5.6.1
Release: 1
# The following files contain code from
# ISC for panels/network/rfkill.h
# And MIT for wacom/calibrator/calibrator.c
# wacom/calibrator/calibrator.h
# wacom/calibrator/gui_gtk.c
# wacom/calibrator/gui_gtk.h
# wacom/calibrator/main.c
Group:  Graphical desktop/Cinnamon
License: GPLv2+ and LGPLv2+ and MIT and ISC
URL:     http://cinnamon.linuxmint.com
Source0: https://github.com/linuxmint/cinnamon-control-center/archive/%{version}/%{name}-%{version}.tar.gz

Requires: cinnamon-settings-daemon >= %{csd_version}
Requires: hicolor-icon-theme
Requires: adwaita-icon-theme
Requires: gnome-menus >= %{gnome_menus_version}
Requires: cinnamon-desktop
Requires: cinnamon-translations
Requires: dbus-x11
Obsoletes: %{name}-filesystem <= %{version}-%{release}
# we need XRRGetScreenResourcesCurrent
#Requires: libxrandr >= %{libXrandr_version}
# For the user languages
Requires: iso-codes
# For the printers panel
#Requires: cups-pk-helper
# For the network panel
Requires: networkmanager-applet
# For the info/details panel
Requires: glxinfo
Requires: xdriinfo
Requires: gnome-color-manager

BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(cinnamon-desktop)
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: pkgconfig(libcinnamon-menu-3.0)
BuildRequires: intltool >= 0.37.1
BuildRequires: pkgconfig(xkbfile)
BuildRequires: gnome-doc-utils
BuildRequires: chrpath
BuildRequires: pkgconfig(upower-glib)
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: pkgconfig(mm-glib)
BuildRequires: pkgconfig(iso-codes)
BuildRequires: pkgconfig(goa-1.0)
BuildRequires: pkgconfig(colord)
BuildRequires: pkgconfig(libnotify)
BuildRequires: gnome-doc-utils
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(libgnomekbd)
BuildRequires: pkgconfig(libxklavier)
BuildRequires: pkgconfig(libnm) 
BuildRequires: pkgconfig(libnma)
BuildRequires: pkgconfig(libwacom)
BuildRequires: pkgconfig(mm-glib) >= 0.7
BuildRequires: pkgconfig(x11)
BuildRequires: tzdata
BuildRequires: meson

%description
This package contains configuration utilities for the Cinnamon desktop, which
allow to configure accessibility options, desktop fonts, keyboard and mouse
properties, sound setup, desktop theme and background, user interface
properties, screen resolution, and other settings.

%package -n %libname
Summary: The cinnamon control center library, a part of %{name}
Group: System/Libraries

%description -n %libname
The cinnamon control center library, a part of %{name}

%package devel
Summary: Development package for %{name}
Group: Development/C
Requires: %{name} = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}

%description devel
Header files and libraries for developing Muffin plugins. Also includes
utilities for testing Metacity/Muffin themes.


%prep
%setup -q

%build
%meson

%meson_build

%install
%meson_install

#desktop-file-edit                                       \
#  --set-icon=cinnamon-preferences-color                 \
#  $RPM_BUILD_ROOT%{_datadir}/applications/cinnamon-color-panel.desktop
#desktop-file-install                                    \
#  --delete-original                                     \
#  --dir $RPM_BUILD_ROOT%{_datadir}/applications         \
#  $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# remove useless libtool archive files
find $RPM_BUILD_ROOT -name '*.la' -delete

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/cinnamon-control-center-1/panels/*.so
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cinnamon-control-center


#find_lang %{name}-timezones

%files
%doc AUTHORS COPYING README
%{_datadir}/cinnamon-control-center/ui/
%{_datadir}/applications/*.desktop
%{_datadir}/cinnamon-control-center/panels/
%{_datadir}/icons/hicolor/*/*/*
# list all binaries explicitly, so we notice if one goes missing
%{_bindir}/cinnamon-control-center
#config #{_sysconfdir}/xdg/menus/cinnamoncc.menu
%dir %{_libdir}/cinnamon-control-center-1/
%dir %{_libdir}/cinnamon-control-center-1/panels
%{_libdir}/cinnamon-control-center-1/panels/libcolor.so
#{_libdir}/cinnamon-control-center-1/panels/libdate_time.so
%{_libdir}/cinnamon-control-center-1/panels/libdisplay.so
%{_libdir}/cinnamon-control-center-1/panels/libnetwork.so
%{_libdir}/cinnamon-control-center-1/panels/libregion.so
%{_libdir}/cinnamon-control-center-1/panels/libwacom-properties.so
%{_libdir}/cinnamon-control-center-1/panels/libonline-accounts.so
%{_datadir}/glib-2.0/schemas/org.cinnamon.control-center.display.gschema.xml

#{_datadir}/polkit-1/rules.d/cinnamon-control-center.rules
#{_datadir}/polkit-1/actions/org.cinnamon.controlcenter.datetime.policy

%files -n %libname
%{_libdir}/libcinnamon-control-center.so.%{major}*

%files devel
%{_includedir}/cinnamon-control-center-1/
%{_libdir}/libcinnamon-control-center.so
%{_libdir}/pkgconfig/libcinnamon-control-center.pc

