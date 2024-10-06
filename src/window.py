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

import random
import time

from .player_id_enum import PlayerID
from .tic_tac_toe_grid import TicTacToeGrid

from gettext import gettext as _


@Gtk.Template(resource_path='/io/github/nokse22/ultimate-tic-tac-toe/ui/window.ui')
class UltimateTicTacToeWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'UltimateTicTacToeWindow'

    player_label = Gtk.Template.Child()
    field_grid = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player_sign = "X"
        self.multiplayer = False
        self.current_player = PlayerID.X

        self.game_over = False

        for x in range(3):
            for y in range(3):
                child = self.field_grid.get_child_at(x, y)
                child.x = x
                child.y = y

        self.restart()

    def restart(self):
        for x in range(3):
            for y in range(3):
                self.field_grid.get_child_at(x, y).reset()

        self.current_player = PlayerID.X

        if not self.multiplayer:
            self.player_label.set_visible(False)
        else:
            self.player_label.set_visible(True)

        self.player_label.set_label(_("Player") + " X")
        self.player_label.remove_css_class("player-o")
        self.player_label.add_css_class("player-x")

        self.game_over = False

    def next_player(self, player):
        match player:
            case PlayerID.X:
                return PlayerID.O
            case PlayerID.O:
                return PlayerID.X

    @Gtk.Template.Callback("on_button_clicked")
    def on_button_clicked(self, parent, btn):
        self.field_grid.get_child_at(parent.x, parent.y).set_sensitive(False)

        self.select_tile(parent, btn)

        self.current_player = self.next_player(self.current_player)

        if self.multiplayer:
            match self.current_player:
                case PlayerID.X:
                    self.player_label.set_label(_("Player") + " X")
                    self.player_label.add_css_class("player-x")
                    self.player_label.remove_css_class("player-o")
                case PlayerID.O:
                    self.player_label.set_label(_("Player") + " O")
                    self.player_label.add_css_class("player-o")
                    self.player_label.remove_css_class("player-x")

        if self.game_over:
            self.game_is_over()
            return

        if not self.multiplayer and self.current_player == PlayerID.O:
            next_grid = self.field_grid.get_child_at(btn.x, btn.y)

            # If the next grid is won of full it will select the best next board
            #       where to play to win the big game

            print(f"next grid is won by {next_grid.won_by}")

            if next_grid.won_by in [PlayerID.X, PlayerID.O, PlayerID.F]:
                board = self.get_field_grid_board()
                if board is not None:
                    start = time.time()
                    best_move = self.find_best_move(board)
                    print(f"Best move: {best_move} in {time.time() - start}")
                    next_grid = self.field_grid.get_child_at(best_move[1], best_move[0])

                # If the selected move is already played or is full it will select a
                #       new board to play at random

                if next_grid.won_by in [PlayerID.X, PlayerID.O, PlayerID.F]:
                    while next_grid.won_by in [PlayerID.X, PlayerID.O, PlayerID.F]:
                        board_x = random.randint(0, 2)
                        board_y = random.randint(0, 2)
                        next_grid = self.field_grid.get_child_at(board_x, board_y)
                        print(next_grid.won_by)

            # Once the new board to play is set it will find the best move for
            #       this board and select it

            board = self.get_small_grid_board(next_grid)
            start = time.time()
            best_move = self.find_best_move(board)
            print(f"Best move: {best_move} in {time.time() - start}")
            button = next_grid.get_child_at(best_move[1], best_move[0])
            self.select_tile(next_grid, button)
            self.current_player = self.next_player(self.current_player)

        if self.game_over:
            self.game_is_over()

    def get_small_grid_board(self, small_grid):
        board = []
        for y in range(3):
            row = []
            for x in range(3):
                played = small_grid.get_child_at(x, y).played_by
                if played == PlayerID.N:
                    row.append(0)
                elif played == PlayerID.X:
                    row.append(-1)
                elif played == PlayerID.O:
                    row.append(1)
            board.append(row)
        return board

    def get_field_grid_board(self):
        board = []
        for y in range(3):
            row = []
            for x in range(3):
                play = self.field_grid.get_child_at(x, y).won_by
                if play == PlayerID.X:
                    row.append(-1)
                elif play == PlayerID.O:
                    row.append(1)
                elif play == PlayerID.N:
                    row.append(0)
                elif play == PlayerID.F:
                    return None
            board.append(row)
        return board

    def game_is_over(self):
        for x in range(3):
            for y in range(3):
                grid = self.field_grid.get_child_at(x, y)
                grid.set_sensitive(False)
        return

    def select_tile(self, parent, btn):
        print(f"Current player: Player {self.current_player}")

        btn.set_played_by(self.current_player)

        # Check if the just played board has been won of is full

        played_grid = self.field_grid.get_child_at(parent.x, parent.y)
        state = self.check_win(played_grid, self.current_player)
        if state is None:  # Board is full
            played_grid.set_sensitive(False)
            played_grid.won_by = PlayerID.F

        elif state:  # Board has been won

            # Check if the big game has been won

            played_grid.won(self.current_player)
            state = self.big_check_win(self.current_player)
            if state is None:  # Full -> Tie
                self.game_over = True
                toast = Adw.Toast(
                    title=_("It's a tie"),
                    button_label=_("Restart"),
                    action_name="app.restart")
                self.toast_overlay.add_toast(toast)
                self.set_all_sensitivity(False)
                return
            elif state:  # Won by the current player
                self.game_over = True
                if self.multiplayer:
                    player = "X" if self.current_player == PlayerID.X else "O"
                    toast = Adw.Toast(
                        title=_("Player") + " " + player + " " + _("won"),
                        button_label=_("Restart"),
                        action_name="app.restart")
                elif self.current_player == PlayerID.O:
                    toast = Adw.Toast(
                        title=_("You lost!"),
                        button_label=_("Restart"),
                        action_name="app.restart")
                else:
                    toast = Adw.Toast(
                        title=_("You won!"),
                        button_label=_("Restart"),
                        action_name="app.restart")

                self.toast_overlay.add_toast(toast)
                self.set_all_sensitivity(False)
                return

        self.set_all_sensitivity(False)

        # Get the new board where to play and if it's not been won it is set
        #       as sensitive to play, but if it's won or full it will set
        #       all boards as playable

        next_grid = self.field_grid.get_child_at(btn.x, btn.y)
        if next_grid.won_by not in [PlayerID.X, PlayerID.O, PlayerID.F]:
            next_grid.set_sensitive(True)
        else:
            for x in range(3):
                for y in range(3):
                    next_grid = self.field_grid.get_child_at(x, y)
                    if next_grid.won_by not in [PlayerID.X, PlayerID.O, PlayerID.F]:
                        next_grid.set_sensitive(True)

    def check_win(self, grid, player):
        for row in range(3):
            if all(grid.get_child_at(col, row).played_by == player for col in range(3)):
                return True

        for col in range(3):
            if all(grid.get_child_at(col, row).played_by == player for row in range(3)):
                return True

        if all(grid.get_child_at(i, i).played_by == player for i in range(3)) or \
           all(grid.get_child_at(i, 2 - i).played_by == player for i in range(3)):
            return True

        full = True
        for x in range(3):
            for y in range(3):
                if grid.get_child_at(x, y).played_by == PlayerID.N:
                    full = False
        if full:
            return None

        return False

    def set_all_sensitivity(self, sens):
        for x in range(3):
            for y in range(3):
                grid = self.field_grid.get_child_at(x, y)
                grid.set_sensitive(sens)

    def big_check_win(self, player):
        print(f"Checking win for {player}")
        for row in range(3):
            if all(self.field_grid.get_child_at(col, row).won_by == player for col in range(3)):
                return True

        for col in range(3):
            if all(self.field_grid.get_child_at(col, row).won_by == player for row in range(3)):
                return True

        if all(self.field_grid.get_child_at(i, i).won_by == player for i in range(3)) or \
           all(self.field_grid.get_child_at(i, 2 - i).won_by == player for i in range(3)):
            return True

        full = True
        for x in range(3):
            for y in range(3):
                if self.field_grid.get_child_at(x, y).won_by == PlayerID.N:
                    full = False
        if full:
            return None

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
                        score = self.minimax(
                            board, depth + 1, alpha, beta, False)
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
                        score = self.minimax(
                            board, depth + 1, alpha, beta, True)
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
                    score = self.minimax(
                        board, 0, float('-inf'), float('inf'), False)
                    board[row][col] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move
