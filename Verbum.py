from termcolor import colored
import random  
import mysql.connector 

# Allows to run one python script as a subprocess inside another
import subprocess

# Module to securely get the mysql user's password
import getpass

# Module to identify which operating system the user is running the game on
import os

# Identify os and run shell command to clear the screen accordingly, "nt" is the identifier for windows
os.system('cls' if os.name == 'nt' else 'clear')

# Securely get user password and store it as variable "password"
password = getpass.getpass("Enter MySQL password: ")

# Check if MySQL server is running
result = subprocess.run(["python3", "sqlcheck.py"])
if result.returncode == 0:
    print("Connecting to MySQL")
else:
    print("MySQL server is not running!")
    exit(1)

# Perform first time setup
print("Loading...")
subprocess.run(["python3", "wordcheck.py"])

con=mysql.connector.connect(user='root', host='localhost', database='Verbum', password=password)

# Clear password to save memory and for security
password = ""

# User greeting

subprocess.run(["python3", "title.py"])

cur=con.cursor()
play=input('Have you played with us before? \n(Y/N)').strip().upper()

if play=='Y':
    cur.execute('Select username from users')
    usernames=[u[0] for u in cur.fetchall()]
    print('Enter your previously used username:\n')
    while True:
        username=(input('')).lower().strip()
        if username not in usernames:
            print("We don't have this name in our database, please enter a previously used name")
        else:
            break
    print('Welcome back', username, '!')
    cur.execute('update users set play=play+1 where username=%s;',(username,))
    con.commit()
    
        
if play=='N':
    while True:
        
        # Check if database already exists
        answer = input("Is this your first time running the game? (y/n): ").strip().lower()

        # Set up database if not exists
        if answer == "y":
            print("Performing first time setup...")
            subprocess.run(["python3", "sqlconnect.py"])
        else:
            print("Starting game...")
        cur.execute('Select username from users')
        usernames=[u[0] for u in cur.fetchall()]
        print('Enter new username \n')
        username=(input('')).lower().strip()
        if username in usernames:
            print('This has already been taken, please enter a different username')
        else:
            print('Hello', username, '!')
            break
    cur.execute('insert into users (username, play, win, score) VALUES (%s, %s, %s, %s)', (username, 1, 0, 0))
    con.commit()
    
    
cur.execute('Select score from users where username=%s', (username,))
high_score=cur.fetchone()[0]


#opening file and loading all words and meanings into dictionary 'all_words'
all_words={}
f=open('Word_Database.txt', 'r')
lines=f.readlines()
for i in lines:
    x=i.partition(':')
    if x[0] not in (all_words.keys()):
        all_words[x[0].strip()]=x[2].strip()
f.close()

print('Welcome!')
print('If a letter is in the right position, then the letter will turn magenta \nIf it is in the correct word but not in the right position, it will turn cyan \nIf it is not in the correct word, it will turn grey')
print()
print('You will get six guesses to get to the correct word. \nEnjoy!:)')
print()

words0=list(all_words.keys()) #;ist of all lemma 

def color(letter, bg, c='white'):      #letter: the letter to color the background of, bg:the color to turn background of the letter
    b=colored(letter, c, 'on_'+bg, attrs=['bold'])
    return b
    

play_again='go'
print('\n', '~'*50, '\n')
while play_again=='go':
    
    correct_word1=random.choice(words0)
    
    guesses=0
    guess_list=[]
    while guesses<6:
        guess=input().lower()
        
        if guess==correct_word1:
            
            print(color(guess, 'magenta'))
            print('You have guessed correctly!')
            print("The meaning of the word is: \n", colored(all_words[correct_word1], 'green', attrs=['bold']))
            
            cur.execute('Update users set win=win+1 where username=%s;', (username,))
            if (60-(guesses*10))>high_score:
                cur.execute('Update users set score=%s where username=%s', ((60-(guesses*10)), username))
                high_score=60-(guesses*10)
                print('Your new highest score is', high_score, '!')
            con.commit()
            break
        
        elif guess not in words0:
            print('Sorry, the word you have entered is not valid. Please try again')
            
            
        else:
            if guess in guess_list:
                print('You have already guessed this word, please try a new one')
            else:   
                guess_list.append(guess)
                guesses+=1
                
                correct_word=list(correct_word1)
                for i in range(6):
                    
                    if guess[i]==correct_word[i]:
                        print(color(guess[i], 'magenta'), end=' ')
                        correct_word[i]=" "

                    
                    elif guess[i] in correct_word:
                        print(color(guess[i], 'cyan', 'black'), end=' ')
                        letter=guess[i]
                        for j in range(6):
                            if correct_word[j]==letter:
                                correct_word[j]=' '
                                break
                            
                    
                    else:
                        print(color(guess[i], 'grey'), end=' ')
                print('\n ----------'*1)
                
            
    else:
        print()
        print('Sorry, you could not guess correctly')
        print()
        print('The correct word was', colored(correct_word1, 'green', attrs=['bold']))
        print('The meaning of', colored(correct_word1, 'green', attrs=['bold']), 'is: \n', color(all_words[correct_word1], 'magenta'))
        print()
        print('Thank you for playing with us! \n\n')
        
        print('Your current highest score is', high_score)
        
    play_again=input('Do you want to play again? Say Go. \nTo quit playing , say Quit').strip().lower()  
if play_again=='quit':
    print('See you again later!')
    
cur.close()
con.close()
                