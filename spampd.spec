Summary:	spampd - Spam Proxy Daemon
Summary(pl.UTF-8):	spampd - demon spam proxy
Name:		spampd
Version:	2.30
Release:	1
License:	GPL v2+
Group:		Applications/Mail
Source0:	http://www.worlddesign.com/Content/rd/mta/spampd/%{name}-%{version}.tar.gz
# Source0-md5:	742c6f2cb75db54e59d044a8ee40445f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.worlddesign.com/index.cfm/rd/mta/spampd.htm
BuildRequires:	perl-tools-pod
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
# This is not automatically depended as it's only recommendation.
# but we want PLD package be the best!:)
Requires:	perl-Time-HiRes
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

%description -l pl.UTF-8
spampd to program używany wewnątrz systemu dostarczania poczty
elektronicznej w celu przeszukiwania wiadomości pod kątem niechcianej
poczty komercyjnej (UCE - Unsolicited Commercial E-mail, inaczej
spamu). Używa dobrego programu SpamAssassin (SA) do właściwego
przeszukiwania wiadomości. spampd działa jako przezroczyste proxy
SMTP/LMTP pomiędzy dwoma serwerami pocztowymi i w trakcie transakcji
przepuszcza pocztę przez SA. Jeśli SA stwierdzi, że poczta może być
spamem, spampd prosi SA o dodanie do wiadomości nagłówków i raportu
oznaczającego, że wiadomość jest spamem i dlaczego. spampd jest
napisany w Perlu i powinien teoretycznie działać na każdej platformie
obsługiwanej przez Perla i SpamAssassina.

%prep
%setup -q

%build
%{__make} spampd.8

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,/etc/rc.d/init.d,/etc/sysconfig}
install %{name} $RPM_BUILD_ROOT%{_sbindir}
cp -a %{name}.8 $RPM_BUILD_ROOT%{_mandir}/man8
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
%{_mandir}/man8/spampd.8*
