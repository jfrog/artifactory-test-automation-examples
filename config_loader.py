"""
Module for loading configuration details from a config file.
"""

import configparser

class ConfigLoader:
    """
    Class to load configuration details from a config file.
    """
    def __init__(self, config_file='config.ini'):
        """
        Initializes the ConfigLoader with the specified config file.
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def _get_config_value(self, section, key):
        """
        Helper method to get a value from the config file and check if it is empty.
        """
        value = self.config[section].get(key)
        if not value:
            raise ValueError(f"The required key '{key}' is empty in the config.ini file.\n"
                             f"This is a required field for the test.")
        return value

    def get_server_url(self):
        """
        Returns the server URL from the config file.
        """
        return self._get_config_value('artifactory', 'server_url')

    def get_artifactory_url(self):
        """
        Returns the Artifactory URL constructed from the server URL.
        """
        return f"{self.get_server_url()}/artifactory"

    def get_username(self):
        """
        Returns the username from the config file.
        """
        return self._get_config_value('artifactory', 'username')

    def get_password(self):
        """
        Returns the password from the config file.
        """
        return self._get_config_value('artifactory', 'password')

    def get_token(self):
        """
        Returns the token from the config file.
        """
        return self._get_config_value('artifactory', 'token')