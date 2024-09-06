"""
Administration / Configuration component.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

# INCLUDES #############################################################################################################
from flask import Blueprint

# BLUEPRINT ############################################################################################################
bpAdmin = Blueprint('admin', __name__, url_prefix='/admin')

# ROUTES ###############################################################################################################
from .adminLobby import lobby
from .roles import roleAdd, roleDelete