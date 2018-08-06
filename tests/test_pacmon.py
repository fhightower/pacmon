#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `pacmon` module."""

import os

from pacmon import pacmon



def test_initialization():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))


def test_basic_monitoring():
    p = pacmon.Pacmon(os.path.abspath(os.path.join(os.path.dirname(__file__), "./test_output.json")))
    p.monitor('pypi', 'onemillion')
