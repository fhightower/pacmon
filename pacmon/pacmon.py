#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Software package monitoring system which sends alerts when a package has been changed."""

import hashlib
import json
import os
import subprocess
import tempfile

DEFAULT_OUTPUT_DATA_PATH = os.path.join(os.path.expanduser('~/.pacmon'), 'pacmon_hashes.json')


class Pacmon(object):
    def __init__(self, output_path=os.path.join(DEFAULT_OUTPUT_DATA_PATH)):
        super(Pacmon, self).__init__()
        self.local_package_file_path = None
        self.output_path = output_path
        self.package_hashes = dict()
        self.package_location = None
        self.package_name = None
        self.previous_data = dict()
        self.DOWNLOAD_COMMANDS = {
            'pypi': 'pip install {} --quiet --target {}',
            'npm': 'npm i {} --prefix {}'
        }

        # if the output path does not exist, create it
        if not os.path.exists(self.output_path):
            # create the directory in the specified cache_location
            os.makedirs(self.output_path)

    def _download_package_contents(self):
        # run download command
        with subprocess.Popen(self.DOWNLOAD_COMMANDS[self.package_location].format(self.package_name, self.local_package_file_path).split(' '), stdout=subprocess.PIPE) as proc:
            # TODO: improve handling here to catch errors
            print("stdout: {}".format(proc.stdout.read()))

    def _get_hashes_of_package(self):
        package_hashes = dict()

        # create a path for a pypi package
        if self.package_location == 'pypi':
            base_package_path = os.path.join(self.local_package_file_path, self.package_name)
        # create a path for an npm package
        if self.package_location == 'npm':
            base_package_path = os.path.join(self.local_package_file_path, 'node_modules', self.package_name)

        # iterate through the directories in the newly downloaded package
        for path, dirs, files in os.walk(base_package_path):
            for file_ in files:
                # capture the base path to the file
                file_path = '{}/{}'.format(path, file_)
                # capture path to the file from the top of this package to be used as the key for the hash of the file
                file_key_base = file_path.replace(self.local_package_file_path + '/', '')
                with open(file_path, 'rb') as f:
                    package_hashes[file_key_base] = hashlib.md5(f.read()).hexdigest()

        return package_hashes

    def _get_previous_hashes(self):
        try:
            with open(self.output_path, 'r') as f:
                self.previous_data = json.loads(f.read())
        except FileNotFoundError as e:
            self.previous_data = dict()
        return self.previous_data

    def _compare_hashes(self):
        """Compare the hashes of the files in the newly downloaded package with those of the old package."""
        changes = {
            'added_files': list(),
            'removed_files': list(),
            'changed_files': list()
        }
        # if the previous hashes are the same as the current hashes, no changed files
        if self.previous_data[self.package_name] != self.package_hashes:
            for key, value in self.package_hashes.items():
                if self.previous_data[self.package_name].get(key):
                    # if the file's hash has changed, record it
                    if self.previous_data[self.package_name][key] != value:
                        changes['changed_files'].append(key)
                # if the file is a new file, record it
                else:
                    changes['added_files'].append(key)

            # see if there are any files in the old data that are not in the new data
            for key in self.previous_data[self.package_name]:
                # if the file does not exist in the new package, record it
                if not self.package_hashes.get(key):
                    changes['removed_files'].append(key)
        return changes

    def _record_package_hashes(self):
        self.previous_data[self.package_name] = self.package_hashes
        with open(self.output_path, 'w+') as f:
            json.dump(self.previous_data, f)

    def check_package(self, package_location, package_name):
        """Monitor the given package from the given package_location."""
        changes = dict()
        if package_location not in self.DOWNLOAD_COMMANDS:
            raise ValueError('That package location ({}) is not supported. The available package locations are: {}'.format(package_location, self.DOWNLOAD_COMMANDS.keys()))
        else:
            self.package_name = package_name
            self.package_location = package_location

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            self.local_package_file_path = tmp_dir_name

            # DOWNLOAD PACKAGE CONTENTS
            self._download_package_contents()

            # GET HASHES OF PACKAGE CONTENTS
            self.package_hashes = self._get_hashes_of_package()

        # COMPARE HASHES OF NEW PACKAGE WITH THOSE OF THE OLD PACKAGE
        # see if there are previous hashes for this library
        if self._get_previous_hashes().get(self.package_name):
            # if there are previous hashes for this library, compare the new hashes with the old ones
            changes = self._compare_hashes()
            # # SEND ALERT - On Aug. 21 I removed the code to send an alert... I'll handle this elsewhere
            # if changes['added_files'] or changes['removed_files'] or changes['changed_files']:
            #     self._send_alert(changes)
        else:
            print("There is no previous data for the {} package. I've recorded the current data and will let you know if something changes next time you check this package.".format(self.package_name))

        # RECORD THE PACKAGE HASHES
        self._record_package_hashes()

        return changes
