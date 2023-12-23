import sys

sys.path.append('../Rules')
from Board import Board 
from BoardOutOfBoundsException import BoardOutOfBoundsException
from Controller import Controller
from UnexpectedPieceException import UnexpectedPieceException
from Game import Game

from typing import List

from GraphBuilder import GraphBuilder
from Evaluate import Evaluate

class AlphaBeta:
    def __init__(self, board):
        self.board = board
        self.gb = GraphBuilder()
        self.gb.createGraph(board)

    def getGraph(self):
        return self.gb

    def createSon(self, h):
        b = self.gb.getBoard(h)
        g = Game(b)
        g.allLegal()

        son_list = []
        for i in range(8):
            for j in range(8):
                for c in g.getStateBoard()[i][j]:
                    if c is None:
                        continue
                    copy = g.clone()
                    if b.getTurn() == b.isWhite(i, j) and b.isApiece(i, j):
                        copy.move(i, j, c[0], c[1])
                        copy.isCheckMateBlack()
                        copy.isCheckMateWhite()
                        son_list.append(copy.getBoard())

                for c in g.getPassBoard()[i][j]:
                    if c is None:
                        continue
                    copy = g.clone()
                    if b.getTurn() == b.isWhite(i, j) and b.isApiece(i, j):
                        copy.move(i, j, c[0], c[1])
                        copy.isCheckMateBlack()
                        copy.isCheckMateWhite()
                        son_list.append(copy.getBoard())

        if son_list:
            self.gb.create_graph(h, son_list)

    def algorithm(self, node: int, depth: int, a: float, b: float, is_maximizing: bool) -> float:
        if depth == 0:
            if self.gb.getBoard(node).isCheckMateBlack:
                self.gb.setWeight(node, float('inf'))
            elif self.gb.getBoard(node).isCheckMateWhite:
                self.gb.setWeight(node, float('-inf'))
            else:
                e = Evaluate(self.gb.getBoard(node))
                self.gb.setWeight(node, e.total())
            return self.gb.getWeight(node)
        elif is_maximizing:
            value = float('-inf')
            self.createSon(node)
            for child in self.gb.getSon(node):
                value = max(value, self.algorithm(child, depth - 1, a, b, False))
                a = max(a, value)
                if a >= b:
                    break
            self.gb.setWeight(node, value)
            return value
        else:
            value = float('inf')
            self.createSon(node)
            for child in self.gb.getSon(node):
                value = min(value, self.algorithm(child, depth - 1, a, b, True))
                b = min(b, value)
                if b <= a:
                    break
            self.gb.setWeight(node, value)
            return value

    def bestPlaying(self, node: int, depth: int, is_maximizing: bool) -> Board:
        search = self.algorithm(node, depth, float('-inf'), float('inf'), is_maximizing)

        # Zero-based
        son = self.gb.getSon(0)

        x = 0

        for s in son:
            if self.gb.getWeight(s) == search:
                x = s
                break

        return self.gb.getBoard(x)