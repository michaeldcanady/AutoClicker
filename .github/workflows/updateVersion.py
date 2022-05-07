import os
import re

import fire

version_filepath = os.path.join('.', "src", 'VERSION')
version_pattern = re.compile(fr'^\d+.\d+.\d+.\d?$')


def get(with_pre_release_placeholder: bool = False):
    with open(version_filepath, 'r') as version_file:
        version_lines = version_file.readlines()
        assert len(version_lines) == 1, 'Version file is malformed'
        version = version_lines[0]
        assert version_pattern.match(version), 'Version string is malformed'
        return version


def write_version_file(major: int, minor: int, patch: int, build: int):
    version = f'{major}.{minor}.{patch}.{build}'
    with open(version_filepath, 'w') as version_file:
        version_file.write(version)


def inc_build():
    version = get()
    major, minor, patch, build = version.split('.')
    write_version_file(major, minor, patch, int(build) + 1)


def inc_patch():
    version = get()
    major, minor, patch, build = version.split('.')
    write_version_file(major, minor, int(patch) + 1, build)


def inc_minor():
    version = get()
    major, minor, patch, build = version.split('.')
    write_version_file(major, int(minor) + 1, patch, build)


def inc_major():
    version = get()
    major, minor, patch, build = version.split('.')
    write_version_file(int(major) + 1, minor, patch, build)


if __name__ == "__main__":
    fire.Fire({
        'get': get,
        'inc-build': inc_build,
        'inc-patch': inc_patch,
        'inc-minor': inc_minor,
        'inc-major': inc_major
    })
