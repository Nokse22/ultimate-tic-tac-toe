# window.py
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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib

import random
import time

class TacticsWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'TacticsWindow'

    label = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout_box = Gtk.Box(orientation=1)
        self.headerbar = Adw.HeaderBar(css_classes=["flat"])
        self.player_turn = Gtk.Label(label="Player 1", css_classes=["error", "label"], margin_start=6)
        self.headerbar.pack_start(self.player_turn)

        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu = Gio.Menu()

        section = Gio.Menu()
        section.append(_("Single player"), "app.singleplayer")
        section.append(_("Multiplayer"), "app.multiplayer")

        menu.append_section("Players", section)

        section = Gio.Menu()
        menu.append_section(None, section)

        section.append(_("Restart"), "app.restart")
        section.append(_("How to play"), "app.rules")
        section.append(_("Keyboard shortcuts"), "win.show-help-overlay")
        section.append(_("About Tactics"), "app.about")
        menu_button.set_menu_model(menu)
        self.headerbar.pack_end(menu_button)

        layout_box.append(self.headerbar)
        self.set_content(layout_box)
        self.set_title("Tactics")

        self.big_grid = Gtk.Grid(#width_request=300, height_request=300,
                column_homogeneous=True, row_homogeneous=True,
                column_spacing=2, row_spacing=2, css_classes=["big-grid"],
                halign=Gtk.Align.FILL, valign=Gtk.Align.CENTER, vexpand=True,
                margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
        self.clamp = Adw.Clamp()
        self.clamp.set_child(self.big_grid)
        layout_box.append(self.clamp)

        self.buttons = []

        for x in range(3):
            for y in range(3):
                grid = Gtk.Grid(name="", column_spacing=6, row_spacing=6, vexpand=True, hexpand=True, css_classes=["small-grid"])
                for g_x in range(3):
                    for g_y in range(3):
                        button = Gtk.Button(name=f"{x},{y},{g_x},{g_y}",
                                vexpand=True, hexpand=True,
                                width_request=50, height_request=50,
                                css_classes=["button"], label="")
                        button.connect("clicked", self.on_button_clicked)
                        grid.attach(button, g_x, g_y, 1, 1)
                        self.buttons.append(button)
                self.big_grid.attach(grid, x, y, 1, 1)

        self.player_sign = "X"
        self.multyplayer = False
        self.player_gen = self.player_number_generator()
        self.current_player = 1

        self.game_over = False

    def restart(self):
        for button in self.buttons:
            button.set_label("")
            button.remove_css_class("error")
            button.remove_css_class("accent")
            button.set_sensitive(True)

        for x in range(3):
            for y in range(3):
                grid = self.big_grid.get_child_at(x, y)
                grid.set_sensitive(True)
                grid.remove_css_class("won-1")
                grid.remove_css_class("won-2")
                grid.set_name("")

        if self.current_player == 1:
            self.current_player = next(self.player_gen)

        self.player_turn.set_label("Player 1")
        self.player_turn.remove_css_class("accent")
        self.player_turn.add_css_class("error")

        self.game_over = False

    def player_number_generator(self):
        player_number = 1
        while True:
            yield player_number
            player_number = 1 if player_number == 2 else 2

    def on_button_clicked(self, btn):
        self.select_button(btn)

        print(self.current_player, )

        if self.game_over:
            for x in range(3):
                for y in range(3):
                    grid = self.big_grid.get_child_at(x, y)
                    grid.set_sensitive(False)
            return

        if not self.multyplayer and self.current_player == 1:
            coordinates = btn.get_name().split(",")
            board_x = int(coordinates[2])
            board_y = int(coordinates[3])
            grid = self.big_grid.get_child_at(board_x, board_y)
            if grid.get_name() == "X" or grid.get_name() == "O":
                board = []
                for y in range(3):
                    row = []
                    for x in range(3):
                        play = self.big_grid.get_child_at(x, y).get_name()
                        if play == "X":
                            row.append(-1)
                        elif play == "O":
                            row.append(1)
                        elif play == "":
                            row.append(0)
                        print(play)
                    board.append(row)
                start = time.time()
                best_move = self.find_best_move(board)
                print(f"Best move: {best_move} in {time.time() - start}")
                grid = self.big_grid.get_child_at(best_move[1], best_move[0])

                if grid.get_name() == "X" or grid.get_name() == "O":
                    while grid.get_name() == "X" or grid.get_name() == "O":
                        board_x = random.randint(0, 2)
                        board_y = random.randint(0, 2)
                        grid = self.big_grid.get_child_at(board_x, board_y)

            board = []
            for y in range(3):
                row = []
                for x in range(3):
                    play = grid.get_child_at(x, y).get_label()
                    if play == "":
                        row.append(0)
                    elif play == "X":
                        row.append(-1)
                    elif play == "O":
                        row.append(1)
                board.append(row)
            start = time.time()
            best_move = self.find_best_move(board)
            print(f"Best move: {best_move} in {time.time() - start}")
            button = grid.get_child_at(best_move[1], best_move[0])
            self.select_button(button)

        if self.game_over:
            for x in range(3):
                for y in range(3):
                    grid = self.big_grid.get_child_at(x, y)
                    grid.set_sensitive(False)
            return

    def select_button(self, btn):
        self.current_player = next(self.player_gen)

        coordinates = btn.get_name().split(",")

        player_label = ""
        print(f"Current player: Player {self.current_player}")

        match self.current_player:
            case 1:
                player_label = "X"
                btn.set_label(player_label)
                btn.add_css_class("error")
            case 2:
                player_label = "O"
                btn.set_label(player_label)
                btn.add_css_class("accent")
        btn.set_sensitive(False)

        grid = self.big_grid.get_child_at(int(coordinates[0]), int(coordinates[1]))
        if self.check_win(grid, player_label):
            grid.set_sensitive(False)
            grid.add_css_class("won-"+str(self.current_player))
            grid.set_name(player_label)
            if self.big_check_win(player_label):
                self.game_over = True
                for x in range(3):
                    for y in range(3):
                        grid = self.big_grid.get_child_at(x, y)
                        grid.set_sensitive(False)
                        return

        for x in range(3):
            for y in range(3):
                grid = self.big_grid.get_child_at(x, y)
                grid.set_sensitive(False)

        active_grid_x = int(coordinates[2])
        active_grid_y = int(coordinates[3])

        grid = self.big_grid.get_child_at(active_grid_x, active_grid_y)
        style_context = grid.get_style_context()
        if not (style_context.has_class("won-1") or style_context.has_class("won-2")):
            grid.set_sensitive(True)
        else:
            for x in range(3):
                for y in range(3):
                    grid = self.big_grid.get_child_at(x, y)
                    style_context = grid.get_style_context()
                    if not (style_context.has_class("won-1") or style_context.has_class("won-2")):
                        grid.set_sensitive(True)

        match self.current_player:
            case 1:
                self.player_turn.set_label("Player 2")
                self.player_turn.remove_css_class("error")
                self.player_turn.add_css_class("accent")
            case 2:
                self.player_turn.set_label("Player 1")
                self.player_turn.remove_css_class("accent")
                self.player_turn.add_css_class("error")

    def check_win(self, grid, player_symbol):
        for row in range(3):
            if all(grid.get_child_at(col, row).get_label() == player_symbol for col in range(3)):
                return True

        for col in range(3):
            if all(grid.get_child_at(col, row).get_label() == player_symbol for row in range(3)):
                return True

        if all(grid.get_child_at(i, i).get_label() == player_symbol for i in range(3)) or \
           all(grid.get_child_at(i, 2 - i).get_label() == player_symbol for i in range(3)):
            return True

        return False

    def big_check_win(self, player_symbol):
        for row in range(3):
            if all(self.big_grid.get_child_at(col, row).get_name() == player_symbol for col in range(3)):
                return True

        for col in range(3):
            if all(self.big_grid.get_child_at(col, row).get_name() == player_symbol for row in range(3)):
                return True

        if all(self.big_grid.get_child_at(i, i).get_name() == player_symbol for i in range(3)) or \
           all(self.big_grid.get_child_at(i, 2 - i).get_name() == player_symbol for i in range(3)):
            return True

        return False

    def evaluate(self, board):
        # Check rows, columns, and diagonals for a win
        for row in board:
            if all(cell == row[0] and cell != 0 for cell in row):
                return row[0]

        for col in range(3):
            if all(board[row][col] == board[0][col] and board[row][col] != 0 for row in range(3)):
                return board[0][col]

        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
            return board[0][0]

        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
            return board[0][2]

        # Check for a draw
        if all(cell != 0 for row in board for cell in row):
            return 0

        # Game still ongoing
        return None

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        result = self.evaluate(board)

        if result is not None:
            return result - depth

        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 0:
                        board[row][col] = 1
                        score = self.minimax(board, depth + 1, alpha, beta, False)
                        board[row][col] = 0
                        best_score = max(best_score, score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] == 0:
                        board[row][col] = -1
                        score = self.minimax(board, depth + 1, alpha, beta, True)
                        board[row][col] = 0
                        best_score = min(best_score, score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def find_best_move(self, board):
        best_score = float('-inf')
        best_move = None

        if board == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]:
            return [random.randint(0, 2), random.randint(0, 2)]

        for row in range(3):
            for col in range(3):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = self.minimax(board, 0, float('-inf'), float('inf'), False)
                    board[row][col] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move
