%include	/usr/lib/rpm/macros.perl
Summary:	spampd - Spam Proxy Daemon
Name:		spampd
Version:	2.20
Release:	0.1
Epoch:		0
License:	GPL v2+
Group:		Applications/Mail
Source0:	http://www.worlddesign.com/Content/rd/mta/spampd/spampd-2.20.tar.gz
# Source0-md5:	4efdb66e424bc24f8a7ce3bf6264ce31
URL:		http://www.worlddesign.com/index.cfm/rd/mta/spampd.htm
%if %{with initscript}
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
%endif
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

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc changelog.txt spampd.html
%attr(755,root,root) %{_sbindir}/*
