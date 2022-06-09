import math
import copy
import sys
from collections import Counter

outputText = []


class Pattern:
    def __init__(self):
        self.falseLetters = set()
        self.unknownPosition = set()
        self.unfixedLetters = {}
        self.fixedLetters = {}


def string_to_dict(word):
    out = {}
    for i in range(len(word)):
        out[i] = word[i]
    return out


def dict_to_string(word):
    out = ""
    for i in range(len(word)):
        if i < 6:
            out += word[i] + ","
        else:
            out += word[i]
    return out


def letter_in_dict(letter, word):
    for i in word:
        if word[i] == letter:
            return True
    return False


def matching_word(word, pattern):
    fixedLetters = pattern.fixedLetters.copy()
    unfixedLetters = pattern.unfixedLetters.copy()
    falseLetters = pattern.falseLetters.copy()
    unknownPosition = pattern.unknownPosition.copy()
    word = string_to_dict(word)
    keys = []
    # green
    for i in fixedLetters:
        keys.append(i)
    for i in keys:
        if word[i] != fixedLetters[i]:
            return False
        word.pop(i)
        fixedLetters.pop(i)
    keys.clear()
    # yellow
    for i in unfixedLetters:
        keys.append(i)
    for i in keys:
        if word[i] == unfixedLetters[i]:
            return False
        word.pop(i)
        unfixedLetters.pop(i)
    # grey
    for letter in falseLetters:
        if letter_in_dict(letter, word):
            return False
    return True


def new_possible_words(pattern, possibles):
    newWords = []
    for i in possibles:
        if matching_word(i, pattern):
            newWords.append(i)
    return newWords


def entropy(word, word_set):
    probabilityDist = {}
    expectedInformation = 0
    size = len(word_set)
    for i in word_set:
        pattern = match(word, i)
        if pattern in probabilityDist:
            probabilityDist[pattern] += 1
        else:
            probabilityDist[pattern] = 1
    for i in probabilityDist:
        n = probabilityDist[i]
        if n != 0:
            p = n / size
            expectedInformation += p * (-math.log2(p))
    return expectedInformation


def match(guess, answer):
    out = {}
    answer = string_to_dict(answer)
    guess = string_to_dict(guess)
    keys = []
    # green
    for i in guess:
        keys.append(i)
    for i in keys:
        if answer[i] == guess[i]:
            out[i] = '1'
            answer.pop(i)
            guess.pop(i)
    keys.clear()
    # yellow
    for i in guess:
        keys.append(i)
    for i in keys:
        if letter_in_dict(guess[i], answer):
            out[i] = '2'
            guess.pop(i)
            answer.pop(i)
    # grey
    for i in guess:
        out[i] = '0'
    return dict_to_string(out)


def letter_in_word(letter, word):
    for i in word:
        if letter == i:
            return True
    return False


def duplicate(guess):
    # word to list
    guess = list(guess)
    # list to Counter to dict
    guess_dict = dict(Counter(guess))
    return guess_dict


def check_guess(guess, check_answer):
    pattern = Pattern()
    out = {}
    guess_dict = duplicate(guess)
    answer_dict = duplicate(check_answer)
    Answer = string_to_dict(check_answer)
    guess = string_to_dict(guess)
    keys = []
    for i in guess:
        keys.append(i)
    for i in keys:
        # guess 中的某字母有沒有在Answer中
        nums_in_answer = answer_dict.get(guess[i])
        # guess 中的某字母大寫有沒有在Answer中
        nums_in_swap_answer = answer_dict.get(guess[i].swapcase())
        if nums_in_answer:
            # 在猜測字中剩幾個某字母
            guess_letter = guess_dict[guess[i]]
            # 在答案字中剩幾個某字母
            answer_letter = answer_dict[guess[i]]
        else:
            guess_letter = 0
            answer_letter = 0
        # 如果兩個數字中其中一個為0時 代表沒有剩餘某字母 剩下的guess都該返還grey
        has_both_letter = guess_letter > 0 and answer_letter > 0
        if nums_in_swap_answer:
            # 在答案字中剩幾個某字母大寫
            answer_swap_letter = answer_dict[guess[i].swapcase()]
        else:
            answer_swap_letter = 0
        has_both_swap_letter = answer_swap_letter > 0
        # green
        if Answer[i] == guess[i] and has_both_letter:
            guess_letter = guess_letter - 1
            answer_letter = answer_letter - 1
            guess_dict[guess[i]] = guess_letter
            answer_dict[guess[i]] = answer_letter
            out[i] = '1'
            pattern.fixedLetters[i] = Answer[i]
            Answer.pop(i)
            guess.pop(i)
        # blue
        elif Answer[i] == guess[i].swapcase() and has_both_swap_letter:
            answer_swap_letter = answer_swap_letter - 1
            answer_dict[guess[i].swapcase()] = answer_swap_letter
            out[i] = '3'
            pattern.fixedLetters[i] = Answer[i].swapcase()
            Answer.pop(i)
            guess.pop(i)
    keys.clear()
    for i in guess:
        keys.append(i)
    for i in keys:
        # guess 中的某字母有沒有在Answer中
        nums_in_answer = answer_dict.get(guess[i])
        # guess 中的某字母大寫有沒有在Answer中
        nums_in_swap_answer = answer_dict.get(guess[i].swapcase())
        if nums_in_answer:
            in_answer = True
            # 在猜測字中剩幾個某字母
            guess_letter = guess_dict[guess[i]]
            # 在答案字中剩幾個某字母
            answer_letter = answer_dict[guess[i]]
        else:
            in_answer = False
        if nums_in_swap_answer:
            in_swap_answer = True
            answer_swap_letter = answer_dict[guess[i].swapcase()]
        else:
            in_swap_answer = False
            answer_swap_letter = 0
        # 如果兩個數字中其中一個為0時 代表沒有剩餘某字母 剩下的guess都該返還grey
        has_both_letter = guess_letter > 0 and answer_letter > 0
        # yellow
        # 如果字母有在答案中 且 還有剩餘
        if in_answer and has_both_letter:
            guess_letter = guess_letter - 1
            answer_letter = answer_letter - 1
            guess_dict[guess[i]] = guess_letter
            answer_dict[guess[i]] = answer_letter
            out[i] = '2'
            pattern.unfixedLetters[i] = guess[i]
            guess.pop(i)
            Answer.pop(i)
        # orange
        # 如果字母大寫有在答案中 且 字母小寫沒有在答案中 且 還有剩餘
        elif in_swap_answer and not in_answer and answer_swap_letter > 0:
            answer_swap_letter = answer_swap_letter - 1
            answer_dict[guess[i].swapcase()] = answer_swap_letter
            out[i] = '4'
            pattern.unfixedLetters[i] = guess[i]
            guess.pop(i)
            Answer.pop(i)
        # grey
        else:
            # print(str(i)+" grey " + guess[i])
            out[i] = '0'
            pattern.falseLetters.add(guess[i])
    pattern_lower = pattern
    for key in pattern.unfixedLetters:
        pattern_lower.unfixedLetters[key] = pattern_lower.unfixedLetters[key].lower()

    for key in pattern.fixedLetters:
        pattern_lower.fixedLetters[key] = pattern_lower.fixedLetters[key].lower()
    return pattern, pattern_lower, out


def colorCodeToPattern(guess):
    colorCode = string_to_dict(input("Guess: " + guess + " Enter color code: ").strip())
    pattern = Pattern()
    for i in range(len(colorCode)):
        if colorCode[i] == '0':
            pattern.falseLetters.add(guess[i].lower())
        elif colorCode[i] == '1':
            pattern.fixedLetters[i] = guess[i].lower()
        elif colorCode[i] == '2':
            pattern.unfixedLetters[i] = guess[i].lower()
        elif colorCode[i] == '3':
            pattern.fixedLetters[i] = guess[i].lower()
        elif colorCode[i] == '4':
            pattern.unfixedLetters[i] = guess[i].lower()
        elif colorCode[i] == '5':
            pattern.unknownPosition.add(i)
    pattern_lower = copy.copy(pattern)
    return pattern, pattern_lower, colorCode


def wordle(guess, alphabetical):
    # 用來尋找possible words (datasets 只有小寫字母)
    pattern = Pattern()
    # python dict
    answerTable = {}
    # python list
    possibleWords = []
    realAnswers = []
    with open(alphabetical, 'r') as f:
        for Line in f:
            word = Line.strip()
            realAnswers.append(word)
            possibleWords.append(word)
            answerTable[word] = True
    total = len(possibleWords)
    guesses = 0
    out_nums = None
    while len(pattern.fixedLetters) < 7:
        if len(possibleWords) < total:
            max_info = [0, None]
            realAnswers = []
            for word in possibleWords:
                if answerTable[word]:
                    realAnswers.append(word)
                e = entropy(word, realAnswers)
                # max_info[(float)information,(string)word]
                if e > max_info[0]:
                    max_info[0] = e
                    max_info[1] = word
            # information = -( ln(1 / 剩餘單字量) / ln (2) )
            if len(realAnswers) == 1:
                guess = realAnswers[0]
            else:
                guess = max_info[1]
        # pattern_lower用途為儲存全小寫正確pattern，否則大寫字母將無法在dataset中匹配(dataset字詞為全小寫)
        pattern, pattern_lower, out_nums = colorCodeToPattern(guess)
        guesses += 1
        possibleWords = new_possible_words(pattern_lower, possibleWords)
    has_blue = "3" in out_nums.values()
    if has_blue:
        # 在 color code 3(blue)中把藍區塊(color code 3)字母大小寫翻轉
        blue = [key for key, pos in out_nums.items() if pos == '3']
        swap_guess = list(guess)
        for i in blue:
            swap_guess[i] = swap_guess[i].swapcase()
        guess = ''.join(swap_guess)
        guesses += 1
    print('Answer: ', guess)
    print("------------------")


def first_guess(alphabetical):
    possibleWords = []
    with open(alphabetical, 'r') as f:
        for Line in f:
            word = Line.strip()
            possibleWords.append(word)
    max_info = [0, None]
    for word in possibleWords:
        e = entropy(word, possibleWords)
        if e >= max_info[0]:
            max_info[0] = e
            max_info[1] = word
    guess = max_info[1]
    print("first word: " + guess)
    return guess


def interactiveMode():
    alphabetical = str(sys.argv[1])
    # alphabetical = 'sampled71.txt'
    # init_guess = first_guess(alphabetical)
    init_guess = "darline"
    while True:
        wordle(init_guess, alphabetical)


if __name__ == '__main__':
    interactiveMode()
