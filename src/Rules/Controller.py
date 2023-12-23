from typing import List
from LinkedList import LinkedList  # Certifique-se de ter a classe LinkedList ou ajuste conforme necessário
from UnexpectedPieceException import UnexpectedPieceException
from IllegalMoveException import IllegalMoveException
from BoardOutOfBoundsException import BoardOutOfBoundsException

class Controller:
    @staticmethod
    def is_square_attacked(c, b):
        list_moves = Controller.uncheckedMoves(b)
        for i in range(8):
            for j in range(8):
                for a in list_moves[i][j]:
                    if a == c and not b.has_same_color(i, j, a[0], a[1]):
                        return True
        return False

    @staticmethod
    def is_square_defended(c, b):
        list_moves = Controller.uncheckedMoves(b)
        for i in range(8):
            for j in range(8):
                for a in list_moves[i][j]:
                    if a == c and b.has_same_color(i, j, a[0], a[1]):
                        return True
        return False

    @staticmethod
    def is_square_attacked_by_pieces(c_list, b, turn):
        list_moves = Controller.uncheckedMoves(b)
        for i in range(8):
            for j in range(8):
                if b.is_white(i, j) == turn:
                    for a in list_moves[i][j]:
                        if a == c_list[0] or a == c_list[1]:
                            return True
        return False
    
    def bishopGen(b, pos_i, pos_j):
        x = (0, 0)
        list_moves = []

        for i in range(1, 8):
            if (pos_i + i) < 8:
                if pos_j + i < 8 and b.getPiece(pos_i + i, pos_j + i) == 'o':
                    x = (pos_i + i, pos_j + i)
                    list_moves.append(x)
                else:
                    if pos_j + i < 8:
                        x = (pos_i + i, pos_j + i)
                        list_moves.append(x)
                    break

        for i in range(1, 8):
            if (pos_i + i) < 8:
                if pos_j - i >= 0 and b.getPiece(pos_i + i, pos_j - i) == 'o':
                    x = (pos_i + i, pos_j - i)
                    list_moves.append(x)
                else:
                    if pos_j - i >= 0:
                        x = (pos_i + i, pos_j - i)
                        list_moves.append(x)
                    break

        for i in range(1, pos_i + 1):
            if (pos_i - i) >= 0:
                if pos_j + i < 8 and b.getPiece(pos_i - i, pos_j + i) == 'o':
                    x = (pos_i - i, pos_j + i)
                    list_moves.append(x)
                else:
                    if pos_j + i < 8:
                        x = (pos_i - i, pos_j + i)
                        list_moves.append(x)
                    break

        for i in range(1, pos_i + 1):
            if (pos_i - i) >= 0:
                if (pos_j - i) >= 0 and b.getPiece(pos_i - i, pos_j - i) == 'o':
                    x = (pos_i - i, pos_j - i)
                    list_moves.append(x)
                else:
                    if (pos_j - i) >= 0:
                        x = (pos_i - i, pos_j - i)
                        list_moves.append(x)
                    break

        return list_moves


    def rookGen(b, pos_i, pos_j):
        moves = []
        x = (0, 0)
        path_blocked = False
        path_blocked2 = False
        t = 0

        for j in range(pos_j):
            if b.getPiece(pos_i, j) != 'o':
                path_blocked = True
                t = j

        if path_blocked:
            x = (pos_i, t)
            moves.append(x)

            for j in range(t + 1, pos_j):
                x = (pos_i, j)
                moves.append(x)
        else:
            for j in range(pos_j):
                x = (pos_i, j)
                moves.append(x)

        for j in range(pos_j + 1, 8):
            if b.getPiece(pos_i, j) == 'o':
                x = (pos_i, j)
                moves.append(x)
            else:
                x = (pos_i, j)
                moves.append(x)
                break

        for i in range(pos_i):
            if b.getPiece(i, pos_j) != 'o':
                path_blocked2 = True
                t = i

        if path_blocked2:
            x = (t, pos_j)
            moves.append(x)

            for i in range(t + 1, pos_i):
                x = (i, pos_j)
                moves.append(x)
        else:
            for i in range(pos_i):
                x = (i, pos_j)
                moves.append(x)

        for i in range(pos_i + 1, 8):
            if b.getPiece(i, pos_j) == 'o':
                x = (i, pos_j)
                moves.append(x)
            else:
                x = (i, pos_j)
                moves.append(x)
                break

        return moves

    @staticmethod
    def getPawnMoves(b, i, j):
        moves_p = []
        x = None

        if b.getPiece(i, j) == 'P':
            if 0 <= i - 1 < 8 and 0 <= j - 1 < 8 and b.getPiece(i - 1, j - 1) != 'o':
                x = (i - 1, j - 1)
                moves_p.append(x)

            if 0 <= i - 1 < 8 and 0 <= j + 1 < 8 and b.getPiece(i - 1, j + 1) != 'o':
                x = (i - 1, j + 1)
                moves_p.append(x)

            if 0 <= i - 1 < 8 and b.getPiece(i - 1, j) == 'o':
                x = (i - 1, j)
                moves_p.append(x)

            if 0 <= i - 2 < 8 and b.has_pawn_moved(i, j) is False and b.getPiece(i - 2, j) == 'o' and b.getPiece(i - 1, j) == 'o':
                x = (i - 2, j)
                moves_p.append(x)

        elif b.getPiece(i, j) == 'p':
            if 0 <= i + 1 < 8 and 0 <= j + 1 < 8 and b.getPiece(i + 1, j + 1) != 'o':
                x = (i + 1, j + 1)
                moves_p.append(x)

            if 0 <= i + 1 < 8 and 0 <= j - 1 < 8 and b.getPiece(i + 1, j - 1) != 'o':
                x = (i + 1, j - 1)
                moves_p.append(x)

            if 0 <= i + 1 < 8 and b.getPiece(i + 1, j) == 'o':
                x = (i + 1, j)
                moves_p.append(x)

            if 0 <= i + 2 < 8 and b.has_pawn_moved(i, j) is False and b.getPiece(i + 2, j) == 'o' and b.getPiece(i + 1, j) == 'o':
                x = (i + 2, j)
                moves_p.append(x)

        return moves_p

    def getRookMoves(b, pos_i, pos_j):
        moves = Controller.rookGen(b, pos_i, pos_j)
        return moves

    def getKnightMoves(b, pos_i, pos_j):
        moves_k = []
        x = (0, 0)
        adding_general_ = [-2, -1, -2, 1, 2, -1, 2, 1, -1, -2, -1, 2, 1, -2, 1, 2]

        for i in range(0, len(adding_general_), 2):
            if 0 <= (pos_i + adding_general_[i]) <= 7 and 0 <= (pos_j + adding_general_[i + 1]) <= 7:
                x = ((pos_i + adding_general_[i]), (pos_j + adding_general_[i + 1]))
                moves_k.append(x)

        return moves_k
    
    def getBishopMoves(b, pos_i, pos_j):
        return Controller.bishopGen(b, pos_i, pos_j)

    def getKingMoves(b, pos_i, pos_j):
        moves = []
        l = [1, -1, 0, 0, -1, 1, 1, -1]
        c = [0, 0, 1, -1, -1, 1, -1, 1]

        for k in range(len(l)):
            x = pos_i + l[k]
            y = pos_j + c[k]

            if not (0 <= x < 8 and 0 <= y < 8 and b.has_same_color(pos_i, pos_j, x, y)):
                continue

            moves.append((x, y))

        return moves

    def getQueenMoves(b, pos_i, pos_j):
        moves = []
        moves.append((-1, -1))
        moves = Controller.bishopGen(b, pos_i, pos_j)
        list_moves = Controller.rookGen(b, pos_i, pos_j)

        for c in list_moves:
            if c[0] != -1:
                moves.append(c)

        return moves


    @staticmethod
    def uncheckedMoves(b):
        list_moves = [[[] for _ in range(8)] for _ in range(8)]

        for i in range(8):
            for j in range(8):
                if b.getPiece(i, j) != 'o':
                    if b.getPiece(i, j) == 'P':
                        list_moves[i][j] = Controller.getPawnMoves(b, i, j)
                    elif b.getPiece(i, j) == 'C':
                        list_moves[i][j] = Controller.getKnightMoves(b, i, j)
                    elif b.getPiece(i, j) == 'B':
                        list_moves[i][j] = Controller.getBishopMoves(b, i, j)
                    elif b.getPiece(i, j) == 'T':
                        list_moves[i][j] = Controller.getRookMoves(b, i, j)
                    elif b.getPiece(i, j) == 'Q':
                        list_moves[i][j] = Controller.getQueenMoves(b, i, j)
                    elif b.getPiece(i, j) == 'K':
                        list_moves[i][j] = Controller.getKingMoves(b, i, j)
                    elif b.getPiece(i, j) == 'p':
                        list_moves[i][j] = Controller.getPawnMoves(b, i, j)
                    elif b.getPiece(i, j) == 'c':
                        list_moves[i][j] = Controller.getKnightMoves(b, i, j)
                    elif b.getPiece(i, j) == 'b':
                        list_moves[i][j] = Controller.getBishopMoves(b, i, j)
                    elif b.getPiece(i, j) == 't':
                        list_moves[i][j] = Controller.getRookMoves(b, i, j)
                    elif b.getPiece(i, j) == 'q':
                        list_moves[i][j] = Controller.getQueenMoves(b, i, j)
                    elif b.getPiece(i, j) == 'k':
                        list_moves[i][j] = Controller.getKingMoves(b, i, j)
                else:
                    list_moves[i][j] = []

        return list_moves


    @staticmethod
    def pass_pawn(b, i, j):
        list_moves = [[], []]

        if b.getLastMove()[0] is not None:
            if b.getPiece(i, j) == 'P' and i == 3:
                a1 = (1, j + 1)
                b1 = (1, j - 1)
                a2 = (3, j + 1)
                b2 = (3, j - 1)

                if 0 <= j + 1 < 8 and b.getLastMove()[0] == a1 and b.getLastMove()[1] == a2 and b.getPiece(2, j + 1) == 'o' and b.getPiece(3, j + 1) == 'p':
                    list_moves[0].append((2, j + 1))
                    list_moves[1].append((3, j + 1))

                if 0 <= j - 1 >= 0 and b.getLastMove()[0] == b1 and b.getLastMove()[1] == b2 and b.getPiece(2, j - 1) == 'o' and b.getPiece(3, j - 1) == 'p':
                    list_moves[0].append((2, j - 1))
                    list_moves[1].append((3, j - 1))

            elif b.getPiece(i, j) == 'p' and i == 4:
                a1 = (6, j + 1)
                b1 = (6, j - 1)
                a2 = (4, j + 1)
                b2 = (4, j - 1)

                if 0 <= j + 1 < 8 and b.getLastMove()[0] == a1 and b.getLastMove()[1] == a2 and b.getPiece(5, j + 1) == 'o' and b.getPiece(4, j + 1) == 'P':
                    list_moves[0].append((5, j + 1))
                    list_moves[1].append((4, j + 1))

                if 0 <= j - 1 >= 0 and b.getLastMove()[0] == b1 and b.getLastMove()[1] == b2 and b.getPiece(5, j - 1) == 'o' and b.getPiece(4, j - 1) == 'P':
                    list_moves[0].append((5, j - 1))
                    list_moves[1].append((4, j - 1))

        return list_moves
