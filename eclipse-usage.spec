%{?scl:%scl_package eclipse-usage}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

%global gittag %{version}.AM1

Name:             %{?scl_prefix}eclipse-usage
Version:          4.4.3
Release:          0.1.%{baserelease}%{?dist}
Summary:          Usage reporting plug-ins for Eclipse
License:          EPL and ASL 2.0
URL:              http://tools.jboss.org/

# Generate tarball with: ./get-jbosstools.sh
Source0:          jbosstools-%{gittag}.tar.xz
Source1:          get-jbosstools.sh

BuildArch:        noarch

BuildRequires:    %{?scl_prefix}tycho
BuildRequires:    %{?scl_prefix}tycho-extras
BuildRequires:    %{?scl_prefix}eclipse-epp-logging
BuildRequires:    %{?scl_prefix_maven}maven-plugin-build-helper

%description
Usage reporting plug-ins for Eclipse.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n jbosstools-%{gittag}

# Fix whitespace error in xml declaration
sed -i -e '1s/\t//' jbosstools-build/parent/pom.xml

# Fix perms on license
chmod -x jbosstools-base/foundation/features/org.jboss.tools.foundation.license.feature/license.html

# Remove unnecessary plugins from parent pom
%pom_remove_plugin org.jboss.tools.tycho-plugins:repository-utils jbosstools-build/parent
%pom_remove_plugin org.jacoco:jacoco-maven-plugin jbosstools-build/parent
%pom_remove_plugin org.apache.maven.plugins:maven-enforcer-plugin jbosstools-build/parent

# Remove dep on jgit
%pom_xpath_remove "pom:plugin[pom:artifactId='tycho-packaging-plugin']/pom:dependencies" jbosstools-build/parent
%pom_xpath_remove "pom:plugin[pom:artifactId='tycho-packaging-plugin']/pom:configuration/pom:sourceReferences" jbosstools-build/parent
%pom_xpath_set "pom:plugin[pom:artifactId='tycho-packaging-plugin']/pom:configuration/pom:timestampProvider" "default" jbosstools-build/parent

# Disable everything except for usage plugin
%pom_disable_module org.jboss.tools.foundation.feature jbosstools-base/foundation/features
%pom_disable_module org.jboss.tools.foundation.security.linux.feature jbosstools-base/foundation/features
%pom_disable_module org.jboss.tools.foundation.test.feature jbosstools-base/foundation/features
%pom_disable_module plugins jbosstools-base/foundation
%pom_disable_module tests jbosstools-base/foundation
%pom_disable_module org.jboss.tools.usage.test.feature jbosstools-base/usage/features
%pom_disable_module org.jboss.tools.usage.test jbosstools-base/usage/tests

# No need to install poms or license feature
%mvn_package "::pom::" __noinstall
%mvn_package ":org.jboss.tools.foundation.license.feature" __noinstall
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
pushd jbosstools-build
sed -i -e 's/%{version}\.AM./%{gittag}/' parent/pom.xml
%mvn_build -j -- install -f parent/pom.xml
popd

%mvn_build -j -- -Dno-target-platform -f jbosstools-base/pom.xml 
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc jbosstools-base/foundation/features/org.jboss.tools.foundation.license.feature/license.html

%changelog
* Tue Jan 17 2017 Mat Booth <mat.booth@redhat.com> - 4.4.3-0.1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Tue Jan 17 2017 Mat Booth <mat.booth@redhat.com> - 4.4.3-1
- Update to latest release

* Wed Oct 26 2016 Mat Booth <mat.booth@redhat.com> - 4.4.1-3
- Augment the product ID instead of the distro name

* Fri Oct 21 2016 Mat Booth <mat.booth@redhat.com> - 4.4.1-2
- Trim down the source tarball and fix the license tag

* Tue Sep 27 2016 Mat Booth <mat.booth@redhat.com> - 4.4.1-1
- Initial package