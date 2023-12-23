from copy import deepcopy
from Controller import Controller
from UnexpectedPieceException import UnexpectedPieceException
from IllegalMoveException import IllegalMoveException
from BoardOutOfBoundsException import BoardOutOfBoundsException

class Game:
    def __init__(self, board):
        self.board = board
        self.stateBoard = [[[] for _ in range(8)] for _ in range(8)]
        self.passBoard = [[[] for _ in range(8)] for _ in range(8)]

        for i in range(8):
            for j in range(8):
                self.stateBoard[i][j] = []
                self.passBoard[i][j] = []

    def clone(self):
        b = self.board.clone()
        game = Game(b)

        for i in range(8):
            for j in range(8):
                game.stateBoard[i][j] = deepcopy(self.stateBoard[i][j])
                game.passBoard[i][j] = deepcopy(self.passBoard[i][j])

        return game

    def equals(self, g):
        return self.board.equals(g.board)

    def getBoard(self):
        return self.board

    def getPassBoard(self):
        return self.passBoard

    def hasEnded(self):
        return self.board.endOfGame

    def move(self, i, j, final_i, final_j):
        c = (final_i, final_j)
        if self.isLegal(i, j, c) and (not self.board.isBlack(i, j) == self.board.turn or self.board.isWhite(i, j) == self.board.turn):
            if i == 7 and j == 4 and final_i == 7 and final_j == 2:
                self.board.changePos(i, j, c[0], c[1])
                self.board.changePos(7, 0, (7, 3))
                self.board.turn = not self.board.turn
                self.board.hasWhiteCastled = True
            elif i == 7 and j == 4 and final_i == 7 and final_j == 6:
                self.board.changePos(i, j, c[0], c[1])
                self.board.changePos(7, 7, (7, 5))
                self.board.hasWhiteCastled = True
                self.board.turn = not self.board.turn
            elif i == 0 and j == 4 and final_i == 0 and final_j == 2:
                self.board.changePos(i, j, c[0], c[1])
                self.board.changePos(0, 0, (0, 3))
                self.board.hasBlackCastled = True
                self.board.turn = not self.board.turn
            elif i == 0 and j == 4 and final_i == 0 and final_j == 6:
                self.board.changePos(i, j, c[0], c[1])
                self.board.changePos(0, 7, (0, 5))
                self.board.hasBlackCastled = True
                self.board.turn = not self.board.turn
            else:
                self.board.changePos(i, j, c[0], c[1])
                self.board.turn = not self.board.turn

            self.board.setLastMove(i, j, final_i, final_j)
        elif self.isEnPassantLegal(i, j, c) and self.board.isWhite(i, j) == self.board.turn:
            self.board.changePos(i, j, c[0], c[1])
            self.board.eliminate(i, c.pos_j)
            self.board.turn = not self.board.turn
        else:
            raise IllegalMoveException("Movimento ilegal")

    def allLegal(self):
        list_ = Controller.uncheckedMoves(self.board)

        for i in range(8):
            for j in range(8):
                if self.board.isApiece(i, j) and (self.board.isWhite(i, j) == self.board.turn):
                    teste = list_[i][j]
                    letra = deepcopy(teste)

                    for c in teste:
                        copy = self.board.clone()
                        copy.changePos(i, j, c[0], c[1])

                        if self.board.turn:
                            if self.board.hasSameColor(i, j, c[0], c[1]):
                                letra.remove(c)
                            elif copy.isWhiteKingInCheck():
                                letra.remove(c)
                        else:
                            if self.board.hasSameColor(i, j, c[0], c[1]):
                                letra.remove(c)
                            if copy.isBlackKingInCheck():
                                letra.remove(c)

                    list_[i][j] = letra
                else:
                    list_[i][j] = []

        self.stateBoard = list_

        if self.board.turn:
            self.WhitesCastling()
        else:
            self.BlacksCastling()

        self.legalEnPassant()
        self.getHasBlackKingMoved()
        self.getHasBlackLeftRookMoved()
        self.getHasBlackRightRookMoved()
        self.getHasWhiteKingMoved()
        self.getHasWhiteLeftRookMoved()
        self.getHasWhiteRightRookMoved()

    def legalEnPassant(self):
        if self.board.turn:
            for j in range(8):
                self.passBoard[3][j] = Controller.pass_pawn(self.board, 3, j)[0]

            for j in range(8):
                to_remove = []
                for c in self.passBoard[3][j]:
                    copy = self.board.clone()
                    copy.changePos(3, j, c)
                    copy.eliminate(3, c.pos_j)
                    if copy.isWhiteKingInCheck():
                        to_remove.append(c)

                for c in to_remove:
                    self.passBoard[3][j].remove(c)
        else:
            for j in range(8):
                self.passBoard[4][j] = Controller.pass_pawn(self.board, 4, j)[0]

            for j in range(8):
                to_remove = []
                for c in self.passBoard[4][j]:
                    copy = self.board.clone()
                    copy.changePos(4, j, c)
                    copy.eliminate(4, c.pos_j)
                    if copy.isBlackKingInCheck():
                        to_remove.append(c)

                for c in to_remove:
                    self.passBoard[4][j].remove(c)

    def isLegal(self, i, j, c):
        for x in self.stateBoard[i][j]:
            if x[0] == c[0] and x[1] == c[1]:
                return True

        return False

    def isEnPassantLegal(self, i, j, c):
        if i == 3 and self.board.turn:
            for x in self.passBoard[i][j]:
                if x.pos_i == c.pos_i and x.pos_j == c.pos_j:
                    return True
        elif i == 4 and not self.board.turn:
            for x in self.passBoard[i][j]:
                if x.pos_i == c.pos_i and x.pos_j == c.pos_j:
                    return True

        return False

    def getStateBoard(self):
        return self.stateBoard

    def isCheckMateWhite(self):
        legal = 0

        if self.board.isWhiteKingInCheck():
            for i in range(8):
                for j in range(8):
                    x = iter(self.stateBoard[i][j])

                    while True:
                        try:
                            c = next(x)
                            copy = self.board.clone()
                            copy.copy.changePos(i, j, c[0], c[1])

                            if not copy.isWhiteKingInCheck():
                                legal += 1

                        except StopIteration:
                            break

                        if legal != 0:
                            break

                if legal != 0:
                    break

            if legal == 0:
                self.board.endOfGame = True
                self.board.isCheckmateWhite = True

    def isCheckMateBlack(self):
        legal = 0

        if self.board.isBlackKingInCheck():
            for i in range(8):
                for j in range(8):
                    x = iter(self.stateBoard[i][j])

                    while True:
                        try:
                            c = next(x)
                            copy = self.board.clone()
                            copy.copy.changePos(i, j, c[0], c[1])

                            if not copy.isBlackKingInCheck():
                                legal += 1

                        except StopIteration:
                            break

                        if legal != 0:
                            break

                if legal != 0:
                    break

            if legal == 0:
                self.board.endOfGame = True
                self.board.isCheckmateBlack = True

    def isBlackPromotion(self):
        ourBoard = self.board.getBoard()
        for i in range(len(ourBoard[7])):
            if ourBoard[7][i] == 'p':
                ourBoard[7][i] = 'q'

    def isWhitePromotion(self):
        ourBoard = self.board.getBoard()
        for i in range(len(ourBoard[0])):
            if ourBoard[0][i] == 'P':
                ourBoard[0][i] = 'Q'

    def getHasBlackKingMoved(self):
        ourBoard = self.board.getBoard()
        if ourBoard[0][4] == 'o':
            self.board.hasBlackKingMoved = True

    def getHasWhiteKingMoved(self):
        ourBoard = self.board.getBoard()
        if ourBoard[7][4] == 'o':
            self.board.hasWhiteKingMoved = True

    def getHasWhiteLeftRookMoved(self):
        ourBoard = self.board.getBoard()
        if ourBoard[7][0] == 'o':
            self.board.hasLeftWhiteRookMoved = True

    def getHasWhiteRightRookMoved(self):
        ourBoard = self.board.getBoard()
        if ourBoard[7][7] != 'T':
            self.board.hasRightWhiteRookMoved = True

    def getHasBlackLeftRookMoved(self):
        ourBoard = self.board.getBoard()
        if ourBoard[0][0] != 't':
            self.board.hasLeftBlackRookMoved = True

    def getHasBlackRightRookMoved(self):
        ourBoard = self.board.getBoard()
        if ourBoard[0][7] == 'o':
            self.board.hasRightBlackRookMoved = True

    def BlacksCastling(self):
        if not self.board.hasBlackKingMoved and not self.board.hasLeftBlackRookMoved and \
           (self.board.getPiece(0, 3) == 'o') and (self.board.getPiece(0, 2) == 'o') and (self.board.getPiece(0, 1) == 'o'):
            c = [(0, 3), (0, 2)]
            if Controller.isSquareAttacked(c, self.board, self.board.turn):
                self.stateBoard[0][4].append((0, 2))

        if not self.board.hasBlackKingMoved and not self.board.hasRightBlackRookMoved and \
           (self.board.getPiece(0, 5) == 'o') and (self.board.getPiece(0, 6) == 'o'):
            c = [(0, 5), (0, 6)]
            if Controller.isSquareAttacked(c, self.board, self.board.turn):
                self.stateBoard[0][4].append((0, 6))

    def WhitesCastling(self):
        if not self.board.hasWhiteKingMoved and not self.board.hasLeftWhiteRookMoved and \
           (self.board.getPiece(7, 3) == 'o') and (self.board.getPiece(7, 2) == 'o') and (self.board.getPiece(7, 1) == 'o'):
            c = [(7, 3), (7, 2)]
            if Controller.isSquareAttacked(c, self.board, self.board.turn):
                self.stateBoard[7][4].append((7, 2))

        if not self.board.hasWhiteKingMoved and not self.board.hasRightWhiteRookMoved and \
           (self.board.getPiece(7, 5) == 'o') and (self.board.getPiece(7, 6) == 'o'):
            c = [(7, 5), (7, 6)]
            if Controller.isSquareAttacked(c, self.board, self.board.turn):
                self.stateBoard[7][4].append((7, 6))
