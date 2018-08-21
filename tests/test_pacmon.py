#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `pacmon` module."""

import json
import os

from pacmon import pacmon



def test_initialization():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))


def test_basic_monitoring_1():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    p.monitor('pypi', 'ioc_fanger')


def test_basic_monitoring_2():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    p.monitor('pypi', 'requests')


def test_basic_monitoring_3():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    p.monitor('pypi', 'onemillion')


def test_change():
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")), 'w+') as f:
        json.dump({
            "onemillion": {
                "abc": "123"
            }
        }, f)
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    changes = p.monitor('pypi', 'onemillion')
    assert changes != {}
