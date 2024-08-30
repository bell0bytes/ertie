"""
The Ertië driver. The main workhorse is the __init__.py file in the app subfolder.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# IMPORTS ##############################################################################################################
########################################################################################################################
from app import createApp

########################################################################################################################
# MAIN #################################################################################################################
########################################################################################################################
try:
    # create the Flask app and run it
    ertie = createApp()

except Exception as e:
    # if an Exception occurs, print an error message and quit
    print(f'Critical Error: Unable to initialise Ertië!\nMessage: {e}')
    raise SystemExit(1)