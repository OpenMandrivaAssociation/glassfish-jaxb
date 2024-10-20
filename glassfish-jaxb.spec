%{?_javapackages_macros:%_javapackages_macros}
Name: glassfish-jaxb
Version: 2.2.5
Release: 8.3
Summary: JAXB Reference Implementation
Group:	Development/Java

License: CDDL and GPLv2 with exceptions
URL: https://jaxb.java.net

# svn export https://svn.java.net/svn/jaxb~version2/tags/jaxb-2_2_5/ glassfish-jaxb-2.2.5
# find glassfish-jaxb-2.2.5/ -name '*.class' -delete
# find glassfish-jaxb-2.2.5/ -name '*.jar' -delete
# find glassfish-jaxb-2.2.5/ -name '*.zip' -delete
# find glassfish-jaxb-2.2.5/ -name '*.dll' -delete
# tar czf glassfish-jaxb-2.2.5.tar.gz glassfish-jaxb-2.2.5
Source0: %{name}-%{version}.tar.gz

# JAXB implementation POM:
Source1: http://repo1.maven.org/maven2/com/sun/xml/bind/jaxb-impl/2.2.5/jaxb-impl-2.2.5.pom

# JAXB XJC POM:
Source2: http://repo1.maven.org/maven2/com/sun/xml/bind/jaxb-xjc/2.2.5/jaxb-xjc-2.2.5.pom

# Ant build file used to generate the Javadoc (this is not part of the original
# source but written on purpose for the packaging):
Source3: build-javadoc.xml

# Use resolver from xml-commons-resolver instead of an internal rebundled one:
Patch0: %{name}-dont-use-internal-resolver.patch

# Don't try to generate the 1.0 runtime:
Patch1: %{name}-dont-generate-1.0-runtime.patch

# Removing Jing driver because of incompatibility issues:
Patch2: %{name}-dont-generate-jing-rnc-driver.patch

# Don't bundle the contents of other jar files in the XJC compiler jar file:
Patch3: %{name}-dont-bundle-other-jars.patch

# Remove the class-path entry from the generated manifest files:
Patch4: %{name}-remove-classpath-from-manifests.patch

# Patch the POM files to include the dependencies corresponding to the jar
# files that we aren't bundling within the jat files of this package:
Patch5: %{name}-add-dependencies.patch

# Don't use the prebuilt javadocs:
Patch6: %{name}-dont-use-prebuilt-javadocs.patch

# Don't build the examples as they need additional dependencies:
Patch7: %{name}-dont-build-examples.patch

# Fix Java 8 compatibility
Patch8: %{name}-fix-java8-compatibility.patch

BuildArch: noarch

BuildRequires: javapackages-local
BuildRequires: java-devel

BuildRequires: ant
BuildRequires: codemodel
BuildRequires: istack-commons
BuildRequires: relaxngcc
BuildRequires: xml-commons-resolver
BuildRequires: txw2
BuildRequires: relaxngDatatype
BuildRequires: glassfish-dtd-parser
BuildRequires: glassfish-jaxb-api
BuildRequires: glassfish-fastinfoset
BuildRequires: jing
BuildRequires: stax-ex
BuildRequires: isorelax
BuildRequires: xsom
BuildRequires: rngom

%description
GlassFish JAXB Reference Implementation.


%package javadoc
Summary: Javadocs for %{name}

Requires: jpackage-utils


%description javadoc
This package contains the API documentation for %{name}.


%prep

# Unpack the sources:
%setup -q

# Put the POM files in place (we do this before patching because we need to
# patch the POMs in order to add the dependencies for the artifacts that we are
# not bundling):
cp %{SOURCE1} jaxb-impl.pom
cp %{SOURCE2} jaxb-xjc.pom

# Apply the patches:
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

# Link the libraries where the build script expects them:
ln -s $(build-classpath codemodel) tools/lib/rebundle/compiler/codemodel.jar
ln -s $(build-classpath glassfish-dtd-parser) tools/lib/rebundle/compiler/dtd-parser.jar
ln -s $(build-classpath istack-commons-tools) tools/lib/rebundle/compiler/istack-commons-tools.jar
ln -s $(build-classpath relaxngDatatype) tools/lib/rebundle/compiler/relaxngDatatype.jar
ln -s $(build-classpath xml-resolver) tools/lib/rebundle/compiler/resolver.jar
ln -s $(build-classpath rngom) tools/lib/rebundle/compiler/rngom.jar
ln -s $(build-classpath xsom) tools/lib/rebundle/compiler/xsom.jar
ln -s $(build-classpath isorelax) tools/lib/rebundle/runtime/isorelax.jar
ln -s $(build-classpath msv-msv) tools/lib/rebundle/runtime/msv.jar
ln -s $(build-classpath relaxngDatatype) tools/lib/rebundle/runtime/relaxngDatatype.jar
ln -s $(build-classpath istack-commons-runtime) tools/lib/rebundle/runtime2/istack-commons-runtime.jar
ln -s $(build-classpath txw2) tools/lib/rebundle/runtime2/txw2.jar
ln -s $(build-classpath jaxb-api) tools/lib/redist/jaxb-api.jar
ln -s $(build-classpath glassfish-fastinfoset) tools/lib/util/FastInfoset.jar
ln -s $(build-classpath args4j) tools/lib/util/args4j.jar
ln -s $(build-classpath codemodel-annotation-compiler) tools/lib/util/codemodel-annotation-compiler.jar
ln -s $(build-classpath dom4j) tools/lib/util/dom4j.jar
ln -s $(build-classpath jing) tools/lib/util/jing.jar
ln -s $(build-classpath relaxngcc) tools/lib/util/relaxngcc.jar
ln -s $(build-classpath stax-ex) tools/lib/util/stax-ex.jar
ln -s $(build-classpath txwc2) tools/lib/util/txwc2.jar

# Put the Javadoc build file in place (no patching needed here, as this is not
# part of the original source):
cp %{SOURCE3} build-javadoc.xml


%build

# Build the binaries:
ant \
  -Dbuild.sysclasspath=last \
  -Dbuild.number=1 \
  dist

# Build the javadoc for the runtime and the compiler:
ant \
  -Dbuild.sysclasspath=last \
  -f build-javadoc.xml


%install

%mvn_artifact jaxb-impl.pom dist/lib/jaxb-impl.jar
%mvn_artifact jaxb-xjc.pom dist/lib/jaxb-xjc.jar

%mvn_install -J apidocs/

%files -f .mfiles
%doc License.txt
%doc License.html


%files javadoc -f .mfiles-javadoc
%doc License.txt
%doc License.html


%changelog
* Mon Oct 27 2014 Michal Srb <msrb@redhat.com> - 2.2.5-8
- Fix FTBFS (Resolves: rhbz#1106636)
- Adapt to current packaging guidelines
- Remove R, add BR: javapackages-local (for %%mvn_artifact macro)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.5-6
- Use Requires: java-headless rebuild (#1067528)
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 13 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.5-2
- Add missing xsom and rngom dependencies to the POM files

* Sat Mar 10 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.5-1
- Updated to upstream version 2.2.5
- Removed classpath from manifest files

* Wed Mar 7 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.4u1-4
- Updated to reflect the change from glassfish-fi to glassfish-fastinfoset

* Wed Feb 22 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.4u1-3
- Updated to reflect the changes of the jar names in txw2

* Wed Feb 22 2012 Juan Hernandez <juan.hernandez@redhat.com> 2.2.4u1-2
- Cleanup of the spec file

* Sat Jan 21 2012 Marek Goldmann <mgoldman@redhat.com> 2.2.4u1-1
- Initial packaging

