import subprocess
import os
import requests
import unittest
import pytest
import re


"""
TestNpmPublish
--------------
This test suite verifies the functionality of publishing an NPM package to an Artifactory repository.
The test assumes NPM_REPO_KEY is a valid NPM repository key in the Artifactory instance.

Tests:
- `test_publish_npm_package`: Creates an NPM package, writes the .npmrc file, publishes the package, and verifies the upload.

Fixtures:
- `setup`: Sets up the Artifactory URL, username, password, token, and loads the package.json template.
- `tearDown`: Cleans created files from os.

Methods:
- `create_npm_package`: Creates the package.json and index.js files for the NPM package.
- `write_npmrc_file`: Writes the .npmrc file with the authentication token.
- `publish_npm_package`: Publishes the NPM package using npm commands.
- `verify_package_upload`: Verifies the uploaded package in the repository.
"""
class TestNpmPublish(unittest.TestCase):
    NPM_REPO_KEY = "npm-test"
    NPM_PACKAGE_TEMPLATE_PATH = "npm_package_template.json"
    NPM_PACKAGE_NAME = "example-npm-package"
    NPM_PACKAGE_VERSION = "1.0.1"

    @pytest.fixture(autouse=True)
    def setup(self, artifactory, resource_loader):
        """
        Sets up the Artifactory URL, username, password, token, and loads the package.json template.
        """
        self.artifactory_url = artifactory.get_artifactory_url()
        self.artifactory_username = artifactory.get_username()
        self.artifactory_password = artifactory.get_password()
        self.artifactory_token = artifactory.get_token()
        self.package_json_content = resource_loader(
            self.NPM_PACKAGE_TEMPLATE_PATH,
            package_name=self.NPM_PACKAGE_NAME,
            package_version=self.NPM_PACKAGE_VERSION
        )

    def tearDown(self):
        """
        Cleans created files from the filesystem.
        """
        for file in ["package.json", "index.js", ".npmrc"]:
            if os.path.exists(file):
                os.remove(file)

    def test_publish_npm_package(self):
        """
        Creates an NPM package, writes the .npmrc file, publishes the package, and verifies the upload.
        """
        npm_repo_url_no_protocol = re.sub(r'^https?://', '', f"{self.artifactory_url}/api/npm/{self.NPM_REPO_KEY}/")
        npm_repo_url =  f"{self.artifactory_url}/api/npm/{self.NPM_REPO_KEY}/"
        self.create_npm_package()
        self.write_npmrc_file(npm_repo_url, npm_repo_url_no_protocol)
        result = self.publish_npm_package(npm_repo_url_no_protocol)
        assert result.returncode == 0, "NPM Publish failed."
        response = self.verify_package_upload()
        assert response.status_code == 200, f"Failed to verify package: {response.status_code}"

    def create_npm_package(self):
        """
        Creates the package.json and index.js files for the NPM package.
        """
        with open("package.json", "w") as f:
            f.write(str(self.package_json_content).replace("'", '"'))
        with open("index.js", "w") as f:
            f.write('console.log("Hello, npm!");')

    def write_npmrc_file(self, npm_repo_url, npm_repo_url_no_protocol):
        """
        Writes the .npmrc file with the authentication token.
        """
        npmrc_content = f"""
        email = youremail@email.com
        always-auth = true
        registry=http://{npm_repo_url_no_protocol}
        //{npm_repo_url_no_protocol}:_authToken={self.artifactory_token}
        """
        with open(".npmrc", "w") as npmrc_file:
            npmrc_file.write(npmrc_content)

    def publish_npm_package(self, npm_repo_url_no_protocol):
        """
        Publishes the NPM package using npm command.
        """
        publish_command = [
            "npm",
            "publish",
            "--registry",
            f"http://{npm_repo_url_no_protocol}"
        ]
        result = subprocess.run(publish_command, capture_output=True, text=True)
        print(f"\nNPM Publish result: {result}")
        return result

    def verify_package_upload(self):
        """
        Verifies the uploaded package in the repository.
        """
        package_url = f"{self.artifactory_url}/api/npm/{self.NPM_REPO_KEY}/{self.NPM_PACKAGE_NAME}/"
        response = requests.get(package_url, auth=(self.artifactory_username, self.artifactory_password))
        return response

