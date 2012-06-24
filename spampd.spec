%include	/usr/lib/rpm/macros.perl
Summary:	spampd - Spam Proxy Daemon
Summary(pl):	spampd - demon spam proxy
Name:		spampd
Version:	2.20
Release:	0.5
Epoch:		0
License:	GPL v2+
Group:		Applications/Mail
Source0:	http://www.worlddesign.com/Content/rd/mta/spampd/spampd-2.20.tar.gz
# Source0-md5:	4efdb66e424bc24f8a7ce3bf6264ce31
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.worlddesign.com/index.cfm/rd/mta/spampd.htm
BuildRequires:	perl-tools-pod
BuildRequires:	rpmbuild(macros) >= 1.228
# This is not automatically depended as it's only recommendation.
# but we want PLD package be the best! :)
Requires:	perl-Time-HiRes
Requires(post,preun):	rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
spampd is a program used within an e-mail delivery system to scan
messages for possible Unsolicited Commercial E-mail (UCE, aka spam)
content. It uses an excellent program called SpamAssassin (SA) to do
the actual message scanning. spampd acts as a transparent SMTP/LMTP
proxy between two mail servers, and during the transaction it passes
the mail through SA. If SA decides the mail could be spam, then spampd
will ask SA to add some headers and a report to the message indicating
it's spam and why. spampd is written in Perl and should theoretically
run on any platform supported by Perl and SpamAssassin.

%description -l pl
spampd to program u�ywany wewn�trz systemu dostarczania poczty
elektronicznej w celu przeszukiwania wiadomo�ci pod k�tem niechcianej
poczty komercyjnej (UCE - Unsolicited Commercial E-mail, inaczej
spamu). U�ywa dobrego programu SpamAssassin (SA) do w�a�ciwego
przeszukiwania wiadomo�ci. spampd dzia�a jako przezroczyste proxy
SMTP/LMTP pomi�dzy dwoma serwerami pocztowymi i w trakcie transakcji
przepuszcza poczt� przez SA. Je�li SA stwierdzi, �e poczta mo�e by�
spamem, spampd prosi SA o dodanie do wiadomo�ci nag��wk�w i raportu
oznaczaj�cego, �e wiadomo�� jest spamem i dlaczego. spampd jest
napisany w Perlu i powinien teoretycznie dzia�a� na ka�dej platformie
obs�ugiwanej przez Perla i SpamAssassina.

%prep
%setup -q

%build
pod2man spampd > spampd.1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,/etc/rc.d/init.d,/etc/sysconfig}
install %{name} $RPM_BUILD_ROOT%{_sbindir}
install %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc changelog.txt spampd.html
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{_mandir}/man1/*
