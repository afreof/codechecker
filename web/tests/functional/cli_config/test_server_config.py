#
# -------------------------------------------------------------------------
#
#  Part of the CodeChecker project, under the Apache License v2.0 with
#  LLVM Exceptions. See LICENSE for license information.
#  SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
# -------------------------------------------------------------------------

"""
Test server configuration file.
"""


import json
import multiprocessing
import os
import unittest

from libtest import codechecker
from libtest import env

from . import setup_class_common, teardown_class_common


class TestServerConfig(unittest.TestCase):
    _ccClient = None

    def setup_class(self):
        setup_class_common("server_config")

    def teardown_class(self):
        teardown_class_common()

    def setup_method(self, method):

        # TEST_WORKSPACE is automatically set by test package __init__.py .
        self.test_workspace = os.environ['TEST_WORKSPACE']
        self.codechecker_cfg = env.import_codechecker_cfg(self.test_workspace)

        test_class = self.__class__.__name__
        print('Running ' + test_class + ' tests in ' + self.test_workspace)

        # Get the CodeChecker cmd if needed for the tests.
        self._codechecker_cmd = env.codechecker_cmd()

        self.config_file_json = os.path.join(
            self.test_workspace, "codechecker.json")
        self.config_file_yaml = os.path.join(
            self.test_workspace, "codechecker.yaml")

    def test_valid_json_config(self):
        """ Start server with a valid JSON configuration file. """
        with open(self.config_file_json, 'w+',
                  encoding="utf-8", errors="ignore") as config_f:
            json.dump({
                'server': ['--skip-db-cleanup']}, config_f)

        event = multiprocessing.Event()
        event.clear()

        self.codechecker_cfg['viewer_port'] = env.get_free_port()

        server_access = \
            codechecker.start_server(self.codechecker_cfg, event,
                                     ['--config', self.config_file_json])
        event.set()
        event.clear()
        with open(server_access['server_output_file'], 'r',
                  encoding='utf-8', errors='ignore') as out:
            content = out.read()
            self.assertFalse('usage: CodeChecker' in content)

    def test_valid_yaml_config(self):
        """ Start server with a valid YAML configuration file. """
        with open(self.config_file_yaml, 'w+',
                  encoding="utf-8", errors="ignore") as config_f:
            config_f.write("""
# Server related options:
server:
  - --skip-db-cleanup""")

        event = multiprocessing.Event()
        event.clear()

        self.codechecker_cfg['viewer_port'] = env.get_free_port()

        server_access = \
            codechecker.start_server(self.codechecker_cfg, event,
                                     ['--config', self.config_file_yaml])
        event.set()
        event.clear()
        with open(server_access['server_output_file'], 'r',
                  encoding='utf-8', errors='ignore') as out:
            content = out.read()
            self.assertFalse('usage: CodeChecker' in content)

    def test_invalid_config(self):
        """ Start server with an invalid configuration file. """
        with open(self.config_file_json, 'w+',
                  encoding="utf-8", errors="ignore") as config_f:
            json.dump({
                'server': ['--dummy-option']}, config_f)

        event = multiprocessing.Event()
        event.clear()

        self.codechecker_cfg['viewer_port'] = env.get_free_port()

        server_access = \
            codechecker.start_server(self.codechecker_cfg, event,
                                     ['--config', self.config_file_json])
        event.set()
        event.clear()
        with open(server_access['server_output_file'], 'r',
                  encoding='utf-8', errors='ignore') as out:
            content = out.read()
            self.assertTrue('usage: CodeChecker' in content)

    def test_empty_config(self):
        """ Start server with an empty configuration file. """
        with open(self.config_file_json, 'w+',
                  encoding="utf-8", errors="ignore") as config_f:
            config_f.write("")

        event = multiprocessing.Event()
        event.clear()

        self.codechecker_cfg['viewer_port'] = env.get_free_port()

        server_access = \
            codechecker.start_server(self.codechecker_cfg, event,
                                     ['--config', self.config_file_json])
        event.set()
        event.clear()
        with open(server_access['server_output_file'], 'r',
                  encoding='utf-8', errors='ignore') as out:
            content = out.read()
            self.assertFalse('usage: CodeChecker' in content)
