"""
Class for program source code
"""

import uuid
import os


class SourceCode:
    def __init__(self, code: str = None, path: str = None):
        self.code = code
        self.path = path

    def create_file(self) -> str:
        """
        Creates a file for the source code and returns path to that file

        To be able to execute the code
        Assumption: code is in Java
        """

        if self.path is None:
            filename = uuid.uuid4().hex + ".java"

            self.path = os.path.join(os.getcwd(), filename)
            with open(self.path, "w") as f:
                f.write(self.code)

        return self.path

    def delete_file(self):
        """
        Deletes a file with the source code
        """
        if self.path is None:
            return
        os.remove(self.path)
