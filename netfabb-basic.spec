Name:           netfabb-basic
%global altname netfabb-free
Version:        7.2.0
Release:        11%{?dist}
Summary:        Freeware suite for STL editing
License:        Redistributable
URL:            http://www.netfabb.com/
# keep both sources in the SRPM
# both files are downloaded from http://www.netfabb.com/downloadcenter.php?basic=1
# and have no public tarball urls
# The Manual directory has been removed as it is not redistributable
# Useful contents from the 5.2.1 version added (man, icons, LICENSE, README)
# The text of the license is the same as if you run netfabb 7.2.0
# (confirmed by mhroncok@redhat.com)
Source0:        %{altname}_%{version}_linux32.tar.gz
Source1:        %{altname}_%{version}_linux64.tar.gz
BuildRequires:  desktop-file-utils
Requires:       lib3ds%{?_isa} = 1.3.0
Provides:       %{altname} = %{version}-%{release}
Provides:       %{altname}%{?_isa} = %{version}-%{release}

ExclusiveArch:  %{ix86} x86_64
%global debug_package %{nil}

%description
netfabb Basic is a free (as in free beer) software for 3D Printing
and the STL file format. Numerous tools allow all steps of the fabrication
process: editing, repairing, positioning, slicing and exporting triangulated
CAD data. For professional use, the author offers commercial support and
additional modules.

%prep

%ifarch %{ix86}
%setup -qTc -a0
%endif

%ifarch x86_64
%setup -qTc -a1
%endif

# Fix a Czech translation bug
sed -i -e 's/Provézt/Provést/g' \
       -e 's/provézt/provést/g' netfabb_free

%build
# nothing to do

%install
# the workflow is copied from install.sh, but we will not run it, as it doesn't respect the buildroot
# there are also several changes to make things more OK

# create directories
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
for res in 16 22 24 32 48 128; do
  mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps
done
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/pixmaps

# binary and libraries
install -pm 0755 netfabb_free %{buildroot}%{_bindir}/%{altname}
ln -s ./%{altname} %{buildroot}%{_bindir}/%{name}
install -pm 0755 *.so.* %{buildroot}%{_libdir}/

# we have this in Fedora
rm %{buildroot}%{_libdir}/lib3ds-netfabb-1.so.3
ln -s lib3ds-1.so.3 %{buildroot}%{_libdir}/lib3ds-netfabb-1.so.3

# desktopfile
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=netfabb Basic
GenericName=STL-Viewer
GenericName[de]=STL-Betrachter
Comment=View and repair STL files
Comment[de]=STL Dateien betrachten und reparieren
Icon=%{name}
TryExec=%{_bindir}/%{name}
Exec=%{_bindir}/%{name} %U
Terminal=false
MimeType=application/netfabb;model/x.stl-binary;model/x.stl-ascii;application/sla;application/x-3ds;model/mesh;image/x-3ds;model/x3d+xml;model/x3d+binary;
Categories=Graphics;3DGraphics;Viewer;
StartupNotify=true
EOF

# man and icons
cp -p man/%{name}.1.gz %{buildroot}%{_mandir}/man1
cp -p man/%{altname}.1.gz %{buildroot}%{_mandir}/man1
cp -p icons/%{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
for res in 16 22 24 32 48 128; do
  cp -p icons/%{name}${res}.png %{buildroot}%{_datadir}/icons/hicolor/${res}x${res}/apps/%{name}.png
done
cp -p icons/%{name}48.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%doc README LICENSE Examples
%{_bindir}/%{altname}
%{_bindir}/%{name}
%{_libdir}/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{altname}.1*
%{_mandir}/man1/%{name}.1*


%changelog
* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 7.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 7.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 7.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 7.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 7.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 7.2.0-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 7.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 7.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 18 2017 Sérgio Basto <sergio@serjux.com> - 7.2.0-3
- Fixup rpm setup macro use -a instead -b

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 7.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 02 2017 Miro Hrončok <mhroncok@redhat.com> - 7.2.0-1
- New version 7.2.0
- Use manpages icons etc. from 5.2.1
- Fix a Czech translation bug
- Add new MIME types model/x.stl-binary and model/x.stl-ascii

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 22 2015 Miro Hrončok <mhroncok@redhat.com> - 5.2.1-1
- New version

* Fri Sep 12 2014 Miro Hrončok <mhroncok@redhat.com> - 5.2.0-2
- Rebuilt

* Fri Sep 12 2014 Miro Hrončok <mhroncok@redhat.com> - 5.2.0-1
- New version

* Fri Jul 11 2014 Miro Hrončok <mhroncok@redhat.com> - 5.1.1-3
- Rebuilt

* Thu Jul 10 2014 Miro Hrončok <mhroncok@redhat.com> - 5.1.1-2
- Use Fedora's lib3ds
- Update desktop database

* Tue Apr 08 2014 Miro Hrončok <mhroncok@redhat.com> - 5.1.1-1
- Updated to 5.1.1

* Wed Mar 19 2014 Miro Hrončok <mhroncok@redhat.com> - 5.1.0-1
- Updated to 5.1.0

* Wed Jan 08 2014 Miro Hrončok <mhroncok@redhat.com> - 5.0.1-2
- Use install to copy files that needs different rights
- Rework icon cache scriptlets

* Tue Dec 31 2013 Miro Hrončok <mhroncok@redhat.com> - 5.0.1-1
- New version

* Tue Mar 26 2013 Miro Hrončok <mhroncok@redhat.com> - 4.9.5-1
- Initial release
