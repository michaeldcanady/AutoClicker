import pyinstaller_versionfile
import os

pyinstaller_versionfile.create_versionfile_from_input_file(
    output_file=os.path.join('.', "src", 'versionfile.txt'),
    input_file=os.path.join('.', "src", 'metadata.yml')
)
