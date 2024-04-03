from tkinter import *
import tkinter as tk
from tkinter.ttk import Progressbar
from pygame import mixer
import pyttsx3
from tkinter import ttk, messagebox
import json
from tkinter import Tk, Text, Button, Label, Frame, PhotoImage
import tkinter.messagebox as messagebox
from tkinter import StringVar
from tkinter import Tk,Text,Button,StringVar,Label
import random
import sqlite3
import re
from tkinter import Tk, Entry, Label, Button, messagebox
from tkinter import PhotoImage


#create database


def create_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, scores INTEGER, amount_won REAL)''')
    conn.commit()
    conn.close()

def update_scores(username, new_score):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET scores = ? WHERE username = ?", (new_score, username))
    conn.commit()
    conn.close()

def update_amount_won(username, amount):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET amount_won = ? WHERE username = ?", (amount, username))
    conn.commit()
    conn.close()

    

def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def username_exists(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result is not None

def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None

def register():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter a username and password.")
        return
    if len(password) < 6 or not password.isalnum():
        messagebox.showerror("Error", "Password must be alphanumeric and at least 6 characters long.")
        return
    if username_exists(username):
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        return
    if register_user(username, password):
        messagebox.showinfo("Success", "Registration successful. You can now log in.")
    else:
        messagebox.showerror("Error", "Failed to register user.")

category_window = None  
def logout():
    global category_window
    if category_window:
        category_window.destroy()  # Destroy the category selection window
    create_login_window()  # Show the login window again


def exit_game():
    global category_window
    category_window.destroy()





def login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter a username and password.")
        return
    if authenticate_user(username, password):
        messagebox.showinfo("Success", "Login successful.")
        root.destroy()  # Destroy the login window
        show_category_selection()  # Show category selection window
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def forgot_password():
    messagebox.showinfo("Forgot Password", "Please contact support for assistance.")

def show_password():
    if password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")



def show_category_selection():
    global category_window
    category_window = tk.Tk()
    category_window.title("Category Selection")
    category_window.geometry("1430x1430")
    category_window.configure(bg="blue")

    img = tk.PhotoImage(file="logo90.png")
    img_label = tk.Label(category_window, image=img)
    img_label.pack()

    categories = ["GENERAL KNOWLEDGE", "GEOGRAPHY", "HISTORY", "LITERATURE", "MUSIC", "POP CULTURE", "SPORT", "COMPUTER SCIENCE", "RIDDLES", "SCIENCE AND TECHNOLOGY"]

    def start_game_with_category(category):
        global category_window
        category_window.destroy() 
        main_game(category) 
      
     
    
    #for category in categories:
        #button = ttk.Button(category_window, text=category, command=lambda cat=category: start_game_with_category(cat))
        #button.pack(pady=5)

    category_frame = ttk.Frame(category_window)
    category_frame.pack()

    for category in categories:
        button = ttk.Button(category_frame, text=category, command=lambda cat=category: start_game_with_category(cat))
        button.pack(side=tk.LEFT, padx=5, pady=5)

    logout_button = ttk.Button(category_window, text="Logout", command=logout)
    logout_button.pack(pady=5)

    exit_button = ttk.Button(category_window, text="Exit", command=exit_game)
    exit_button.pack(pady=5)




    category_window.mainloop()


"""
def start_timer(category):
    timer_decision_window = tk.Toplevel()  # Create a new window for timer decision
    timer_decision_window.title("Timer Decision")
    timer_decision_window.geometry("300x150")

    decision_label = ttk.Label(timer_decision_window, text="Do you want to enable the timer?")
    decision_label.pack(pady=10)

    def start_with_timer():
        timer_decision_window.destroy()  # Close the decision window
        start_timer_window(category)

    def start_without_timer():
        timer_decision_window.destroy()  # Close the decision window
        #start_quiz(category, enable_timer=False)  # Start the quiz without a timer
        
       

    timer_button_frame = ttk.Frame(timer_decision_window)
    timer_button_frame.pack(pady=10)

    timer_button = ttk.Button(timer_button_frame, text="Start with Timer", command=start_with_timer)
    timer_button.grid(row=0, column=0, padx=10)

    no_timer_button = ttk.Button(timer_button_frame, text="Continue without Timer", command=start_without_timer)
    no_timer_button.grid(row=0, column=1, padx=10)

def start_timer_window(category):
    timer_window = tk.Toplevel()  # Use Toplevel instead of Tk
    timer_window.title("Timer")
    timer_window.geometry("300x200")

    img = tk.PhotoImage(file="timerr.png")
    img_label = tk.Label(timer_window, image=img)
    img_label.pack()

    countdown_label = ttk.Label(timer_window, text="Time Left:")
    countdown_label.pack()

    countdown_var = tk.StringVar()
    countdown_display = ttk.Label(timer_window, textvariable=countdown_var)
    countdown_display.pack()

    # Timer countdown functionality
    def countdown(seconds):
        if seconds > 0:
            countdown_var.set(seconds)
            timer_window.after(1000, countdown, seconds - 1)  # Schedule the next call after 1000ms (1 second)
        else:
            countdown_var.set("Time's up!")
            try_again_button = ttk.Button(timer_window, text="Try Again", command=timer_window.destroy)
            try_again_button.pack(pady=5)

            # Call the appropriate quiz function based on the selected category
            start_quiz(category)
           

    countdown(60)  # Start the countdown from 60 seconds

    timer_window.mainloop()

"""



def create_login_window():
    global root, username_entry, password_entry, password_var

    root = tk.Tk()
    root.title("Who Wants to Be a Millionaire - Login")
    root.geometry("1430x1430")
    root.resizable(True, True)  # Allow window expansion

    # Add image of Who Wants to Be a Millionaire
    img = tk.PhotoImage(file="logo90.png")
    img_label = tk.Label(root, image=img)
    img_label.pack()

    frame = ttk.Frame(root)
    frame.pack(pady=10)

    username_label = ttk.Label(frame, text="Username:")
    username_label.grid(row=0, column=0, padx=5, pady=5)

    # Create a rounded entry widget for username
    username_entry = ttk.Entry(frame, style="Rounded.TEntry")
    username_entry.grid(row=0, column=1, padx=5, pady=5)

    password_label = ttk.Label(frame, text="Password:")
    password_label.grid(row=1, column=0, padx=5, pady=5)

    # Create a rounded entry widget for password
    password_var = tk.BooleanVar()
    password_entry = ttk.Entry(frame, show="*", style="Rounded.TEntry")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    # Add "Show Password" checkbutton
    password_checkbutton = ttk.Checkbutton(frame, text="Show Password", variable=password_var, command=show_password)
    password_checkbutton.grid(row=2, columnspan=2, pady=5)

    login_button = ttk.Button(frame, text="Login", command=login, style="Green.TButton")
    login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    register_button = ttk.Button(frame, text="Register", command=register, style="Blue.TButton")
    register_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

    forgot_password_label = tk.Label(root, text="Forgot Password?", fg="blue", cursor="hand2")
    forgot_password_label.pack(pady=5)
    forgot_password_label.bind("<Button-1>", lambda e: forgot_password())

    # Define custom style for rounded entry widgets
    root.style = ttk.Style()
    root.style.theme_use("classic")
    #root.style.configure("Rounded.TEntry", padding=10, relief="flat", foreground="black")
    root.style.configure("Rounded.TEntry", padding=(10, 5), relief="raised", foreground="black")
   
  

    root.mainloop()


def main_game(category):
    # Initialize pyttsx3 engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[0].id)

    # Initialize mixer and play background music
    mixer.init()
    mixer.music.load("kbc.mp3")
    mixer.music.play(-1)

    


    def select(event):
        callButtton.place_forget()
        progressBarA.place_forget()
        progressBarB.place_forget()
        progressBarC.place_forget()
        progressBarD.place_forget()


        progressbarLabelA.place_forget()
        progressbarLabelB.place_forget()
        progressbarLabelC.place_forget()
        progressbarLabelD.place_forget()
        b=event.widget
        value=b["text"]

        for i in range(15):
            if value==correct_answers[i]:
                if value==correct_answers[14]:
                    def close():
                        root2.destroy()
                        root.destroy()
                    def playagain():
                        lifeline50Button.config(state=NORMAL,image=image50)
                        audiencePoleButton.config(state=NORMAL,image=audiencePole)
                        phoneLifeLineButton.config(state=NORMAL,image=phoneImage)
                        root2.destroy()
                        questionArea.delete(1.0,END)
                        questionArea.insert(END,question[0])
                        optionButton1.config(text=First_options[0])
                        optionButton2.config(text=Second_options[0])
                        optionButton3.config(text=Third_options[0])
                        optionButton4.config(text=Fourth_options[0])
                        amountLabel.config(image=amountImages)

                # load_new_questions()

                    mixer.music.stop()
                    mixer.music.load("kbcwon.mp3")
                    mixer.music.play()
                    root2=Toplevel()
                    root2.config(bg="black")
                    root2.geometry("500x400+140+30")
                    root2.title("You won 100,000,000 pounds")
                    imgLabel=Label(root2,image=centerImage,bd=0)
                    imgLabel.pack(pady=30)

                    
                    winLabel=Label(root2, text="You Won",font=("arial", 40, "bold",), bg='black', fg="white")
                    winLabel.pack()

                    playagainButton=Button(root2, text="Play Again",font=("arial",20,"bold"),bg="black", fg="white",activebackground="black",activeforeground="white",bd=0,cursor="hand2",command=playagain)
                    playagainButton.pack()

                    closeButton=Button(root2, text="Close",font=("arial",20,"bold"),bg="black", fg="white",activebackground="black",activeforeground="white",bd=0,cursor="hand2",command=close)
                    closeButton.pack()

                    happyimage=PhotoImage(file="happy.png")
                    happyLabel=Label(root2,image=happyimage,bg="black")
                    happyLabel.place(x=30,y=280)
                        
                    happyLabel1=Label(root2,image=happyimage,bg="black")
                    happyLabel1.place(x=400,y=280)


                    root2.mainloop()
                    break

                questionArea.delete(1.0,END)
                questionArea.insert(END,question[i+1])
                optionButton1.config(text=First_options[i+1])
                optionButton2.config(text=Second_options[i+1])
                optionButton3.config(text=Third_options[i+1])
                optionButton4.config(text=Fourth_options[i+1])
                amountLabel.configure(image=amountImages[i])
                amountLabel.image = amountImages[i]


            if value not in correct_answers:
                def close():
                    root1.destroy()
                    root.destroy()
                def tryagain():
                    lifeline50Button.config(state=NORMAL,image=image50)
                    audiencePoleButton.config(state=NORMAL,image=audiencePole)
                    phoneLifeLineButton.config(state=NORMAL,image=phoneImage)
                    root1.destroy()
                    questionArea.delete(1.0,END)
                    questionArea.insert(END,question[0])
                    optionButton1.config(text=First_options[0])
                    optionButton2.config(text=Second_options[0])
                    optionButton3.config(text=Third_options[0])
                    optionButton4.config(text=Fourth_options[0])
                    amountLabel.config(image=amountImages[0])

                root1=Toplevel()
                root1.config(bg="black")
                root1.geometry("500x400+140+30")
                root1.title("You won 0 pounds")
                imgLabel=Label(root1,image=centerImage,bd=0)
                imgLabel.pack(pady=30)

                loseLabel=Label(root1, text="You lose",font=("arial", 40, "bold",), bg='black', fg="white")
                loseLabel.pack()

                tryagainButton=Button(root1, text="Try Again",font=("arial",20,"bold"),bg="black", fg="white",activebackground="black",activeforeground="white",bd=0,cursor="hand2",command=tryagain)
                tryagainButton.pack()

                closeButton=Button(root1, text="Close",font=("arial",20,"bold"),bg="black", fg="white",activebackground="black",activeforeground="white",bd=0,cursor="hand2",command=close)
                closeButton.pack()

                sadimage=PhotoImage(file="sad.png")
                sadLabel=Label(root1,image=sadimage,bg="black")
                sadLabel.place(x=30,y=280)
                
                sadLabel1=Label(root1,image=sadimage,bg="black")
                sadLabel1.place(x=400,y=280)
                root1.mainloop()
                break
    def lifeline50():
        lifeline50Button.config(image=image50X,state=DISABLED)
        if questionArea.get(1.0,"end-1c")==question[0]:
           optionButton2.config(text='')
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[1]:
           optionButton1.config(text='')
           optionButton2.config(text="")
        if questionArea.get(1.0,"end-1c")==question[2]:
           optionButton1.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[3]:
           optionButton2.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[4]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[5]:
           optionButton2.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[6]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[7]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[8]:
           optionButton2.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[9]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[10]:
           optionButton1.config(text="")
           optionButton2.config(text="")
        if questionArea.get(1.0,"end-1c")==question[11]:
           optionButton3.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[12]:
           optionButton1.config(text="")
           optionButton4.config(text="")
        if questionArea.get(1.0,"end-1c")==question[13]:
           optionButton1.config(text="")
           optionButton3.config(text="")
        if questionArea.get(1.0,"end-1c")==question[14]:
           optionButton2.config(text="")
           optionButton4.config(text="")
    def audiencePoleLifeLine():
        audiencePoleButton.config(image=audiencePoleX, state=DISABLED)
        progressBarA.place(x=580, y=190)
        progressBarB.place(x=620, y=190)
        progressBarC.place(x=660, y=190)
        progressBarD.place(x=700, y=190)

        progressbarLabelA.place(x=580, y=320)
        progressbarLabelB.place(x=620, y=320)
        progressbarLabelC.place(x=660, y=320)
        progressbarLabelD.place(x=700, y=320)

        if questionArea.get(1.0,"end-1c")==question[0]:
           progressBarA.config(value=30)
           progressBarB.config(value=50)
           progressBarC.config(value=90)
           progressBarD.config(value=60)
        if questionArea.get(1.0,"end-1c")==question[1]:
           progressBarA.config(value=30)
           progressBarB.config(value=50)
           progressBarC.config(value=70)
           progressBarD.config(value=40)
        if questionArea.get(1.0,"end-1c")==question[2]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=40)
           progressBarD.config(value=30)
        if questionArea.get(1.0,"end-1c")==question[3]:
           progressBarA.config(value=70)
           progressBarB.config(value=20)
           progressBarC.config(value=40)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[4]:
           progressBarA.config(value=20)
           progressBarB.config(value=30)
           progressBarC.config(value=40)
           progressBarD.config(value=70)
        if questionArea.get(1.0,"end-1c")==question[5]:
           progressBarA.config(value=70)
           progressBarB.config(value=40)
           progressBarC.config(value=20)
           progressBarD.config(value=10)
        if questionArea.get(1.0,"end-1c")==question[6]:
           progressBarA.config(value=40)
           progressBarB.config(value=60)
           progressBarC.config(value=30)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[7]:
           progressBarA.config(value=10)
           progressBarB.config(value=60)
           progressBarC.config(value=40)
           progressBarD.config(value=30)
        if questionArea.get(1.0,"end-1c")==question[8]:
           progressBarA.config(value=20)
           progressBarB.config(value=40)
           progressBarC.config(value=70)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[9]:
           progressBarA.config(value=30)
           progressBarB.config(value=70)
           progressBarC.config(value=50)
           progressBarD.config(value=20)
        if questionArea.get(1.0,"end-1c")==question[10]:
           progressBarA.config(value=20)
           progressBarB.config(value=50)
           progressBarC.config(value=70)
           progressBarD.config(value=30)
        if questionArea.get(1.0,"end-1c")==question[11]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=50)
           progressBarD.config(value=40)
        if questionArea.get(1.0,"end-1c")==question[12]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=40)
           progressBarD.config(value=50)
        if questionArea.get(1.0,"end-1c")==question[13]:
           progressBarA.config(value=20)
           progressBarB.config(value=70)
           progressBarC.config(value=30)
           progressBarD.config(value=40)
        if questionArea.get(1.0,"end-1c")==question[14]:
           progressBarA.config(value=20)
           progressBarB.config(value=40)
           progressBarC.config(value=70)
           progressBarD.config(value=50)

    def phoneLifeLine():
        mixer.music.load("calling.mp3")
        mixer.music.play()
        callButtton.place(x=70,y=260)
        phoneLifeLineButton.config(image=phoneImageX,state=DISABLED)

    def phoneclick():
        for i in range(15):
           if questionArea.get(1.0,'end-1c')==question[i]:
              engine.say(f"The answer is {correct_answers[i]}")
              engine.runAndWait()
              mixer.init()
              mixer.music.load("kbc.mp3")
              mixer.music.play(-1)

    correct_answers = [
    "Tokyo","Canberra", "Mars","Shakespeare","Pacific Ocean",
    "1776", "Vincent van Gogh", "Yen", "Nitrogen",
    "Albert Einstein", "Japan", "Blue whale",
    "Helium", "Harper Lee", "Ottawa"]

    question=["What is the capital of Japan?",
          "What is the capital city of Australia?",
          "Which planet is known as the Red Planet?",
          "Who wrote 'Romeo and Juliet?",
          "What is the largest ocean on Earth?",
          "In what year did the United States declare its independence?",
          "Who painted the famous artwork \"Starry Night\"?",
          "What is the currency of Japan?",
          "Which gas makes up the majority of Earth's atmosphere?",
          "Who is known as the \"Father of Modern Physics\"?",
          "Which country is known as the \"Land of the Rising Sun\"?",
          "What is the largest mammal in the world?",
          "Which of the following elements is a noble gas?",
          "Who wrote the famous novel \"To Kill a Mockingbird\"?",
          "What is the capital city of Canada?"]

    First_options = [
        "Seoul",
        "Sydney",
        "Venus",
        "Shakespeare",
        "Atlantic Ocean",
        "1776",
        "Pablo Picasso",
        "Won",
        "Oxygen",
        "Isaac Newton",
        "China",
        "Elephant",
        "Oxygen",
        "J.K. Rowling",
        "Vancouver"
    ]
    Second_options = [
       "Beijing","Melbourne", "Mars", "Jane Aust", "Indian Ocean",
       "1789", "Vincent van Gogh", "Yen", "Carbon dioxide",
       "Albert Einstein", "South Korea", "Blue whale",
       "Helium", "Harper Lee", "Toronto"
    ]

    Third_options = [
       "Tokyo","Canberra", "Jupiter", "C.Dickens","Southern Ocean",
       "1800", "Leonardo Vinci", "Baht", "Nitrogen",
       "Galilei", "Japan", "Giraffe",
       "Sodium", "Ernest Hemingway", "Ottawa"
    ]

    Fourth_options = [
       "BangKok","Brisbane", "Saturn","Emily Brontë", "Pacific Ocean",
       "1865", "Claude Monet", "Ringgit", "Hydrogen",
       "Nikola Tesla", "Vietnam","Gorilla",
       "Carbon", "Scott gerald", "Montreal"
    ]

# Shuffle the questions, options, and correct answers together
    questions_and_options = list(zip(question, First_options, Second_options, Third_options, Fourth_options, correct_answers))
    random.shuffle(questions_and_options)

    # Unpack the shuffled values
    question, First_options, Second_options, Third_options, Fourth_options, correct_answers = zip(*questions_and_options)       
        
    question, First_options, Second_options, Third_options, Fourth_options, correct_answers = zip(*questions_and_options)


    root=Tk()
    root.geometry("1430x1430+0+0")
    root.title("who want to be a millionaire created by Terry.G.")

    root.config(bg="black")
    #==============================================Frames=====================================#
    leftframe=Frame(root,bg = "black",padx=90)
    leftframe.grid()

    topFrame = Frame(leftframe,bg="black",pady=15)
    topFrame.grid()

    centerFrame = Frame(leftframe,bg="black",pady=15)
    centerFrame.grid(row=1, column=0)

    bottomFrame = Frame(leftframe)
    bottomFrame.grid(row=2, column=0)

    rightframe=Frame(root,pady=25,padx=50,bg="black")
    rightframe.grid(row=0, column=1)
    #===============================================IMAGES================================================#
    image50=PhotoImage(file="50-50.png")
    image50X=PhotoImage(file="50-50-X.png")

    lifeline50Button = Button(topFrame, image=image50, bg="black",bd=0,activebackground='black',width=180,height=80,command=lifeline50)

    lifeline50Button.grid(row=0,column=0)

    audiencePoleX=PhotoImage(file="audiencePoleX.png")
    audiencePoleButton = Button(topFrame, image=audiencePoleX,bg="black",bd=0,activebackground="black",width=180,height=80,command=audiencePoleLifeLine)
    audiencePoleButton.grid(row=0,column=1)

    audiencePole=PhotoImage(file="audiencePole.png")
    audiencePoleButton = Button(topFrame, image=audiencePole,bg="black",bd=0,activebackground="black",width=180,height=80,command=audiencePoleLifeLine)
    audiencePoleButton.grid(row=0,column=1)

    phoneImage=PhotoImage(file="phoneAFriend.png")
    phoneImageX=PhotoImage(file="phoneAFriendX.png")

    phoneLifeLineButton = Button(topFrame,image=phoneImage,bg="black",bd=0,activebackground='black',width=180,height=80,command=phoneLifeLine)
    phoneLifeLineButton.grid(row=0,column=2)

    callimage=PhotoImage(file="phone.png")
    callButtton=Button(root,image=callimage,bd=0,bg="black",activebackground="black",cursor="hand2", command=phoneclick)

    centerImage= PhotoImage(file="center.png")
    logoLabel=Label(centerFrame, image=centerImage,bg="black",width=300,height=200)
    logoLabel.grid()

    amountImage=PhotoImage(file="Picture0.png")
    amountImage1=PhotoImage(file="Picture1.png")
    amountImage2=PhotoImage(file="Picture2.png")
    amountImage3=PhotoImage(file="Picture3.png")
    amountImage4=PhotoImage(file="Picture4.png")
    amountImage5=PhotoImage(file="Picture5.png")
    amountImage6=PhotoImage(file="Picture6.png")
    amountImage7=PhotoImage(file="Picture7.png")
    amountImage8=PhotoImage(file="Picture8.png")
    amountImage9=PhotoImage(file="Picture9.png")
    amountImage10=PhotoImage(file="Picture10.png")
    amountImage11=PhotoImage(file="Picture11.png")
    amountImage12=PhotoImage(file="Picture12.png")
    amountImage13=PhotoImage(file="Picture13.png")
    amountImage14=PhotoImage(file="Picture14.png")
    amountImage15=PhotoImage(file="Picture15.png")

    amountImages = [amountImage1, amountImage2, amountImage3, amountImage4, amountImage5,
                    amountImage6, amountImage7, amountImage8, amountImage9, amountImage10,
                    amountImage11, amountImage12, amountImage13, amountImage14, amountImage15]
    amountLabel=Label(rightframe,image=amountImage,bg="black")
    amountLabel.grid()

    LayoutImage=PhotoImage(file="lay.png")
    LayoutLabel=Label(bottomFrame, image=LayoutImage,bg="black")
    LayoutLabel.grid()
    #shufffle the questions and corresponding options
    #questions_and_options = list(zip(question, First_options, Second_options, Third_options, Fourth_options, correct_answers))
    #random.shuffle(questions_and_options)

    # Unpack the shuffled values
    #question, First_options, Second_options, Third_options, Fourth_options, correct_answers = zip(*questions_and_options)
    ##shuffled_data = list(zip(shuffled_questions, shuffled_options, correct_answers))
    #random.shuffle(shuffled_data)
    #shuffled_questions, shuffled_options, correct_answers = zip(*shuffled_data)

    #=============================================QUESTION AREA==========================================#
    questionArea=Text(bottomFrame, font=("arial",18,"bold"),width=34,height=2,wrap="word",bg="black",fg="white",bd=0)
    questionArea.place(x=70,y=10)

    questionArea.insert(END,question[0])

    labelA = Label(bottomFrame,font=("arial",16,"bold"), text="A: ", bg="black", fg="white",)
    labelA.place(x=60,y=110)

    optionButton1=Button(bottomFrame, text= First_options[0],font=("arial",16,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#width=20)
    #optionButton1 = Button(bottomFrame, text=First_options[0], font=("arial", 18, "bold"), bg="black", fg="white",
                        #  bd=0, activebackground="black", activeforeground='white', cursor="hand2",
                        #  command=lambda: show_full_text(First_options[0]), wraplength=200)
    optionButton1.place(x=100, y=100)

    labelB = Label(bottomFrame,font=("arial",15,"bold"), text="B: ", bg="black", fg="white",)
    labelB.place(x=330,y=110)
    optionButton2=Button(bottomFrame, text= Second_options[0],font=("arial",15,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#idth=20)
    optionButton2.place(x=370, y=100)

    labelC = Label(bottomFrame,font=("arial",16,"bold"), text="C: ", bg="black", fg="white",)
    labelC.place(x=60,y=190)
    optionButton3=Button(bottomFrame, text= Third_options[0],font=("arial",15,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#,wraplength=200,width=20)
    optionButton3.place(x=100, y=180)
    labelD = Label(bottomFrame,font=("arial",16,"bold"), text="D: ", bg="black", fg="white",)
    labelD.place(x=330,y=190)
    optionButton4=Button(bottomFrame, text= Fourth_options[0],font=("arial",15,"bold"),bg="black", fg="white",bd=0,activebackground="black",activeforeground='white',cursor="hand2",wraplength=130)#width=20)
    optionButton4.place(x=370, y=180)
    #===========================Progress Bar(AUDIENCE POLL BUTTONS AND LABEL)=================================#
    progressBarA=Progressbar(root,orient=VERTICAL,length=120)
    progressBarB=Progressbar(root,orient=VERTICAL,length=120)
    progressBarC=Progressbar(root,orient=VERTICAL,length=120)
    progressBarD=Progressbar(root,orient=VERTICAL,length=120)

    progressbarLabelA=Label(root, text="A", font=("arial",20,"bold"),bg='black', fg="white")
    progressbarLabelB=Label(root, text="B", font=("arial",20,"bold"),bg='black', fg="white")
    progressbarLabelC=Label(root, text="C", font=("arial",20,"bold"),bg='black', fg="white")
    progressbarLabelD=Label(root, text="D", font=("arial",20,"bold"),bg='black', fg="white")
    #option_mapping = {"A": progressBarA, "B": progressbarLabelB, "C": progressbarLabelC, "D": progressbarLabelD}
    #correct_answer=StringVar()



    #=======================================OPTION FUNCTION==================================================#
    optionButton1.bind('<Button-1>', select)
    optionButton2.bind('<Button-1>', select)
    optionButton3.bind('<Button-1>', select)
    optionButton4.bind('<Button-1>', select)
    



    root.mainloop()


create_login_window()


#main_game("GENERAL KNOWLEDGE")


