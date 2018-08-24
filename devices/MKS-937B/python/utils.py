#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path

def get_abs_path(relative):
    """
    relative = relative path with base at python/
    """
    return path.join(path.dirname(path.realpath(__file__)), relative)