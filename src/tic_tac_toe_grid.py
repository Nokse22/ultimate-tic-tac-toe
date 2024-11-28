# tic_tac_toe_grid.py
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
from gi.repository import GObject, GLib, GdkPixbuf

from .player_id_enum import PlayerID
from .tic_button import TicButton


@Gtk.Template(resource_path='/io/github/nokse22/ultimate-tic-tac-toe/ui/tic_tac_toe_grid.ui')
class TicTacToeGrid(Adw.Bin):
    __gtype_name__ = 'TicTacToeGrid'

    __gsignals__ = {
        'button-clicked': (GObject.SignalFlags.RUN_FIRST, None, (Gtk.Widget,)),
    }

    grid = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    image = Gtk.Template.Child()

    won_by = PlayerID.N

    x = None
    y = None

    resource_path = "/io/github/nokse22/ultimate-tic-tac-toe/images"

    x_pixbuf = GdkPixbuf.Pixbuf.new_from_resource_at_scale(
        f"{resource_path}/cross-large-symbolic.svg", -1, 500, True)
    o_pixbuf = GdkPixbuf.Pixbuf.new_from_resource_at_scale(
        f"{resource_path}/circle-outline-thick-symbolic.svg", -1, 500, True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for x in range(3):
            for y in range(3):
                child = self.grid.get_child_at(x, y)
                child.x = x
                child.y = y

    @Gtk.Template.Callback("on_button_clicked")
    def on_button_clicked(self, btn):
        self.emit("button-clicked", btn)

    def get_child_at(self, x, y):
        return self.grid.get_child_at(x, y)

    def won(self, player):
        self.won_by = player
        match player:
            case PlayerID.X:
                self.image.set_from_pixbuf(self.x_pixbuf)
            case PlayerID.O:
                self.image.set_from_pixbuf(self.o_pixbuf)

        GLib.timeout_add(500, self.stack.set_visible_child_name, "won_view")

    def reset(self):
        self.stack.set_visible_child_name("grid_view")
        self.set_sensitive(True)
        self.won_by = PlayerID.N
        for x in range(3):
            for y in range(3):
                child = self.get_child_at(x, y)
                child.reset()
