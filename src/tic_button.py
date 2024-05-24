# tic_button.py
#
# Copyright 2024 Nokse
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk

from .player_id_enum import PlayerID

class TicButton(Gtk.Button):
    __gtype_name__ = 'TicButton'

    played_by = PlayerID.N

    x = None
    y = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_css_class("tile-button")

    def get_coords(self):
        return (self.x, self.y)

    def set_played_by(self, played):
        match played:
            case PlayerID.X:
                self.set_icon_name("cross-large-symbolic")
                self.add_css_class("error")
                self.played_by = PlayerID.X
            case PlayerID.O:
                self.set_icon_name("circle-outline-thick-symbolic")
                self.add_css_class("accent")
                self.played_by = PlayerID.O

        self.set_sensitive(False)

    def reset(self):
        self.played_by = PlayerID.N
        self.remove_css_class("accent")
        self.remove_css_class("error")
        self.set_icon_name("")
        self.set_sensitive(True)
                
