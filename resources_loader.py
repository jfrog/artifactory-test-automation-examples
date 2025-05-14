import os

class ResourcesLoader:
    """
    A class to load and process resource files, as XML or JSON templates resources folder.
    Attributes:
    -----------
    resources_folder : str
        The folder where resource files are located. Defaults to "resources".

    Methods:
    --------
    get_xml_resource_template(template_path: str, **replacements) -> str
        Reads an XML or JSON template file from the resources folder, replaces placeholders with provided values, and returns the processed content.
    """
    def __init__(self, resources_folder: str = "resources"):
        self.resources_folder = resources_folder

    def get_resource_template(self, template_path: str, **replacements) -> str:
        """
        Reads a template file and replaces placeholders with provided values.
        :param template_path: Path to the template file (relative to resources folder)
        :param replacements: Key-value pairs where keys are placeholders in the template
        :return: Processed content with replaced values
        """
        file_path = os.path.join(self.resources_folder, template_path)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        for key, value in replacements.items():
            placeholder = f"{{{{{key}}}}}"  # Handles placeholders like {{key}}
            content = content.replace(placeholder, value)

        return content