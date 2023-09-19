%define		vendor_version	2.34.0

Summary:	GitHub’s official command line tool
Name:		github-cli
Version:	2.35.0
Release:	1
License:	MIT
Group:		Development/Tools
#Source0Download: https://github.com/cli/cli/releases
Source0:	https://github.com/cli/cli/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bacce482983a5c722da24bdec1f3cfc0
# cd cli-%{version}
# go mod vendor
# cd ..
# tar cJf github-cli-vendor-%{version}.tar.xz cli-%{version}/vendor
Source1:	%{name}-vendor-%{vendor_version}.tar.xz
# Source1-md5:	8c0a0e5ba2e62dbc68492988287bf0ab
URL:		https://cli.github.com
BuildRequires:	golang >= 1.21
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.009
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%go_arches
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_debugsource_packages	0

%description
gh is GitHub on the command line. It brings pull requests, issues, and
other GitHub concepts to the terminal next to where you are already
working with git and your code.

%package -n bash-completion-github-cli
Summary:	Bash completion for github-cli command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-github-cli
Bash completion for github-cli command line.

%package -n fish-completion-github-cli
Summary:	fish-completion for github-cli
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-github-cli
fish-completion for github-cli.

%package -n zsh-completion-github-cli
Summary:	ZSH completion for github-cli command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-github-cli
ZSH completion for github-cli command line.

%prep
%setup -q -a1 -n cli-%{version}

%{__mv} cli-%{vendor_version}/vendor .

%{__mkdir_p} .go-cache

%build
%__go build -v -mod=vendor -ldflags "-X github.com/cli/cli/v2/internal/build.Date=%(date +%Y-%m-%d) -X github.com/cli/cli/v2/internal/build.Version=%{version}" -o target/gh ./cmd/gh

%__go run ./cmd/gen-docs --man-page --doc-path target/man

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{bash_compdir},%{fish_compdir},%{zsh_compdir}}

install -p target/gh $RPM_BUILD_ROOT%{_bindir}/gh
install -p target/man/* $RPM_BUILD_ROOT%{_mandir}/man1

./target/gh completion -s bash > $RPM_BUILD_ROOT%{bash_compdir}/gh
./target/gh completion -s fish > $RPM_BUILD_ROOT%{fish_compdir}/gh.fish
./target/gh completion -s zsh > $RPM_BUILD_ROOT%{zsh_compdir}/_gh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/gh
%{_mandir}/man1/gh.1*
%{_mandir}/man1/gh-*.1*

%files -n bash-completion-github-cli
%defattr(644,root,root,755)
%{bash_compdir}/gh

%files -n fish-completion-github-cli
%defattr(644,root,root,755)
%{fish_compdir}/gh.fish

%files -n zsh-completion-github-cli
%defattr(644,root,root,755)
%{zsh_compdir}/_gh
