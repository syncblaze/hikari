#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © Nekoka.tt 2019
#
# This file is part of Hikari.
#
# Hikari is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hikari is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Hikari. If not, see <https://www.gnu.org/licenses/>.
"""
Generic users not bound to a guild, and guild-bound member definitions.
"""
from __future__ import annotations

import abc

from hikari.internal_utilities import auto_repr
from hikari.orm.models import interfaces


class IUser(interfaces.FabricatedMixin, interfaces.ISnowflake, interface=True):
    """
    Representation of a user account.
    """

    __slots__ = ()

    #: ID of the user.
    #:
    #: :type: :class:`int`
    id: int

    #: The user name.
    #:
    #: :type: :class:`str`
    username: str

    #: The 4-digit discriminator of the object.
    #:
    #: :type: :class:`int`
    discriminator: int

    #: The hash of the user's avatar, or None if they do not have one.
    #:
    #: :type: :class:`str`
    avatar_hash: str

    #: True if the user is a bot, False otherwise
    #:
    #: :type: :class:`bool`
    bot: bool

    __repr__ = auto_repr.repr_of("id", "username", "discriminator", "bot")


class User(IUser):
    """
    Implementation of the user data type.
    """

    __slots__ = ("_fabric", "id", "username", "discriminator", "avatar_hash", "bot", "__weakref__")

    # noinspection PyMissingConstructor
    def __init__(self, fabric_obj, payload):
        self._fabric = fabric_obj
        self.id = int(payload["id"])
        # We don't expect this to ever change...
        self.bot = payload.get("bot", False)
        self.update_state(payload)

    def update_state(self, payload) -> None:
        self.username = payload.get("username")
        self.discriminator = int(payload["discriminator"])
        self.avatar_hash = payload.get("avatar")


class BotUser(User):
    """
    A special instance of user to represent the bot that is signed in.
    """

    __slots__ = ("verified", "mfa_enabled")

    #: Whether the account is verified or not.
    #:
    #: :type: :class:`bool`
    verified: bool

    #: Whether MFA is enabled or not.
    #:
    #: :type: :class:`bool`
    mfa_enabled: bool

    __repr__ = auto_repr.repr_of("id", "username", "discriminator", "bot", "verified", "mfa_enabled")

    def __init__(self, fabric_obj, payload):
        super().__init__(fabric_obj, payload)

    def update_state(self, payload) -> None:
        super().update_state(payload)
        self.verified = payload.get("verified", False)
        self.mfa_enabled = payload.get("mfa_enabled", False)


__all__ = ["IUser", "User", "BotUser"]