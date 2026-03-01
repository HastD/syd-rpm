# SPDX-FileCopyrightText: 2026 Daniel Hast
#
# SPDX-License-Identifier: GPL-3.0-only

%bcond check 0

%global with_selinux 1
%global modulename syd
%global selinuxtype targeted

%global __brp_mangle_shebangs %{nil}

Name:           syd
Version:        3.50.0
Release:        %autorelease
Summary:        Rock-solid application kernel

License:        %{shrink:
    ((MIT OR Apache-2.0) AND Unicode-3.0) AND
    (0BSD) AND
    (0BSD OR MIT OR Apache-2.0) AND
    (Apache-2.0) AND
    (Apache-2.0 OR BSL-1.0) AND
    (Apache-2.0 OR MIT) AND
    (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND
    (BSD-2-Clause) AND
    (BSD-2-Clause OR Apache-2.0 OR MIT) AND
    (BSD-3-Clause) AND
    (CC0-1.0) AND
    (GPL-3.0-only) AND
    (GPL-3.0-or-later) AND
    (ISC) AND
    (MIT) AND
    (MIT OR Apache-2.0) AND
    (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND
    (MIT OR Apache-2.0 OR Zlib) AND
    (MIT OR Zlib OR Apache-2.0) AND
    (MPL-2.0) AND
    (MPL-2.0 OR LGPL-3.0-or-later) AND
    (Unlicense OR MIT) AND
    (WTFPL) AND
    (Zlib) AND
    (Zlib OR Apache-2.0 OR MIT)
}
# LICENSE.dependencies contains a full license breakdown
URL:            https://gitlab.exherbo.org/sydbox/sydbox
Source:         syd-%{version}.tar.xz
Source:         syd-%{version}-vendor.tar.xz
Source:         syd-selinux-%{version}.tar.xz

BuildRequires:  cargo-rpm-macros >= 26
BuildRequires:  libseccomp-devel

%if 0%{?with_selinux}
BuildRequires:  container-selinux
BuildRequires:  make
BuildRequires:  selinux-policy-devel
Requires:       (%{name}-selinux if selinux-policy-%{selinuxtype})
%endif

%global _description Syd is a rock-solid application kernel to sandbox applications on Linux.

%description
%{_description}

%prep
%autosetup -p1 -a1
%cargo_prep -v vendor
%setup -q -T -D -a2

%build
%cargo_build -f oci -- --workspace
%{cargo_license_summary -f oci}
%{cargo_license -f oci} > LICENSE.dependencies
%{cargo_vendor_manifest}

%if 0%{?with_selinux}
make -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 %{modulename}.pp
%endif

%install
install -Dp -m 0755 -t %{buildroot}%{_bindir} target/rpm/syd* target/rpm/pandora
rm -f %{buildroot}%{_bindir}/syd*.d

%if 0%{?with_selinux}
install -Dp -m 0644 -t %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype} %{modulename}.pp.bz2
install -Dp -m 0644 -t %{buildroot}%{_datadir}/selinux/devel/include/distributed selinux/%{modulename}.if
%endif

%if %{with check}
%check
%cargo_test -f oci -- --workspace
%endif

%files
%license COPYING
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc ChangeLog.md
%doc README.md
%{_bindir}/syd
%{_bindir}/syd-aes
%{_bindir}/syd-asm
%{_bindir}/syd-aux
%{_bindir}/syd-bit
%{_bindir}/syd-cap
%{_bindir}/syd-cat
%{_bindir}/syd-cpu
%{_bindir}/syd-dns
%{_bindir}/syd-elf
%{_bindir}/syd-emacs
%{_bindir}/syd-env
%{_bindir}/syd-exec
%{_bindir}/syd-fd
%{_bindir}/syd-fork
%{_bindir}/syd-fs
%{_bindir}/syd-hex
%{_bindir}/syd-info
%{_bindir}/syd-key
%{_bindir}/syd-ldd
%{_bindir}/syd-lock
%{_bindir}/syd-ls
%{_bindir}/syd-mdwe
%{_bindir}/syd-mem
%{_bindir}/syd-net
%{_bindir}/syd-oci
%{_bindir}/syd-ofd
%{_bindir}/syd-path
%{_bindir}/syd-pause
%{_bindir}/syd-pds
%{_bindir}/syd-poc
%{_bindir}/syd-pty
%{_bindir}/syd-read
%{_bindir}/syd-rnd
%{_bindir}/syd-run
%{_bindir}/syd-sec
%{_bindir}/syd-sh
%{_bindir}/syd-sha
%{_bindir}/syd-size
%{_bindir}/syd-stat
%{_bindir}/syd-sys
%{_bindir}/syd-tck
%{_bindir}/syd-test
%{_bindir}/syd-test-do
%{_bindir}/syd-tor
%{_bindir}/syd-tsc
%{_bindir}/syd-tty
%{_bindir}/syd-utc
%{_bindir}/syd-uts
%{_bindir}/syd-x

%package tui
Summary: Syd's Terminal User Interface
Requires: %{name}

%description tui
Syd's Terminal User Interface. %{_description}

%files tui
%{_bindir}/syd-tui

%package pandora
Summary: Syd's log inspector & profile writer
Requires: %{name}

%description pandora
pandora: Syd's log inspector & profile writer. %{_description}

%files pandora
%{_bindir}/pandora

%if 0%{?with_selinux}
%package selinux
Summary:        SELinux policies for syd
URL:            https://github.com/HastD/syd-rpm/
License:        GPL-3.0-only

Requires:       %{name}
Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildArch:      noarch
%{?selinux_requires_min}

%description selinux
SELinux policy modules for syd. %{_description}

%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%postun selinux
if [ "$1" -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
    %selinux_relabel_post -s %{selinuxtype}
fi

%posttrans selinux
%selinux_relabel_post -s %{selinuxtype}

%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%{_datadir}/selinux/devel/include/distributed/%{modulename}.if
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

# if with_selinux
%endif

%changelog
%autochangelog
