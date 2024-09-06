"""
Component to manage club members.

:Authors:
    - Gilles Bellot

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

# INCLUDES #############################################################################################################
from flask import Blueprint

# BLUEPRINT ############################################################################################################
bpMembers = Blueprint('members', __name__, url_prefix='/members')

# ROUTES ###############################################################################################################
from .membersLobby import lobby





