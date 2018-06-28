#!/usr/bin/env python
# -------------------------------------------------------------------------
#                     The CodeChecker Infrastructure
#   This file is distributed under the University of Illinois Open Source
#   License. See LICENSE.TXT for details.
# -------------------------------------------------------------------------
"""
Entry point for the $COMMAND$ command.
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import imp
import os

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
CC = os.path.join(THIS_PATH, "CodeChecker")

# Load CodeChecker from the current folder (the wrapper script (without .py))
CodeChecker = imp.load_source('CodeChecker', CC)

# Execute CC's main script with the current subcommand.
CodeChecker.main("$COMMAND$")
