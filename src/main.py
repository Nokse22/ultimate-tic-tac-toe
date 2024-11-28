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

from gi.repository import Gtk, Gio, Adw, GLib
from .window import UltimateTicTacToeWindow

from os import path

import gettext
from gettext import gettext as _

LOCALE_DIR = path.join(
    path.dirname(__file__).split("ultimate-tic-tac-toe")[0], "locale"
)
gettext.bindtextdomain("ultimate-tic-tac-toe", LOCALE_DIR)
gettext.textdomain("ultimate-tic-tac-toe")


class TacticsApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(
            application_id="io.github.nokse22.ultimate-tic-tac-toe",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self.create_action("quit", lambda *_: self.quit(), ["<primary>q"])
        self.create_action("about", self.on_about_action)
        self.create_action("restart", self.on_restart_action)
        self.create_action("rules", self.on_rules_action)

        player_action = Gio.SimpleAction.new_stateful(
            "players",
            GLib.VariantType.new("s"),
            GLib.Variant("s", "singleplayer"),
        )
        player_action.connect("activate", self.on_players_changed)

        self.add_action(player_action)

    def on_players_changed(self, action, state):
        action.set_state(state)
        self.win.multiplayer = (
            False if state.get_string() == "singleplayer" else True
        )
        self.win.restart()

    def on_rules_action(self, *args):
        rules_dialog = Adw.Dialog(
            title=_("How to play"), content_width=500, content_height=500
        )
        toolbar_view = Adw.ToolbarView()
        rules_dialog.set_child(toolbar_view)
        headerbar = Adw.HeaderBar()
        toolbar_view.add_top_bar(headerbar)
        scrolled = Gtk.ScrolledWindow(vexpand=True)
        toolbar_view.set_content(scrolled)

        # Translators Note:
        # The following strings are to _( the rules page
        rules_text = (
            '<span font="16" weight="bold" rise="10000">'
            + _("Basic Rules")
            + "</span>\n"
            " • " + _("Two players:") + " <b>X</b> " + _("and") + " <b>O</b>\n"
            " • <b>X</b> " + _("goes first") + "\n"
            " • "
            + _(
                "Players take turns, aiming to win small boards and eventually the large board."
            )
            + "\n\n"
            '<span font="16" weight="bold" rise="10000">'
            + _("Gameplay")
            + "</span>\n"
            " 1. <b>X</b> "
            + _("starts by playing in")
            + " <i>"
            + _("any")
            + "</i> "
            + _("spot.")
            + "\n"
            " 2. "
            + _(
                "The next player plays in the small board matching the location of the previous move."
            )
            + "\n"
            "<i>"
            + _("Example:")
            + "</i> "
            + _("If")
            + " <b>X</b> "
            + _("plays in the top-right square of a small board,")
            + " <b>O</b> "
            + _("must play in the top-right small board of the large grid.")
            + "\n"
            " 3. "
            + _("This continues, with each move determining the next board.")
            + "\n\n"
            '<span font="16" weight="bold" rise="10000">'
            + _("Winning and Moves")
            + "</span>\n"
            " • "
            + _("Win a small board by following regular tic-tac-toe rules.")
            + "\n"
            " • "
            + _(
                "When a small board is won or filled, it cannot be played in again."
            )
            + "\n"
            " • "
            + _("If directed to a full board, you can play in")
            + " <i>"
            + _("any")
            + "</i> "
            + _("open board.")
            + "\n\n"
            '<span font="16" weight="bold" rise="10000">'
            + _("End of the Game")
            + "</span>\n"
            " • "
            + _(
                "A player wins by winning three small boards in a row (horizontally, vertically, or diagonally) on the large grid."
            )
            + "\n"
            " • "
            + _("If no legal moves remain, the game ends in a draw.")
            + "\n\n"
            + _("Have Fun!")
            + "\n"
        )

        scrolled.set_child(
            Gtk.Label(
                label=rules_text,
                use_markup=True,
                wrap=True,
                margin_start=12,
                margin_end=12,
                margin_top=12,
            )
        )

        rules_dialog.present(self.win)

    def on_restart_action(self, *args):
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

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(
            application_name=_("Ultimate Tic Tac Toe"),
            application_icon="io.github.nokse22.ultimate-tic-tac-toe",
            developer_name="Nokse",
            version="1.0.2",
            website="https://github.com/Nokse22/ultimate-tic-tac-toe",
            issue_url="https://github.com/Nokse22/ultimate-tic-tac-toe/issues",
            developers=["Nokse"],
            copyright="© 2023 Nokse",
        )
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
