# SPDX-FileCopyrightText: 2026 Daniel Hast
#
# SPDX-License-Identifier: GPL-3.0-only

%bcond check 1

%global with_selinux 1
%global modulename syd
%global selinuxtype targeted

%global __brp_mangle_shebangs %{nil}

Name:           syd
Version:        3.51.2
Release:        3
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
BuildRequires:  scdoc

%if 0%{?with_selinux}
BuildRequires:  container-selinux
BuildRequires:  make
BuildRequires:  selinux-policy-devel
Recommends:     (%{name}-selinux if selinux-policy-%{selinuxtype})
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

for file in man/*.scd; do
    scdoc < "$file" > "${file%%.scd}"
done

%if 0%{?with_selinux}
make -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 %{modulename}.pp
%endif

%install
%global syd_programs %{shrink:
syd
syd-aes
syd-asm
syd-aux
syd-bit
syd-cap
syd-cat
syd-cpu
syd-dns
syd-elf
syd-emacs
syd-env
syd-exec
syd-fd
syd-fork
syd-fs
syd-hex
syd-info
syd-key
syd-ldd
syd-lock
syd-ls
syd-mdwe
syd-mem
syd-net
syd-oci
syd-ofd
syd-path
syd-pause
syd-pds
syd-poc
syd-pty
syd-read
syd-rnd
syd-run
syd-sec
syd-sh
syd-size
syd-stat
syd-sum
syd-sys
syd-tck
syd-test
syd-test-do
syd-tor
syd-tsc
syd-tty
syd-utc
syd-uts
syd-x
}

for syd_program in %{syd_programs}; do
    echo "%%{_bindir}/${syd_program}"
done >> syd-rpm-files.txt

for manpage in man/syd*.[1-8]; do
    echo "%%{_mandir}/man${manpage##*.}/${manpage##*/}*"
done >> syd-rpm-files.txt

install -Dp -m 0755 -t %{buildroot}%{_bindir} target/rpm/syd* target/rpm/pandora
rm -f %{buildroot}%{_bindir}/syd*.d

install -Dp -m 0644 -t %{buildroot}%{_mandir}/man1 man/syd*.1
install -Dp -m 0644 -t %{buildroot}%{_mandir}/man2 man/syd.2
install -Dp -m 0644 -t %{buildroot}%{_mandir}/man5 man/syd.5
install -Dp -m 0644 -t %{buildroot}%{_mandir}/man7 man/syd*.7

install -Dp -m 0644 -t %{buildroot}%{_datadir}/vim/vimfiles/ftdetect vim/ftdetect/syd.vim
install -Dp -m 0644 -t %{buildroot}%{_datadir}/vim/vimfiles/syntax vim/syntax/syd-3.vim

install -Dp -t %{buildroot}%{_libdir} target/rpm/libsyd.so target/rpm/libsyd.a
install -Dp -m 0644 -t %{buildroot}%{_includedir} lib/syd.h
install -Dp -m 0755 -t %{buildroot}%{perl_vendorlib} lib/src/syd.pm
install -Dp -m 0755 -t %{buildroot}%{python3_sitelib} lib/src/syd.py

%if 0%{?with_selinux}
install -Dp -m 0644 -t %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype} %{modulename}.pp.bz2
install -Dp -m 0644 -t %{buildroot}%{_datadir}/selinux/devel/include/distributed selinux/%{modulename}.if
%endif

%if %{with check}
%check
%cargo_test -f oci -- --workspace
%endif

%files -f syd-rpm-files.txt
%license COPYING
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc ChangeLog.md
%doc README.md
%{_datadir}/vim/vimfiles/ftdetect/syd.vim
%{_datadir}/vim/vimfiles/syntax/syd-3.vim

%package -n libsyd
Summary: Rust-based C library for syd interaction via /dev/syd
License: LGPL-3.0-only
Requires: %{name} = %{version}-%{release}

%description -n libsyd
Rust-based C library for syd interaction via /dev/syd. Includes Python and Perl bindings. %{_description}

%files -n libsyd
%attr(0755, -, -) %{_libdir}/libsyd.so
%attr(0755, -, -) %{perl_vendorlib}/syd.pm
%pycached %{python3_sitelib}/syd.py

%package -n libsyd-devel
Summary: Development files for libsyd
License: LGPL-3.0-only
BuildRequires: perl-generators
BuildRequires: python3-devel
Requires: libsyd = %{version}-%{release}

%description -n libsyd-devel
This package contains the C header files for libsyd. %{_description}

%files -n libsyd-devel
%attr(0644, -, -) %{_includedir}/syd.h
%attr(0644, -, -) %{_libdir}/libsyd.a

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
