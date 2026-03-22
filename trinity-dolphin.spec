%bcond clang 1

# TDE variables
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif

%define tde_pkg dolphin
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Version:		0.9.2
Release:		%{?tde_version:%{tde_version}_}4
Summary:		File manager for TDE focusing on usability
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/system/%{tarball_name}-%{tde_version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:  tqt3-dev-tools

BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	libtool

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
Dolphin focuses on being only a file manager.
This approach allows to optimize the user
interface for the task of file management.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
# Makes 'media_safelyremove.desktop' an alternative
%__mv -f %{buildroot}%{tde_prefix}/share/apps/d3lphin/servicemenus/media_safelyremove.desktop %{buildroot}%{tde_prefix}/share/apps/d3lphin/servicemenus/media_safelyremove.desktop_d3lphin

# Locales
%find_lang d3lphin


%post
update-alternatives --install \
  %{tde_prefix}/share/apps/d3lphin/servicemenus/media_safelyremove.desktop \
  media_safelyremove.desktop_d3lphin \
  %{tde_prefix}/share/apps/d3lphin/servicemenus/media_safelyremove.desktop_d3lphin \
  15

%preun
if [ $1 -eq 0 ]; then
  update-alternatives --remove \
    media_safelyremove.desktop_d3lphin \
    %{tde_prefix}/share/apps/d3lphin/servicemenus/media_safelyremove.desktop_d3lphin || :
fi


%files -f d3lphin.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING TODO
%{tde_prefix}/bin/d3lphin
%{tde_prefix}/share/applications/tde/d3lphin.desktop
%{tde_prefix}/share/apps/d3lphin/
%{tde_prefix}/share/icons/hicolor/*/apps/d3lphin.png
%{tde_prefix}/share/man/man1/*.1*
%lang(en) %{tde_prefix}/share/doc/tde/HTML/en/d3lphin/

