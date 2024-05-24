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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        print(self.grid)

        for x in range(3):
            for y in range(3):
                child = self.grid.get_child_at(x, y)
                child.x = x
                child.y = y

    def set_child_player_by(x, y, player_id):
        self.childs[x, y].played_by = player_id

    @Gtk.Template.Callback("on_button_clicked")
    def on_button_clicked(self, btn):
        self.emit("button-clicked", btn)

    def get_child_at(self, x, y):
        return self.grid.get_child_at(x, y)

    def won(self, player):
        self.won_by = player
        match player:
            case PlayerID.X:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("/home/lorenzo/Projects/ultimate-tic-tac-toe/src/images/cross-large-symbolic.svg", -1, 100, True)
                self.image.set_from_pixbuf(pixbuf)
                # self.picture.set_resource("./images/cross-large-symbolic.svg")
                # self.image.set_from_icon_name("cross-large-symbolic")
                # self.image.set_from_file("/home/lorenzo/Projects/ultimate-tic-tac-toe/src/images/cross-large-symbolic.svg")
            case PlayerID.O:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("/home/lorenzo/Projects/ultimate-tic-tac-toe/src/images/circle-outline-thick-symbolic.svg", -1, 100, True)
                self.image.set_from_pixbuf(pixbuf)
                # self.image.set_from_icon_name("circle-outline-thick-symbolic")
                # self.image.set_from_file("/home/lorenzo/Projects/ultimate-tic-tac-toe/src/images/circle-outline-thick-symbolic.svg")
                # self.picture.set_resource("./images/circle-outline-thick-symbolic.svg")

        GLib.timeout_add(500, self.stack.set_visible_child_name, "won_view")

    def reset(self):
        self.stack.set_visible_child_name("grid_view")
        self.set_sensitive(True)
        for x in range(3):
            for y in range(3):
                child = self.get_child_at(x, y)
                child.reset()
