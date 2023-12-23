import sys

sys.path.append('../Rules')
from Board import Board 
from BoardOutOfBoundsException import BoardOutOfBoundsException
from Controller import Controller
from UnexpectedPieceException import UnexpectedPieceException


class Evaluate:
    def __init__(self, board):
        self.board = board

    def piece(self):
        white = 0
        black = 0
        for i in range(8):
            for j in range(8):
                if self.board.isWhite(i, j):
                    if self.board.getPiece(i, j) == 'P':
                        white += 1
                    elif self.board.getPiece(i, j) == 'Q':
                        white += 9
                    elif self.board.getPiece(i, j) == 'T':
                        white += 5
                    elif self.board.getPiece(i, j) == 'B':
                        white += 3.5
                    elif self.board.getPiece(i, j) == 'C':
                        white += 3
                else:
                    if self.board.getPiece(i, j) == 'p':
                        black += 1
                    elif self.board.getPiece(i, j) == 'q':
                        black += 9
                    elif self.board.getPiece(i, j) == 't':
                        black += 5
                    elif self.board.getPiece(i, j) == 'b':
                        black += 3.5
                    elif self.board.getPiece(i, j) == 'c':
                        black += 3
        return white - black

    def kingSafety(self):
        white = 0
        black = 0
        for i in range(8):
            for j in range(8):
                if self.board.getPiece(i, j) == 'K':
                    safe_white = Controller.getQueenMoves(self.board, i, j)
                    white = -len(safe_white) ** 0.5
                if self.board.getPiece(i, j) == 'k':
                    safe_black = Controller.getQueenMoves(self.board, i, j)
                    black = -len(safe_black) ** 0.5
        return white - black

    def pieceSafety(self):
        white = 0
        black = 0
        for i in range(8):
            for j in range(8):
                if self.board.isBlack(i, j) and Controller.isSquareDefended((i, j), self.board):
                    if self.board.getPiece(i, j) in ['b', 't', 'c']:
                        black += 1
                    elif self.board.getPiece(i, j) == 'p':
                        black += 0.3
                if self.board.isWhite(i, j) and Controller.isSquareDefended((i, j), self.board):
                    if self.board.getPiece(i, j) in ['B', 'T', 'C']:
                        white += 1
                    elif self.board.getPiece(i, j) == 'P':
                        white += 0.3
        return white - black

    def kingMobility(self):
        white = 0
        black = 0
        white_king = self.board.indexOfPiece('K')
        black_king = self.board.indexOfPiece('k')
        list_white = Controller.getKingMoves(self.board, white_king[0][0], white_king[0][1])
        list_black = Controller.getKingMoves(self.board, black_king[0][0], black_king[0][1])
        white = len(list_white) ** 0.5
        black = len(list_black) ** 0.5
        return white - black

    def pawnAdvancement(self):
        white = 0
        black = 0
        list_white = self.board.indexOfPiece('P')
        list_black = self.board.indexOfPiece('p')
        for c in list_white:
            if c is not None:
                i = c[0]
                if i != 7:
                    white += (7 - (i + 1)) * 0.2
        for c in list_black:
            if c is not None:
                i = c[0]
                black += (i - 1) * 0.2
        return white - black

    def pieceMobility(self):
        white = 0
        black = 0
        for i in range(8):
            for j in range(8):
                if self.board.isWhite(i, j):
                    if self.board.getPiece(i, j) == 'T':
                        white += len(Controller.getRookMoves(self.board, i, j)) ** 0.5 / 2
                    elif self.board.getPiece(i, j) == 'B':
                        white += len(Controller.getBishopMoves(self.board, i, j)) ** 0.5 / 2
                    elif self.board.getPiece(i, j) == 'C':
                        white += len(Controller.getKnightMoves(self.board, i, j)) ** 0.5 / 2
                else:
                    if self.board.getPiece(i, j) == 't':
                        black += len(Controller.getRookMoves(self.board, i, j)) ** 0.5 / 2
                    elif self.board.getPiece(i, j) == 'b':
                        black += len(Controller.getBishopMoves(self.board, i, j)) ** 0.5 / 2
                    elif self.board.getPiece(i, j) == 'c':
                        black += len(Controller.getKnightMoves(self.board, i, j)) ** 0.5 / 2
        return white - black

    def castlePoints(self):
        white = 0
        black = 0
        if self.board.hasWhiteCastled:
            white += 1.5
        if self.board.hasBlackCastled:
            black += 1.5
        return white - black

    def total(self):
        return (
            self.kingMobility() +
            self.pieceSafety() +
            self.piece() +
            self.kingSafety() +
            self.pawnAdvancement() +
            self.pieceMobility() +
            self.castlePoints()
        )

