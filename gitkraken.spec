%global privlibs libffmpeg|libnode
%global __requires_exclude ^(%{privlibs})\\.so
%global __provides_exclude_from .*\\.so
%global debug_package %{nil}

Name: gitkraken
Version: 3.3.2
Release: 1%{?dist}

Summary: Git GUI client
URL: https://www.gitkraken.com/
License: Proprietary
ExclusiveArch: x86_64

Source0: https://release.gitkraken.com/linux/gitkraken-amd64.tar.gz#/%{name}-%{version}.tar.gz
Source1: %{name}.png
Source2: %{name}.desktop

BuildRequires: desktop-file-utils
BuildRequires: %{_bindir}/convert

Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Requires: libgnome-keyring%{?_isa}
Requires: hicolor-icon-theme
Requires: git%{?_isa}

%description
GitKraken - The legendary Git GUI client for Windows, Mac and Linux.

%prep
%autosetup -n %{name}

%build
# Do nothing...

%install
# Creating general directories...
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications/
mkdir -p %{buildroot}/opt/%{name}/

# Creating ghost file for alternatives system...
touch %{buildroot}%{_bindir}/%{name}

# Installing to working directory from official package...
cp -r %_builddir/%{name} %{buildroot}/opt

# Removing some already installed files...
rm -f %{buildroot}/opt/%{name}/LICENSE*

# Installing icons...
for size in 16 32 48 64 128 256 512; do
    dir="%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps"
    mkdir -p $dir
    convert -resize ${size}x${size} %{SOURCE1} "$dir/%{name}.png"
done

# Marking as executable...
chmod +x %{buildroot}/opt/%{name}/%{name}

# Creating desktop icon...
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE2}

%post
%{_sbindir}/update-alternatives --install %{_bindir}/%{name} %{name} /opt/%{name}/%{name} 10

%postun
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{name} /opt/%{name}/%{name}
fi

%files
%license LICENS*
/opt/%{name}
%ghost %{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Thu Dec 14 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 3.3.2-1
- Updated to version 3.3.2.

* Wed Nov 29 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 3.3.0-1
- Updated to version 3.3.0.

* Sun Nov 19 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 3.2.2-1
- Updated to version 3.2.2.

* Wed Nov 01 2017 Vitaly Zaitsev <vitaly@easycoding.org> - 3.2.1-1
- Initial SPEC release.
