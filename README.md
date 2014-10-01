bidding-tictactoe
=================

Tic-Tac-Toe:

Standard Tic-Tac-Toe is a 2-player game played on a 3*3 board in which players take alternate turns to mark the board with Xs and 0s. Any player who gets three Xs or three 0s in a line horizontally, vertically or diagonally wins the game. The result of the game for a player could be a win, loss or a tie.

Standard Tic-Tac-Toe possesses the following characteristics, which allow us to employ the Minimax algorithm to solve the game (i.e. find the next best possible move for a specific player):
a) Fully observable – perfect information game: Every player can completely observe the state of the game and knows the result of all previous moves. Also, there is at least one best way (not necessarily to win, but to minimize the losses) to play for each player. 
b) Deterministic: Players’ actions lead to predictable outcomes. i.e. there are no chaotic or unpredictable outcomes. 
c) Zero-sum: The utility values for the players at the end of the game are equal and opposite. If one player wins, the other player necessarily loses. 
d) Adversarial search problem: The opposing nature of the players’ utility functions makes the situation adversarial. Also, no plan exists that guarantees a win for a specific player regardless of the actions of his opponent. 

Bidding Tic-Tac-Toe:
  
Bidding Tic-Tac-Toe is standard tic-tac-toe with a gambling component. Both players will be given equal number of chips at the beginning of the game. Both players must bid number of chips to play. The bid will be a secret one i.e. both players will announce their bids simultaneously. The player who wins the bid gets the chance to move on the board, but has to give his chips to his opponent. In case of a tie, it will be broken randomly. Hence, tie breaking is not modeled in to the algorithm. 

Algorithms:

The 2 algorithms to implement Bidding Tic-Tac-Toe are: 
a) Bidding algorithm: Finding the best bid given the state of the board and the number  of chips possessed by each player. 
b) Moving algorithm: Finding the best move given the state of the board. 


Bidding algorithm:  

A search algorithm exploring all combination of bids is exponential and the size grows with the number of chips. The aim of the algorithm is that it must be a practical algorithm when the opponent player also plays strategically. The algorithm assumes that there is no optimal bidding algorithm because of the secret bid constraint. 

Moving algorithm:

The standard Minimax algorithm will fail in certain scenarios, primarily because of the following two reasons:   
a) No alternate play: Players don’t take turns alternately making moves on the board. So, Minimax is not optimal. 
b) Wrong utility values: In standard Tic-Tac-Toe, we solve the problem using minimax algorithm. The utility values associated with each move are 1, 0 or -1. i.e. each move is a winning move, losing move or a drawing move. But, the minimax approach does not work when we introduce bidding. Since bidding Tic-Tac-Toe is a non-deterministic game, the utility of the move has to be redefined. We need to introduce the utility of the state of the game for each player.  A utility value is associated with each line of the board, from which the utility for the player is calculated. 

Implementation:
Please see attached python files for implementation of standard Tic-Tac-Toe (basic.py) and bidding Tic-Tac-Toe (bidding_with_changing_utility.py)







