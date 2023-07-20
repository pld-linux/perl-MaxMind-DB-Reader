#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	MaxMind
%define		pnam	DB-Reader
Summary:	Read MaxMind DB files and look up IP addresses
#Summary(pl.UTF-8):
Name:		perl-MaxMind-DB-Reader
Version:	1.000014
Release:	1
License:	artistic_2
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/M/MA/MAXMIND/MaxMind-DB-Reader-%{version}.tar.gz
# Source0-md5:	cd5c259023f7b483cc1204398dcaa6b4
# generic URL, check or change before uncommenting
URL:		https://metacpan.org/release/MaxMind-DB-Reader
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
%if %{with tests}
BuildRequires:	perl(Data::IEEE754)
BuildRequires:	perl(List::AllUtils)
BuildRequires:	perl(MaxMind::DB::Common) >= 0.040001
BuildRequires:	perl(MaxMind::DB::Metadata)
BuildRequires:	perl(MaxMind::DB::Role::Debugs)
BuildRequires:	perl(MaxMind::DB::Types)
BuildRequires:	perl(MooX::StrictConstructor)
BuildRequires:	perl(Path::Class) >= 0.27
BuildRequires:	perl(Test::Bits)
BuildRequires:	perl(Test::MaxMind::DB::Common::Data)
BuildRequires:	perl(Test::MaxMind::DB::Common::Util)
BuildRequires:	perl-Data-Printer
BuildRequires:	perl-Data-Validate-IP >= 0.25
BuildRequires:	perl-DateTime
BuildRequires:	perl-Module-Implementation
BuildRequires:	perl-Moo >= 1.003000
BuildRequires:	perl-Role-Tiny >= 1.003002
BuildRequires:	perl-Test-Fatal
BuildRequires:	perl-Test-Number-Delta
BuildRequires:	perl-Test-Requires
BuildRequires:	perl-namespace-autoclean
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Read MaxMind DB files and look up IP addresses.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+perl(\s|$),#!%{__perl}\1,' \
      bin/mmdb-dump-metadata \
      bin/mmdb-dump-search-tree \
      eg/benchmark \
      eg/lookup-ip-address \
      eg/mmdb-dump-database

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a eg $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes INSTALL
%attr(755,root,root) %{_bindir}/mmdb-dump-metadata
%attr(755,root,root) %{_bindir}/mmdb-dump-search-tree
%{perl_vendorlib}/MaxMind/DB/Reader.pm
%{perl_vendorlib}/MaxMind/DB/Reader
%{_mandir}/man3/MaxMind::DB::Reader.3*
%{_examplesdir}/%{name}-%{version}
