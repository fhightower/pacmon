#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Software package monitoring system which sends alerts when a package has been changed."""

import hashlib
import os
import subprocess
import tempfile


class Pacmon(object):
    def __init__(self, output_path):
        super(Pacmon, self).__init__()
        self.output_path = output_path
        self.package_name = None
        self.package_location = None
        self.local_package_file_path = None
        self.DOWNLOAD_COMMANDS = {
            'pypi': 'pip install {} --quiet --target {}',
            'npm': ''
        }
        self.package_hashes = dict()

    def download_package_contents(self):
        # run download command
        with subprocess.Popen(['pip', 'install', 'onemillion', '--quiet', '--target', '{}'.format(self.local_package_file_path)], stdout=subprocess.PIPE) as proc:
            print("stdout {}".format(proc.stdout.read()))

    def get_hashes_of_package(self):
        package_hashes = dict()
        # iterate through the directories in the newly downloaded package
        for path, dirs, files in os.walk(os.path.join(self.local_package_file_path, self.package_name)):
            for file_ in files:
                # capture the base path to the file
                file_path = '{}/{}'.format(path, file_)
                # capture path to the file from the top of this package to be used as the key for the hash of the file
                file_key_base = file_path.replace(self.local_package_file_path + '/', '')
                with open(file_path, 'rb') as f:
                    package_hashes[file_key_base] = hashlib.md5(f.read()).hexdigest()

        return package_hashes

    def get_previous_hashes(self):
        # TODO: implement
        pass

    def compare_hashes(self):
        """Compare the hashes of the files in the newly downloaded package with those of the old package."""
        # TODO: implement
        pass

    def send_alert(self, changes):
        # TODO: implement
        pass

    def record_package_hashes(self):
        # TODO: implement
        pass

    def monitor(self, package_location, package_name):
        """Monitor the given package from the given package_location."""
        if package_location not in self.DOWNLOAD_COMMANDS:
            raise ValueError('That package location ({}) is not supported. The available package locations are: {}'.format(package_location, self.DOWNLOAD_COMMANDS.keys()))
        else:
            self.package_name = package_name
            self.package_location = package_location

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            self.local_package_file_path = tmp_dir_name

            # DOWNLOAD PACKAGE CONTENTS
            self.download_package_contents()

            # GET HASHES OF PACKAGE CONTENTS
            self.package_hashes = self.get_hashes_of_package()

            print("package hashes {}".format(self.package_hashes))

            assert 1 == 2

        # COMPARE HASHES OF NEW PACKAGE WITH THOSE OF THE OLD PACKAGE
        # see if there are previous hashes for this library
        if self.get_previous_hashes():
            # if there are previous hashes for this library, compare the new hashes with the old ones
            changes = self.compare_hashes()
        else:
            print("There is no previous data for the {} package. I've recorded the current data and will let you know if something changes next time you check this package.".format(self.package_name))

        # SEND ALERT
        if changes:
            self.send_alert(changes)

        # RECORD THE PACKAGE HASHES
        self.record_package_hashes()


if __name__ == '__main__':
    main()
