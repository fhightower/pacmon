#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `pacmon` module."""

import json
import os

from pacmon import pacmon


def test_initialization():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))


def test_pypi_monitoring_1():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    changes = p.check_package('pypi', 'ioc_fanger')
    assert len(changes) == 0


def test_pypi_monitoring_2():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    changes = p.check_package('pypi', 'requests')
    assert len(changes) == 0


def test_pypi_monitoring_3():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    changes = p.check_package('pypi', 'onemillion')
    assert len(changes) == 0


def test_pypi_file_replacement():
    """Make sure file removal and addition is recorded correctly."""
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")), 'w+') as f:
        json.dump({
            "onemillion": {
                "abc": "123"
            }
        }, f)
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    changes = p.check_package('pypi', 'onemillion')
    assert len(changes) == 3
    assert len(changes['added_files']) == 8
    assert len(changes['removed_files']) == 1
    assert len(changes['changed_files']) == 0


def test_pypi_file_change():
    """Make sure a file hash change is recorded correctly."""
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")), 'w+') as f:
        json.dump({
            "onemillion": {
                "onemillion/cli.py": "123"
            }
        }, f)
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    changes = p.check_package('pypi', 'onemillion')
    assert len(changes) == 3
    assert len(changes['added_files']) == 7
    assert len(changes['removed_files']) == 0
    assert len(changes['changed_files']) == 1


def test_npm_monitoring_1():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    changes = p.check_package('npm', 'spaces-ng')
    assert len(changes) == 0


def test_npm_file_replacement():
    """Make sure file removal and addition is recorded correctly."""
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")), 'w+') as f:
        json.dump({
            "spaces-ng": {
                "abc": "123"
            }
        }, f)
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    changes = p.check_package('npm', 'spaces-ng')
    print("changes {}".format(changes))
    assert len(changes) == 3
    assert len(changes['added_files']) == 22
    assert len(changes['removed_files']) == 1
    assert len(changes['changed_files']) == 0


def test_npm_file_change():
    """Make sure a file hash change is recorded correctly."""
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")), 'w+') as f:
        json.dump({
            "spaces-ng": {
                "node_modules/spaces-ng/src/SpacesModule.d.ts": "123",
                "node_modules/spaces-ng/LICENSE": "abc"
            }
        }, f)
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    changes = p.check_package('npm', 'spaces-ng')
    print("changes {}".format(changes))
    assert len(changes) == 3
    assert len(changes['added_files']) == 20
    assert len(changes['removed_files']) == 0
    assert len(changes['changed_files']) == 2
