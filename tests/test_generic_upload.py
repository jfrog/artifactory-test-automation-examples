import os
import requests
import unittest
import pytest
import zipfile

"""
TestGenericUpload
-----------------
This test suite verifies the functionality of uploading a generic ZIP file with custom file size to an Artifactory repository.
The test assumes GENERIC_REPO_KEY is a valid generic repository key in the Artifactory instance.

Tests:
- `test_upload_generic_file`: Creates and uploads a dummy ZIP file to the generic repository and verifies the upload.

Fixtures:
- `setup`: Sets up the Artifactory URL, username, and password for the tests.
- `tearDown`: Cleans created file from os.

Methods:
- `create_dummy_zip`: Creates a dummy ZIP file of the specified size in MB.
- `upload_dummy_zip`: Uploads the dummy ZIP file to the generic repository.
- `verify_upload`: Verifies the upload response.
"""
class TestGenericUpload(unittest.TestCase):
    GENERIC_REPO_KEY = "generic-test"
    DUMMY_FILE_NAME = "dummy01.zip"
    DUMMY_FILE_SIZE_MB = 10  # Set the desired size in MB

    @pytest.fixture(autouse=True)
    def setup(self, artifactory):
        """
        Sets up the Artifactory URL, username, and password for the tests.
        """
        self.artifactory_url = artifactory.get_artifactory_url()
        self.artifactory_username = artifactory.get_username()
        self.artifactory_password = artifactory.get_password()

    def tearDown(self):
        """
        Cleans created file from the filesystem.
        """
        file_path = os.path.join(os.getcwd(), self.DUMMY_FILE_NAME)
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_upload_generic_file(self):
        """
        Creates and uploads a dummy ZIP file to the generic repository and verifies the upload.
        """
        file_path = os.path.join(os.getcwd(), self.DUMMY_FILE_NAME)
        self.create_dummy_zip(file_path, self.DUMMY_FILE_SIZE_MB)
        response = self.upload_dummy_zip(file_path)
        self.verify_upload(response)

    def create_dummy_zip(self, file_path, size_mb):
        """
        Creates a dummy ZIP file of the specified size in MB.
        """
        with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            dummy_content = os.urandom(1024 * 1024)  # 1MB chunk
            for i in range(size_mb):
                zipf.writestr(f"file_{i}.txt", dummy_content)

    def upload_dummy_zip(self, file_path):
        """
        Uploads the dummy ZIP file to the generic repository.
        """
        upload_url = f"{self.artifactory_url}/{self.GENERIC_REPO_KEY}/{self.DUMMY_FILE_NAME}"
        with open(file_path, 'rb') as f:
            response = requests.put(upload_url, auth=(self.artifactory_username, self.artifactory_password), data=f)
        return response

    def verify_upload(self, response):
        """
        Verifies the upload response.
        """
        self.assertEqual(response.status_code, 201, f"Upload failed: {response.text}")

