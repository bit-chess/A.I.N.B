import sys

sys.path.append('../Rules')
from Board import Board
from Game import Game
from UnexpectedPieceException import UnexpectedPieceException
from IllegalMoveException import IllegalMoveException
from BoardOutOfBoundsException import BoardOutOfBoundsException

sys.path.append('../Algorithm')
from AlphaBeta import AlphaBeta

sys.path.append('../Notation')
from Translator import Translator

def main():
    board = Board()
    depth = 3

    while not board.endOfGame:
        game = Game(board)
        foraNucleo = AlphaBeta(board)

        game.board.printImage()
        print()

        if not board.getTurn():
            try:

                board = foraNucleo.bestPlaying(0, depth, False)

                test = Game(board)
                test.allLegal()
                test.isCheckMateBlack()
                test.isCheckMateWhite()
                test.isBlackPromotion()
                test.isWhitePromotion()

                print("De:", Translator.notationComputerToChess(board.lastMove[0][0], board.lastMove[0][1]),
                      "Para:", Translator.notationComputerToChess(board.lastMove[1][0], board.lastMove[1][1]))

            except BoardOutOfBoundsException as b:
                print("\n*Fora do tabuleiro*\n")

            except UnexpectedPieceException as b:
                print("\n*Não é peça*\n")

            except IllegalMoveException as i:
                print("\n*Movimento ilegal*\n")
   
        else:
            first = input("Peça da posição: ")
            second = input("Para: ")

            try:
                ii = Translator.notationChessToComputer(first[0], int(first[1]))
                jj = Translator.notationChessToComputer(second[0], int(second[1]))

                game.allLegal()

                game.getHasWhiteKingMoved()
                game.getHasWhiteLeftRookMoved()
                game.getHasWhiteRightRookMoved()

                game.move(ii[0], ii[1], jj[0], jj[1])
                game.allLegal()

                game.isCheckMateBlack()
                game.isCheckMateWhite()

                game.isWhitePromotion()
                game.isBlackPromotion()

            except BoardOutOfBoundsException as b:
                print("\n*Fora do tabuleiro*\n")

            except UnexpectedPieceException as b:
                print("\n*Não é peça*\n")

            except IllegalMoveException as i:
                print("\n*Movimento ilegal*\n")

            
    board.printImage()
    print("\nJogo Acabou")

if __name__ == "__main__":
    main()
