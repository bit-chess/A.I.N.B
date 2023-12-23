import sys
sys.path.append('../Notation')
sys.path.append('../Rules')

from Translator import Translator
from Board import Board
from Game import Game
from UnexpectedPieceException import UnexpectedPieceException
from IllegalMoveException import IllegalMoveException
from BoardOutOfBoundsException import BoardOutOfBoundsException

def main():
    board = Board()
    game = Game(board)

    while not game.hasEnded():
        game.getBoard().printImage()
        print()
        first = input("Peça da posição.: ")
        second = input("Para.: ")

        ii = Translator.notationChessToComputer(first[0], int(first[1]))
        jj = Translator.notationChessToComputer(second[0], int(second[1]))

        try:
            game.allLegal()
            game.move(ii[0], ii[1], jj[0], jj[1])
            game.allLegal()
            game.isCheckMateBlack()
            game.isCheckMateWhite()
            game.isBlackPromotion()
            game.isWhitePromotion()

        except BoardOutOfBoundsException:
            print("\n*Fora do tabuleiro*\n")
        except (IndexError, UnexpectedPieceException):
            print("\n*Não é peça*\n")
        except IllegalMoveException:
            print("\n*Movimento ilegal*\n")
        except IndexError:
            print("\n*Indice inválido*\n")
        

    game.getBoard().printImage()
    print(" ")
    print("Jogo Acabou")

if __name__ == "__main__":
    main()
