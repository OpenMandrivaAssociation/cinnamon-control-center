%global _internal_version 8475c0d
%global _artwork_version   4.4
%global glib2_version 2.31.0
%global gtk3_version 3.5.13
%global csd_version 2.3.0
%global gnome_desktop_version 3.5.91
%global desktop_file_utils_version 0.9
%global gnome_menus_version 2.11.1
%global libXrandr_version 1.2.99

Summary: Utilities to configure the Cinnamon desktop
Name:    cinnamon-control-center
Version: 2.4.2
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
Source0: cinnamon-control-center-%{version}.tar.gz
#SourceGet0: https://github.com/linuxmint/cinnamon-control-center/archive/%{version}.tar.gz
Source1: http://leigh123linux.fedorapeople.org/pub/cinnamon-control-center-sounds/source/cinnamon-control-center-sounds-1.0.0.tar.xz

#Source0: cinnamon-control-center-%{version}.git%{_internal_version}.tar.gz
##SourceGet0: https://github.com/linuxmint/cinnamon-control-center/tarball/%{_internal_version}

Requires: cinnamon-settings-daemon >= %{csd_version}
Requires: hicolor-icon-theme
Requires: adwaita-icon-theme
Requires: gnome-menus >= %{gnome_menus_version}
Requires: cinnamon-desktop
Requires: cinnamon-translations
Requires: dbus-x11
Obsoletes: %{name}-filesystem <= %{version}-%{release}
# we need XRRGetScreenResourcesCurrent
Requires: libxrandr >= %{libXrandr_version}
# For the user languages
Requires: iso-codes
# For the printers panel
Requires: cups-pk-helper
# For the network panel
Requires: networkmanager-applet
# For the info/details panel
Requires: glxinfo
Requires: xdriinfo

BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(gdk-pixbuf-2.0) >= 2.23.0
BuildRequires: pkgconfig(librsvg-2.0)
BuildRequires: pkgconfig(cinnamon-desktop)
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xrandr) >= %{libXrandr_version}
BuildRequires: pkgconfig(libgnome-menu-3.0) >= %{gnome_menus_version}
BuildRequires: cinnamon-menus-devel
BuildRequires: cinnamon-settings-daemon-devel >= %{csd_version}
BuildRequires: intltool >= 0.37.1
BuildRequires: pkgconfig(xxf86misc)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(xscrnsaver)
BuildRequires: gnome-doc-utils
BuildRequires: pkgconfig(libglade-2.0)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(dbus-1) >= 0.90
BuildRequires: pkgconfig(dbus-glib-1) >= 0.70
BuildRequires: chrpath
BuildRequires: pkgconfig(libpulse) >= 2.0
BuildRequires: pkgconfig(libpulse-mainloop-glib) >= 2.0
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(upower-glib)
BuildRequires: pkgconfig(libnm-glib) >= 0.9
BuildRequires: pkgconfig(libnm-gtk) >= 0.9
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: gnome-common
BuildRequires: cups-devel
BuildRequires: pkgconfig(libgtop-2.0)
BuildRequires: pkgconfig(iso-codes)
BuildRequires: pkgconfig(cheese-gtk) >= 2.91.91.1
BuildRequires: pkgconfig(clutter-gst-2.0)
BuildRequires: pkgconfig(clutter-gtk-1.0)
BuildRequires: pkgconfig(goa-1.0)
BuildRequires: pkgconfig(colord)
BuildRequires: pkgconfig(libnotify)
BuildRequires: gnome-doc-utils
BuildRequires: pkgconfig(systemd)
BuildRequires: pkgconfig(pwquality)
BuildRequires: pkgconfig(ibus-1.0)
BuildRequires: pkgconfig(libgnomekbd)
BuildRequires: pkgconfig(libxklavier)
BuildRequires: pkgconfig(gnome-bluetooth-1.0) >= 2.91
BuildRequires: pkgconfig(libnm-glib-vpn)
BuildRequires: libwacom-devel

%description
This package contains configuration utilities for the Cinnamon desktop, which
allow to configure accessibility options, desktop fonts, keyboard and mouse
properties, sound setup, desktop theme and background, user interface
properties, screen resolution, and other settings.

%package devel
Summary: Development package for %{name}
Group: Development/C
Requires: %{name} = %{version}-%{release}

%description devel
Header files and libraries for developing Muffin plugins. Also includes
utilities for testing Metacity/Muffin themes.


%prep
%setup -q
tar -xJf %{SOURCE1}
chmod +x autogen.sh
NOCONFIGURE=1 ./autogen.sh

%build
%configure2_5x \
        --disable-static \
        --disable-update-mimedb \
        --with-libsocialweb=no \
        --enable-systemd \
        --enable-ibus \
        --enable-bluetooth

sed -i ./panels/common/gdm-languages.c \
   -e "s!/usr/lib/!/usr/share/!g"

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

%make V=1

%install
%makeinstall_std

desktop-file-edit                                       \
  --set-icon=cinnamon-preferences-color                 \
  $RPM_BUILD_ROOT%{_datadir}/applications/cinnamon-color-panel.desktop
desktop-file-install                                    \
  --delete-original                                     \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications         \
  $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# remove useless libtool archive files
find $RPM_BUILD_ROOT -name '*.la' -delete

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/cinnamon-control-center-1/panels/*.so
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/cinnamon-control-center

# install sound files
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/cinnamon-control-center/sounds/
install -pm 0644 sounds/* $RPM_BUILD_ROOT/%{_datadir}/cinnamon-control-center/sounds/

%find_lang %{name}-timezones

%files -f %{name}-timezones.lang
%doc AUTHORS COPYING README
%{_datadir}/cinnamon-control-center/ui/
%{_datadir}/cinnamon-control-center/sounds/*.oga
%{_datadir}/applications/*.desktop
%{_datadir}/desktop-directories/*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/cinnamon-control-center/icons/
%{_datadir}/cinnamon-control-center/datetime/
# list all binaries explicitly, so we notice if one goes missing
%{_bindir}/cinnamon-control-center
%{_bindir}/cinnamon-sound-applet
%config %{_sysconfdir}/xdg/autostart/cinnamon-sound-applet.desktop
%config %{_sysconfdir}/xdg/menus/cinnamoncc.menu
%{_libdir}/libcinnamon-control-center.so.1*
%dir %{_libdir}/cinnamon-control-center-1/
%{_libdir}/cinnamon-control-center-1/panels/libcolor.so
%{_libdir}/cinnamon-control-center-1/panels/libdate_time.so
%{_libdir}/cinnamon-control-center-1/panels/libdisplay.so
%{_libdir}/cinnamon-control-center-1/panels/libpower.so
%{_libdir}/cinnamon-control-center-1/panels/libregion.so
%{_libdir}/cinnamon-control-center-1/panels/libscreen.so
%{_libdir}/cinnamon-control-center-1/panels/libsoundnua.so
%{_libdir}/cinnamon-control-center-1/panels/libuniversal-access.so
%{_libdir}/cinnamon-control-center-1/panels/libwacom-properties.so

%{_datadir}/polkit-1/rules.d/cinnamon-control-center.rules

%files devel
%{_includedir}/cinnamon-control-center-1/
%{_libdir}/libcinnamon-control-center.so
%{_libdir}/pkgconfig/libcinnamon-control-center.pc

