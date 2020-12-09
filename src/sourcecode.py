"""
Class for program source code
"""

import uuid
import os


class SourceCode:
    def __init__(self, code: str = None, path: str = None):
        self.code = code
        self.path = path
        self.created_by_program = False

    def create_file(self) -> str:
        """
        Creates a file for the source code and returns path to that file

        To be able to execute the code
        Assumption: code is in Java
        """

        if self.path is None:
            filename = uuid.uuid4().hex + ".java"
            self.created_by_program = True
            self.path = os.path.join(os.getcwd(), filename)
            with open(self.path, "w") as f:
                f.write(self.code)

        return self.path

    def delete_file(self):
        """
        Deletes a file with the source code
        """
        if self.path is None or self.created_by_program is False:
            return
        os.remove(self.path)
