# Artifactory Test Automation examples

This project is designed to test API endpoints using **pytest** and **requests**.

## Requirements

- Python 3.8+ (Used for running the tests project)
- Npm 10.2.3+ (Test dependency. Used for the NPM test. The version can be changed according to your requirements but might need to update the test code)
- Apache Maven 3.9.3+ (Test dependency. Used for the Maven test. The version can be changed according to your requirements but might need to update the test code)

## Setup

1. Create a virtual environment:
    ```sh
    python3 -m venv venv
    ```

2. Activate the virtual environment:
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```

3. Install the required Python packages:
    ```sh
    pip3 install -r requirements.txt
    ```

4. Configure your Artifactory credentials, access token and Artifactory Server URL in a configuration file:
   <br>`config.ini`

5. For running all tests smoothly, you need to create the following local repositories in your Artifactory server:
   <br>`Generic repository called "generic-test"`
   <br>`Maven repository called "maven-test"`
   <br>`NPM repository called "npm-test"`

   or you can change the repository names in the test files according to your repository names:
   <br>`tests/test_generic_upload.py -> change GENERIC_REPO_KEY = "generic-test" to your generic repository name`
   <br>`tests/test_maven_deploy.py -> change MAVEN_REPO_KEY = "maven-test" to your maven repository name`
   <br>`tests/test_npm_publish.py -> change NPM_REPO_KEY = "npm-test" to your npm repository name`


## Test Suites

### Generic Upload Test

File: `tests/test_generic_upload.py`

This test suite verifies the functionality of uploading a generic file to an Artifactory repository.

- `test_upload_generic_file`: Creates and uploads a dummy ZIP file to the generic repository and verifies the upload.

### Maven Deployment Test

File: `tests/test_maven_deploy.py`

This test suite verifies the functionality of deploying a Maven package to an Artifactory repository.

- `test_deploy_maven_package`: Creates a Maven project, configures Maven settings, deploys the Maven artifact, and verifies the upload.

### NPM Publish Test

File: `tests/test_npm_publish.py`

This test suite verifies the functionality of publishing an NPM package to an Artifactory repository.

- `test_publish_npm_package`: Creates an NPM package, writes the .npmrc file, publishes the package, and verifies the upload.

## Running the Tests

To run the tests, use the following command:
```sh
pytest
```

