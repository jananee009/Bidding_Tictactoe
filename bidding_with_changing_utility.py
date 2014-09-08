"""Games, or Adversarial Search. (Chapter 5)
"""
from utils import *
import random
#import ipdb; ipdb.set_trace()
from random import randint

class QueryPlayer:
    def __init__(self):
        self.chips = 10
        self.bidswon = 0
        self.offensive = False
        self.name = "query"
    def bid_value(self, player, game, state):
        num = 100
        while num > self.chips:
            num = num_or_str(raw_input('Your bid? '))
        return num
    def to_move(self):
        if self.first:
            return 'X'
        else:
            return 'O'
    def move(self, game, state, other_player):
        "Make a move by querying standard input."
        if self.bidswon >= other_player.bidswon:
            self.offensive = True
        else:
            self.offensive = False
        game.display(state)
        num = num_or_str(raw_input('Your move? '))
        first = math.ceil(float(num)/3)
        second = math.ceil(float(num)%3)
        if first == 0:
            first = 1
        if second == 0:
            second  = 3
        return (int(first), int(second))
    
class AlphaBetaPlayer:
    def __init__(self):
        self.chips = 10
        self.number_of_moves = 0
        self.bidswon = 0
        self.offensive = False
        self.name = "alphabeta"
        
    def bid_is_good(self, other_player, bid):
        if bid < (7*(self.chips)-other_player.chips+6)/8:
            return True
        return False

    def bid_value(self, player, game, state):
#       copy_state = copy.deepcopy(state)
#       copy_game = copy.deepcopy(game)
#       copy_otherplayer = copy.deepcopy(player)
#       offensive_copy = self.offensive
#       move = self.move(copy_game, copy_state, copy_otherplayer)
#       self.offensive = offensive_copy
#       copy_state.nextMover = self
#       copy_state = copy_game.result(copy_otherplayer, copy_state, move)
#       print "bid_Value" 
#       print copy_state
#       print "terminal state is " + str(copy_game.terminal_test(copy_state))
#      
        if self.bidswon > 2 or player.bidswon > 1:
            bid = min(self.chips, player.chips + 1)
            if self.bid_is_good(player, bid):
                return bid
        if self.bidswon > 0 and player.bidswon > self.bidswon and self.chips > 3*player.chips + 3:
            bid = player.chips + 1
            if self.bid_is_good(player, bid):
                return bid
        if self.bidswon == 0 and player.bidswon > self.bidswon and self.chips > 7*player.chips + 6:
            bid = player.chips + 1
            if self.bid_is_good(player, bid):
                return bid
        if self.number_of_moves >= 2:
            bid = (self.chips + 1)/2
            if self.bid_is_good(player, bid):
                return bid
        return randint(0, self.chips/3) + 1
       
    def to_move(self):
        try:
            if self.first:
                return 'X'
            else:
                return 'O'
        except AttributeError:
            print 'Not initialized'
            return 'X'
        
    def move(self, game, state, other_player):
        """Search game to determine best action; use alpha-beta pruning.
        As in [Fig. 5.7], this version searches all the way to the leaves."""

        
        if self.bidswon >= other_player.bidswon:
            self.offensive = True
        else:
            self.offensive = False

        utilities = []
        def max_value(state, other,alpha, beta, utilities):
            if game.terminal_test(state):
                util = game.utility(state, other)
                return if_(other.name == "alphabeta" and other.offensive == False, util, -util)
            v = -infinity
            for a in game.actions(state):
                sta = game.result(other,state, a)
                other = state.nextMover
                v = max(v, min_value(sta, other,alpha, beta, utilities))
                utilities.append((a, sta.utility))
                if v >= beta:
                    utilities.append(('\n', '\n'))
                    return v
                alpha = max(alpha, v)
            utilities.append(('\n', '\n'))
            return v

        def min_value(state, other, alpha, beta, utilities):
            if game.terminal_test(state):
                util = game.utility(state, other)
                return if_(other.name == "alphabeta" and other.offensive == False, -util, util)
            v = infinity
            for a in game.actions(state):
                sta = game.result(other,state, a)
                other = state.nextMover
                v = min(v, max_value(sta, other, alpha, beta, utilities))
                utilities.append((a, sta.utility))
                if v <= alpha:
                    utilities.append(('\n', '\n'))
                    return v
                beta = min(beta, v)
            utilities.append(('\n', '\n'))
            return v

        def dox(a, game, state, other, utilities):
            print a
            ret = min_value(game.result(other,state, a), state.nextMover,-infinity, infinity, utilities)
            #print ', '.join(str(x) + "-" + str(y) for x,y in utilities)
            utilities = []
            print ret
            return ret

            self.number_of_moves = self.number_of_moves + 1
        # Body of alphabeta_search:
        print "AlphaBeta"
        print "Offensive is " + str(self.offensive)
        ret = argmax(game.actions(state),
                      lambda a: dox(a, game, state, other_player, utilities))
        return ret

    
def bid_winner(player1, player2, game, state):
    print "player1 chips: " + str(player1.chips)
    print "player2 chips: " + str(player2.chips)
    bid1 = player1.bid_value(player2, game, state)
    bid2 = player2.bid_value(player1, game, state)
    print "bid 1 is " + str(bid1) + " and bid 2 is " + str(bid2)
    if bid1 > bid2:
        print "player 1 wins"
        player1.chips = player1.chips - bid1
        player2.chips = player2.chips + bid1
        return (player1, player2)
    else:
        print "player 2 wins"
        player2.chips = player2.chips - bid2
        player1.chips = player1.chips + bid2
        return (player2, player1)
    
def play_game(game, *players):
    """Play an n-person, move-alternating game.
    >>> play_game(Fig52Game(), alphabeta_player, alphabeta_player)
    3
    """
    state = game.initial
    players[0].first = True
    players[1].first = True
    firstMove = True
    while True:
        player, loser = bid_winner(players[0], players[1], game, state)
        player.bidswon = player.bidswon + 1 
        if firstMove == True:
            player.first = True
            loser.first = False
            firstMove = False
        state.nextMover = player
        move = player.move(game, copy.deepcopy(state), loser)
        state = game.result(loser, state, move)
        game.display(state)
        print state.utility
        if game.terminal_test(state):
            print "game over"
            game.display(state)
            return game.utility(state, 'X')


class TicTacToe():
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""
    
    def actions(self, state):
        "Legal moves are any square not yet taken."
        return state.moves

    def result(self, otherPlayer,state, move):
        if move not in state.moves:
            print "Illegal move"
            print move
            print state.moves
            return state # Illegal move has no effect
        board = state.board.copy(); board[move] = state.nextMover.to_move()
        moves = list(state.moves); moves.remove(move)
        return Struct(nextMover=otherPlayer,utility=self.compute_utility(board, move, state.nextMover), board=board, moves=moves)

    def utility(self, state, player):
        "Return the value to player; 1 for win, -1 for loss, 0 otherwise."
        return state.utility

    def terminal_test(self, state):
        "A state is terminal if it is won or there are no empty squares."
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h+1):
            for y in range(1, self.v+1):
                print board.get((x, y), '.'),
            print 

    def compute_utility(self, board, move, player):
        "If X wins with this move, return 1; if O return -1; else return 0."
        if (self.k_in_row(board, move, player.to_move() , (0, 1)) or
            self.k_in_row(board, move, player.to_move(), (1, 0)) or
            self.k_in_row(board, move, player.to_move(), (1, -1)) or
            self.k_in_row(board, move, player.to_move(), (1, 1))):
            return if_(player.offensive == True, +1, -1)
        else:
            return 0

    def to_move(self, state, player1, player2):
        "Return the player whose move it is in this state."
        winner = bid_winner(player1, player2, self, state)
        return winner.to_move 
   
    def __init__(self, h=3, v=3, k=3):
        update(self, h=h, v=v, k=k)
        moves = [(x, y) for x in range(1, h+1)
                 for y in range(1, v+1)]
        self.initial = Struct(nextMover = AlphaBetaPlayer(), utility=0, board={}, moves=moves)

    def k_in_row(self, board, move, player, (delta_x, delta_y)):
        "Return true if there is a line through move on board for player."
        x, y = move
        n = 0 # n is number of moves in row
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1 # Because we counted move itself twice
        return n >= self.k

player1 = AlphaBetaPlayer()
player2 = QueryPlayer()
play_game(TicTacToe(), player1, player2)










