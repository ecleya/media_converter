import os
import uuid
import tempfile


class TemporaryFileMixin:
    def __init__(self):
        self._tmp_dir = tempfile.TemporaryDirectory()

    def _new_tmp_filepath(self, extension):
        filepath = os.path.join(self._tmp_dir.name, uuid.uuid4().hex + extension)
        while os.path.exists(filepath):
            filepath = os.path.join(self._tmp_dir.name, uuid.uuid4().hex + extension)

        return filepath
