class Translator:
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    numbers = [8, 7, 6, 5, 4, 3, 2, 1]

    @staticmethod
    def notation_chess_to_computer(pos_w, pos_h):
        if ord(pos_w) > 90:
            pos_w = chr(ord(pos_w) - (ord('a') - ord('A')))

        ordered_pair = [Translator.search_gross(Translator.numbers, pos_h),
                        Translator.letters.index(pos_w)]

        return ordered_pair

    @staticmethod
    def notation_computer_to_chess(i, j):
        ordered_pair = f"{Translator.letters[j]}{Translator.numbers[i]}"
        return ordered_pair

    @staticmethod
    def search_gross(lst, e):
        element = 0
        for i in range(len(lst)):
            if e == lst[i]:
                element = i
        return element


# Exemplo de uso
# print(Translator.notation_computer_to_chess(0, 0))
# retorno = Translator.notation_chess_to_computer('e', 1)
# print(f"{retorno[0]} {retorno[1]}")
# print(retorno[1])
