"""
Flask configuration and the setup factory.
The extension and conf namespace can be seen as a singleton for global variables.

SPDX-FileCopyrightText: © 2024 Gilles Bellot <gilles.bellot@bell0bytes.eu>
SPDX-License-Identifier: AGPL-3.0-or-later
"""
from .factory import createApp
__all__=['createApp']