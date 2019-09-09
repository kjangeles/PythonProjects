import random

WORDLIST_FILE = "words.txt"

inFILE = open(WORDLIST_FILE, 'r')
line = inFILE.readline()
words_list = line.split()
inFILE.close()

HANGMAN = (
"""
- - - - -
|       |
|
|
|
|
|
|
|
- - - - - - 
""",
"""
- - - - -
|       |
|     (X.X)
|
|
|
|
|
|
- - - - - -
""",
"""
- - - - -
|       |
|     (X.X)
|       |
|
|
|
|
|
- - - - - -
""",
"""
- - - - -
|       |
|     (X.X)
|      /|
| 
|
|
|
|
- - - - - -
""",
"""
- - - - -
|       |
|     (X.X)
|      /|\\
| 
|
|
|
|
- - - - - -
""",
"""
- - - - -
|       |
|     (X.X)
|      /|\\
|      /
|
|
|
|
- - - - - -
""",
"""
- - - - -
|       |
|     (X.X)
|      /|\\
|      / \\
|
|
|
|
- - - - - -
""")
def Title_Screen():
    print("WELCOME TO HANGMAN\nType a letter at a time to guess or type 'give up' to quit early\n")
    print(HANGMAN[0])

def losegame():
    print(("Game Over. The word was {} \nWould you like to play again?\n").format(secretWord))
    answer = input("> ").lower()
    if answer not in ("yes", "y"):
        return False
    else:
        Title_Screen()
        return True


Title_Screen()
play_again = True
while play_again:
    secretWord = random.choice(words_list).lower() 
    user_guess = None 
    guessed_letters = []                                        
    blank_word = []                                            
    for letter in secretWord:
        blank_word.append("_")                                  
    tries = 6
    length = len(secretWord)

    print(("\nThere are {} letters in the secret word").format(length))

    while tries > 0:

        if (tries != 0 and "_" in blank_word): 
            print(("\nYou have {} tries remaining.").format(tries))
        
        try:
            guess = input("\nPlease type a letter between A-Z: ").lower()
        except:
            print("That is not valid. Please try again.")
            continue
        
        else:
            if not guess.isalpha() and len(guess) > 1 and guess != "":        
                if guess=="give up":
                    if not losegame():
                        play_again = False
                        break
                    else:
                        secretWord = random.choice(words_list).lower() 
                        user_guess = None 
                        guessed_letters = []                                        
                        blank_word = []                                            
                        for letter in secretWord:
                            blank_word.append("_")                                  
                        tries = 6
                        length = len(secretWord)
                        break
                    print("That is not valid. Please try again.")
                continue
            
            elif guess in guessed_letters and guess != "":
                print("You have already guessed that letter. Please try again.")
                continue
            
            else:
                pass

            guessed_letters.append(guess)      

            if guess not in secretWord and play_again == True:
                tries -= 1
                print(HANGMAN[(len(HANGMAN)-1) - tries])      
                print(("\n{} is not in the secret word.").format(guess))

            else:      
                searchMore = True
                startsearchIndex = 0
                while searchMore:
                    try:
                        foundAtIndex = secretWord.index(guess, startsearchIndex)
                        blank_word[foundAtIndex] = guess
                        startsearchIndex = foundAtIndex + 1
                    except:
                        searchMore = False
            print("".join(blank_word))    
            if tries == 0:
                losegame()
                break

            if "_" not in blank_word and guess != "":
                print(("\nGreat Job! {} was the word.\nWould you like to play again?\n").format(secretWord))
                answer = input("> ").lower()
                if answer not in ("yes", "y"):
                    play_again = False
                    print("Thanks for playing Hangman!")
                else:
                    Title_Screen()
                    secretWord = random.choice(words_list).lower() 
                    user_guess = None 
                    guessed_letters = []                                        
                    blank_word = []                                            
                    for letter in secretWord:
                        blank_word.append("_")                                  
                    tries = 6
                    length = len(secretWord)
                break