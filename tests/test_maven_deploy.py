import subprocess
import os
import requests
import unittest
import pytest

"""
TestMavenDeployment
--------------------
This test suite verifies the functionality of deploying a Maven package to an Artifactory repository.
The test assumes MAVEN_REPO_KEY is a valid Maven repository key in the Artifactory instance.

Tests:
- `test_deploy_maven_package`: Creates a Maven project, configures Maven settings, deploys the Maven artifact, and verifies the upload.

Fixtures:
- `setup`: Sets up the Artifactory URL, username, password, and loads the POM and settings XML templates.
- `tearDown`: Cleans created files from os.

Methods:
- `create_maven_project`: Creates the Maven project structure and writes the POM file.
- `get_java_home`: Retrieves the JAVA_HOME path.
- `configure_maven_settings`: Writes the Maven settings XML file.
- `deploy_maven_artifact`: Deploys the Maven artifact using Maven commands.
- `verify_artifact_upload`: Verifies the uploaded artifact in the repository.
"""
class TestMavenDeployment(unittest.TestCase):
    MAVEN_REPO_KEY = "maven-test"
    POM_XML_TEMPLATE_PATH = "maven_pom_template.xml"
    SETTINGS_XML_TEMPLATE_PATH = "maven_settings_template.xml"
    MAVEN_GROUP_ID = "com.example"
    MAVEN_ARTIFACT_ID = "example-maven-package"
    MAVEN_VERSION = "1.0.1"
    JAVA_HOME = ""  # Set it to the JAVA_HOME path if using a custom Java installation or if running on Windows (default - empty)

    @pytest.fixture(autouse=True)
    def setup(self, artifactory, resource_loader):
        """
        Sets up the Artifactory URL, username, password, and loads the POM and settings XML templates.
        """
        self.artifactory_url = artifactory.get_artifactory_url()
        self.artifactory_username = artifactory.get_username()
        self.artifactory_password = artifactory.get_password()
        self.pom_xml = resource_loader(
            self.POM_XML_TEMPLATE_PATH,
            repo_url=f"{self.artifactory_url}/{self.MAVEN_REPO_KEY}",
            group_id=self.MAVEN_GROUP_ID,
            artifact_id=self.MAVEN_ARTIFACT_ID,
            version=self.MAVEN_VERSION
        )
        self.settings_xml = resource_loader(
            self.SETTINGS_XML_TEMPLATE_PATH,
            artifactory_username=self.artifactory_username,
            artifactory_password=self.artifactory_password
        )
        self.java_home = self.get_java_home()

    def tearDown(self):
        """
        Cleans created files from the filesystem.
        """
        if os.path.exists("maven_settings_template.xml"):
            os.remove("maven_settings_template.xml")
        if os.path.exists(self.MAVEN_ARTIFACT_ID):
            for root, dirs, files in os.walk(self.MAVEN_ARTIFACT_ID, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.MAVEN_ARTIFACT_ID)

    def test_deploy_maven_package(self):
        """
        Creates a Maven project, configures Maven settings, deploys the Maven artifact, and verifies the upload.
        """
        self.create_maven_project()
        self.configure_maven_settings()
        result = self.deploy_maven_artifact()
        assert result.returncode == 0, "Maven deploy failed."
        response = self.verify_artifact_upload()
        assert response.status_code == 200, f"Failed to verify artifact: {response.status_code}"

    def create_maven_project(self):
        """
        Creates the Maven project structure and writes the POM file.
        """
        os.makedirs(f"{self.MAVEN_ARTIFACT_ID}/src/main/java", exist_ok=True)
        os.makedirs(f"{self.MAVEN_ARTIFACT_ID}/src/main/resources", exist_ok=True)
        with open(f"{self.MAVEN_ARTIFACT_ID}/pom.xml", "w") as f:
            f.write(self.pom_xml)

    def get_java_home(self):
        """
        Retrieves the JAVA_HOME path if not set by user.
        """
        if self.JAVA_HOME:
            return self.JAVA_HOME
        else:
            try:
                result = subprocess.run(
                    ["/usr/libexec/java_home"], capture_output=True, text=True, check=True
                )
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                print("Error retrieving JAVA_HOME:", e)
                return None

    def configure_maven_settings(self):
        """
        Writes the Maven settings XML file.
        """
        with open("maven_settings_template.xml", "w") as settings_file:
            settings_file.write(self.settings_xml)

    def deploy_maven_artifact(self):
        """
        Deploys the Maven artifact using Maven commands.
        """
        mvn_command = [
            "mvn",
            "clean",
            "deploy",
            f"--settings=maven_settings_template.xml",
            f"-f={self.MAVEN_ARTIFACT_ID}/pom.xml",
        ]
        result = subprocess.run(
            mvn_command,
            env={**os.environ, "JAVA_HOME": self.java_home},
            capture_output=True,
            text=True,
        )
        print(f"\nMaven Deploy result: {result}")
        return result

    def verify_artifact_upload(self):
        """
        Verifies the uploaded artifact in the repository.
        """
        maven_repo_url = f"{self.artifactory_url}/{self.MAVEN_REPO_KEY}"
        artifact_url = (
            f"{maven_repo_url}/{self.MAVEN_GROUP_ID.replace('.', '/')}/"
            f"{self.MAVEN_ARTIFACT_ID}/{self.MAVEN_VERSION}/{self.MAVEN_ARTIFACT_ID}-{self.MAVEN_VERSION}.pom"
        )
        response = requests.get(artifact_url, auth=(self.artifactory_username, self.artifactory_password))
        return response

