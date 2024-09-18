# main.py
#
# Copyright 2023 Nokse
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

import sys

from gi.repository import Gtk, Gio, Adw, Gdk, GLib
from .window import UltimateTicTacToeWindow


class TacticsApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(
            application_id='io.github.nokse22.ultimate-tic-tac-toe',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('restart', self.on_restart_action)
        self.create_action('rules', self.on_rules_action)

        player_action = Gio.SimpleAction.new_stateful(
            "players",
            GLib.VariantType.new("s"),
            GLib.Variant("s", "singleplayer"),
        )
        player_action.connect("activate", self.on_players_changed)

        self.add_action(player_action)

        css = '''
        .tile-button {
            padding: 0px;
        }
        '''

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css, -1)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def on_players_changed(self, action: Gio.SimpleAction, state: GLib.Variant):
        action.set_state(state)
        self.win.multiplayer = False if state.get_string() == "singleplayer" else True
        self.win.restart()

    def on_rules_action(self, widget, _):
        rules_dialog = Adw.Dialog(
            title="How to play", width_request=360, height_request=400)
        toolbar_view = Adw.ToolbarView()
        rules_dialog.set_child(toolbar_view)
        headerbar = Adw.HeaderBar()
        toolbar_view.add_top_bar(headerbar)
        text = '''Just like in regular tic-tac-toe, the two players (X and O) take turns, starting with X. The game starts with X playing wherever they want in any of the 81 empty spots. Next the opponent plays, however they are forced to play in the small board indicated by the relative location of the previous move. For example, if X plays in the top right square of a small (3 × 3) board, then O has to play in the small board located at the top right of the larger board. Playing any of the available spots decides in which small board the next player plays.

If a move is played so that it is to win a small board by the rules of normal tic-tac-toe, then the entire small board is marked as won by the player in the larger board. Once a small board is won by a player or it is filled completely, no more moves may be played in that board. If a player is sent to such a board, then that player may play in any other board. Game play ends when either a player wins the larger board or there are no legal moves remaining, in which case the game is a draw.
        '''
        scrolled = Gtk.ScrolledWindow(vexpand=True)
        toolbar_view.set_content(scrolled)
        scrolled.set_child(
            Gtk.Label(
                label=text,
                wrap=True,
                margin_start=12,
                margin_end=12,
                margin_top=12
            )
        )

        rules_dialog.present(self.win)

    def on_restart_action(self, widget, _):
        self.win.restart()

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.win = self.props.active_window
        if not self.win:
            self.win = UltimateTicTacToeWindow(application=self)
        self.win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(
            application_name='Ultimate Tic Tac Toe',
            application_icon='io.github.nokse22.ultimate-tic-tac-toe',
            developer_name='Nokse',
            version='1.0.0',
            website='https://github.com/Nokse22/ultimate-tic-tac-toe',
            issue_url='https://github.com/Nokse22/ultimate-tic-tac-toe/issues',
            developers=['Nokse'],
            copyright='© 2023 Nokse')
        about.present(self.win)

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = TacticsApplication()
    return app.run(sys.argv)
