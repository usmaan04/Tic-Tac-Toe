class AI:
    def __init__(self, symbol, check_winner_func):
        self.symbol = symbol
        self.opponent_symbol = 'X' if symbol == 'O' else 'O'
        self.check_winner = check_winner_func

    def make_move(self, board):
        _, move = self.minimax(board, self.symbol)
        return move

    def minimax(self, board, player):
        winner = self.check_winner()

        if winner == self.symbol:
            return 1, None  # AI wins
        elif winner == self.opponent_symbol:
            return -1, None  # Opponent wins
        elif not any(' ' in row for row in board):
            return 0, None  # It's a draw

        moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = player
                    score, _ = self.minimax(board, self.opponent_symbol if player == self.symbol else self.symbol)
                    moves.append((score, (i, j)))
                    board[i][j] = ' '

        if player == self.symbol:
            best_move = max(moves, key=lambda x: x[0])
        else:
            best_move = min(moves, key=lambda x: x[0])

        return best_move




    
