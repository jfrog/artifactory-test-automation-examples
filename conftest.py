"""
Pytest configuration file for setting up fixtures.
"""

import pytest
from config_loader import ConfigLoader
from resources_loader import ResourcesLoader
import json

@pytest.fixture(scope='session')
def artifactory():
    """
    Fixture to load Artifactory configuration.
    """
    return ConfigLoader()

@pytest.fixture(scope="session")
def resource_loader():
    """
    Fixture to load any resource file with dynamic values.
    """
    loader = ResourcesLoader()
    def _get_resource(template_path, **replacements):
        content = loader.get_resource_template(template_path, **replacements)
        if template_path.endswith(".json"):
            return json.loads(content)
        return content
    return _get_resource
