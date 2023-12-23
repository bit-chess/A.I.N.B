from Controller import Controller
from UnexpectedPieceException import UnexpectedPieceException
from IllegalMoveException import IllegalMoveException
from BoardOutOfBoundsException import BoardOutOfBoundsException

class Board:
    def __init__(self):
        self.chessBoard = [['o' for _ in range(8)] for _ in range(8)]
        self.initPosBlack = ['t', 'c', 'b', 'q', 'k', 'b', 'c', 't']
        self.initPosWhite = ['T', 'C', 'B', 'Q', 'K', 'B', 'C', 'T']

        self.hasWhiteKingMoved = False
        self.hasRightWhiteRookMoved = False
        self.hasLeftWhiteRookMoved = False
        self.hasBlackKingMoved = False
        self.hasRightBlackRookMoved = False
        self.hasLeftBlackRookMoved = False
        self.endOfGame = False
        self.isCheckmateWhite = False
        self.isCheckmateBlack = False
        self.turn = True
        self.hasBlackCastled = False
        self.hasWhiteCastled = False
        self.lastMove = [None, None]

        for i in range(8):
            self.chessBoard[1][i] = 'p'
            self.chessBoard[6][i] = 'P'
            self.chessBoard[0][i] = self.initPosBlack[i]
            self.chessBoard[7][i] = self.initPosWhite[i]

    def clone(self):
        b = Board()
        b.chessBoard = [row[:] for row in self.chessBoard]
        b.hasBlackKingMoved = self.hasBlackKingMoved
        b.hasRightWhiteRookMoved = self.hasRightWhiteRookMoved
        b.hasLeftWhiteRookMoved = self.hasLeftWhiteRookMoved
        b.hasWhiteKingMoved = self.hasWhiteKingMoved
        b.hasRightBlackRookMoved = self.hasRightBlackRookMoved
        b.hasLeftBlackRookMoved = self.hasLeftBlackRookMoved
        b.hasWhiteCastled = self.hasWhiteCastled
        b.hasBlackCastled = self.hasBlackCastled
        b.endOfGame = self.endOfGame
        b.isCheckmateBlack = self.isCheckmateBlack
        b.isCheckmateWhite = self.isCheckmateWhite
        b.turn = self.turn

        return b

    def eliminate(self, i, j):
        self.chessBoard[i][j] = 'o'

    def equals(self, other_board):
        for i in range(8):
            for j in range(8):
                if other_board.chessBoard[i][j] != self.chessBoard[i][j]:
                    return False
        return other_board.turn == self.turn

    def isWhite(self, pos_i, pos_j):
        return self.chessBoard[pos_i][pos_j].isupper()

    def isBlack(self, pos_i, pos_j):
        return self.chessBoard[pos_i][pos_j].islower() and self.chessBoard[pos_i][pos_j] != 'o'

    def isWhite_piece(self, piece):
        return piece.isupper()

    def isBlack_piece(self, piece):
        return piece.islower() and piece != 'o'

    def has_same_color(self, me_i, me_j, that_piece_i, that_piece_j):
        return ((self.isBlack(me_i, me_j) and self.isBlack(that_piece_i, that_piece_j)) or
                (self.isWhite(me_i, me_j) and self.isWhite(that_piece_i, that_piece_j)))

    def changePos(self, begin_x, begin_y, final_x, final_y):
        self.set_change(begin_x, begin_y, final_x, final_y)

    def set_change(self, begin_x, begin_y, final_x, final_y):
        if self.chessBoard[final_x][final_y] not in ('K', 'k') and 0 <= begin_x < 8 and 0 <= begin_y < 8:
            self.chessBoard[final_x][final_y] = self.chessBoard[begin_x][begin_y]
            self.chessBoard[begin_x][begin_y] = 'o'

    def getPiece(self, pos_x, pos_y):
        return self.chessBoard[pos_x][pos_y]

    def isWhite_king_in_check(self):
        unchecked_moves = Controller.uncheckedMoves(self)
        king = self.index_of_piece('K')[0]
        for i in range(8):
            for j in range(8):
                if self.isBlack(i, j):
                    for c in unchecked_moves[i][j]:
                        if c == king:
                            return True
        return False

    def isBlackKingInCheck(self):
        unchecked_moves = Controller.uncheckedMoves(self)
        king = self.index_of_piece('k')[0]
        for i in range(8):
            for j in range(8):
                if self.isWhite(i, j):
                    for c in unchecked_moves[i][j]:
                        if c == king:
                            return True
        return False

    def set_board(self, board):
        self.chessBoard = board

    def getBoard(self):
        return self.chessBoard

    def index_of_piece(self, piece):
        positions = [None] * 10
        p = 0

        for i in range(8):
            for j in range(8):
                if self.chessBoard[i][j] == piece:
                    positions[p] = (i, j)
                    p += 1

        return positions

    def isApiece(self, pos_i, pos_j):
        return self.getPiece(pos_i, pos_j) != 'o'

    def promotionWhite(self):
        for j in range(8):
            if self.getPiece(7, j) == 'P':
                return (7, j)
        return (-1, -1)

    def promotionBlack(self):
        for j in range(8):
            if self.getPiece(0, j) == 'P':
                return (0, j)
        return (-1, -1)

    def setLastMove(self, i, j, a, b):
        self.lastMove = [(i, j), (a, b)]

    def getLastMove(self):
        return self.lastMove

    def printImage(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        numbers = [8, 7, 6, 5, 4, 3, 2, 1]
        for i in range(8):
            for j in range(8):
                print(self.chessBoard[i][j], end="")
            print(" ", numbers[i])
        print()
        for i in range(8):
            print(letters[i], end="")
        print()

    def has_pawn_moved(self, pos_i, pos_j):
        piece = self.getPiece(pos_i, pos_j)
        if piece not in ['p', 'P']:
            raise UnexpectedPieceException("Board.hasPawnMoved foi chamado em uma casa que não contém um peão")
        elif piece == 'p' and pos_i == 1:
            return False
        elif piece == 'P' and pos_i == 6:
            return False
        else:
            return True

    def isBlackKingInCheck(self):
        list_moves = Controller.uncheckedMoves(self)
        king = self.index_of_piece('k')[0]
        for i in range(8):
            for j in range(8):
                if self.isWhite(i, j):
                    for c in list_moves[i][j]:
                        if c == king:
                            return True
        return False

    def isWhiteKingInCheck(self):
        list_moves = Controller.uncheckedMoves(self)
        king = self.index_of_piece('K')[0]
        for i in range(8):
            for j in range(8):
                if self.isBlack(i, j):
                    for c in list_moves[i][j]:
                        if c == king:
                            return True
        return False

    def set_board(self, board):
        self.chessBoard = board

    def getBoard(self):
        return self.chessBoard

    def index_of_piece(self, b):
        positions = [None] * 10
        p = 0

        for i in range(8):
            for j in range(8):
                if self.chessBoard[i][j] == b:
                    positions[p] = (i, j)
                    p += 1
        return positions

    def isApiece(self, pos_i, pos_j):
        return self.getPiece(pos_i, pos_j) != 'o'

    def promotionWhite(self):
        for j in range(8):
            if self.getPiece(7, j) == 'P':
                return (7, j)
        return (-1, -1)

    def promotionBlack(self):
        for j in range(8):
            if self.getPiece(0, j) == 'P':
                return (0, j)
        return (-1, -1)

    def get_turn(self):
        return self.turn

    def setLastMove(self, i, j, a, b):
        self.lastMove[0] = (i, j)
        self.lastMove[1] = (a, b)

    def getLastMove(self):
        return self.lastMove
