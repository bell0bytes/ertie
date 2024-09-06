"""
Models for Users / Members

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

########################################################################################################################
# INCLUDES #############################################################################################################
########################################################################################################################
# this is necessary for the relationship function to work
from .members import Member
from .membersChangeLog import MemberChangeLog
from .roles import Role, RoleUserMapping
