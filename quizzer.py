from tkinter import *
from tkinter import font
from tkinter import messagebox
import random
import time

# FORMATTING QUESTIONS
    #   create a set of questions using "> x <"
    #   add questions using "q /a"; seperate them with a "-"
# THIS ONE goal : sets_questions_answers = {"TEST SET 1":{1:["question","answer"],2:["question","answer"]},}



def read_file():
    global sets_questions_answers

    sets_questions_answers = {}

    file =open("questions.txt","r").read().replace("\n","")

    s = file.split(">") # gets a list of each set
    del s[0]

    for set in s:
        s_qs = set.split("<") # ["set_title","questions"]
        sets_questions_answers[s_qs[0]] = {} # {"set_title":{}}
        qs = s_qs[1].split("-") # ["q/a","q/a"]
        del qs[0]
        for qna in qs:
            q_a = qna.split("/") # ["q","a"]
            sets_questions_answers[s_qs[0]][qs.index(qna)+1] = [q_a[0],q_a[1]]
    print(sets_questions_answers)


def load_set_selection():
    global set_selection_window
    set_buttons = {}
    quiz_btn.configure(state="disabled")
    set_selection_window = Tk()
    select_label = Label(set_selection_window,text="select a set of questions!!",font=font.Font(size=20))
    select_label.grid(column=0,padx=10,pady=10,row=0)

    for set in sets_questions_answers:
        set_buttons[list(sets_questions_answers).index(set)+1] = Button(set_selection_window,text=set,font=font.Font(size=20),bg="pink",command=lambda s = set : start_quiz(s))

    for button in set_buttons:
        #print(set_buttons.get(button))
        set_buttons.get(button).grid(column=0,row=list(set_buttons).index(button)+1,padx=10,pady=10)



def start_quiz(s):
    global answer_entry, current_question_no, quiz, current_score, question_label, result_label, quiz_window, submit_ans_btn
    quiz = {}
    set_selection_window.destroy()
    ordered = messagebox.askyesno("ordered","do you want your quiz to be ordered?")
    quiz = sets_questions_answers[s]
    if ordered == False:
        temp = list(list(quiz.values()))
        random.shuffle(temp)
        quiz = dict(zip(quiz,temp))

    current_question_no = 1

    quiz_window = Tk()
    question_label = Label(quiz_window,text=quiz.get(current_question_no)[0],font=font.Font(size=30))
    question_label.grid(column=0,row=0,padx=10,pady=10)
    answer_entry = Entry(quiz_window,width=30)
    answer_entry.grid(column=0,row=1,padx=10,pady=10)
    submit_ans_btn = Button(quiz_window,text="submit",bg="pink",font=font.Font(size=30),command=submit_ans)
    submit_ans_btn.grid(column=0,row=2,padx=10,pady=10)
    result_label = Label(quiz_window,text="",fg="red",fon=font.Font(size=30))
    result_label.grid(column=0,row=3,padx=5,pady=5)

    current_score = 0



def submit_ans():
    global current_score, current_question_no
    if answer_entry.get() == "" or answer_entry.get().isspace():
        messagebox.showerror("error","invalid input")
    else:
        if answer_entry.get().lower() == quiz.get(current_question_no)[1].lower():
            current_score += 1
            answer_entry.config(state="disabled")
            result_label.config(text="correct")
            time.sleep(0.5)
            answer_entry.config(state="normal")
            answer_entry.delete(0,END)
        
        else:
            answer_entry.config(state="disabled")
            result_label.config(text="incorrect")
            time.sleep(0.5)
            answer_entry.config(state="normal")

        if current_question_no == len(quiz):
                print("done")
                answer_entry.destroy()
                result_label.destroy()
                submit_ans_btn.destroy()
                question_label.config(text="score: {}/{}".format(current_score,len(quiz)))
                continue_btn = Button(quiz_window,text="continue",bg="pink",font=font.Font(size=30),command=end_quiz)
                continue_btn.grid(row=1,column=0,padx=10,pady=10)
                
        else:
             current_question_no += 1
             question_label.config(text=quiz.get(current_question_no)[0])

        print(current_score)



def end_quiz():
    quiz_window.destroy()
    quiz_btn.configure(state="active")



def create_new_set():
    global create_set_entry, new_set_question_label, new_set, choosing, new_set_window
    create_btn.config(state="disabled")
    new_set = []
    choosing = "name of test?"
    new_set_window = Tk()
    new_set_question_label = Label(new_set_window,text=choosing+"?",font=font.Font(size=30))
    new_set_question_label.grid(row=0,column=0,padx=10,pady=10)
    create_set_entry = Entry(new_set_window,width=40)
    create_set_entry.grid(row=1,column=0,padx=10,pady=10)
    set_btn = Button(new_set_window,text="submit",font=font.Font(size=30),bg="pink",command=set_creation_submit)
    set_btn.grid(row=2,column=0,padx=10,pady=10)



def set_creation_submit():
    global choosing, length, question

    if create_set_entry.get() == "" or create_set_entry.get().isspace():
        messagebox.showerror("error","invalid input")

    else:
        submission = create_set_entry.get()

        if choosing == "name of test?":
             name = submission
             new_set.append(name)
             new_set.append({})
             create_set_entry.config(state="disabled")
             time.sleep(0.5)
             create_set_entry.config(state="normal")
             create_set_entry.delete(0,END)
             choosing = "amount of questions"
             new_set_question_label.config(text=choosing+"?")

        elif choosing == "amount of questions":
            try: int(submission)
            except: messagebox.showerror("error","enter a number")
            else:
                length = float(submission)
            
                print(new_set)
                choosing = 1.0
                new_set_question_label.config(text="question {}?".format(str(int(choosing))))
                create_set_entry.config(state="disabled")
                time.sleep(0.5)
                create_set_entry.config(state="normal")
                create_set_entry.delete(0,END)

        elif type(choosing) == float:
            if choosing.is_integer():
                question = submission
                choosing += 0.5
                create_set_entry.config(state="disabled")
                time.sleep(0.5)
                create_set_entry.config(state="normal")
                create_set_entry.delete(0,END)
                new_set_question_label.config(text="answer "+str(int(choosing))+"?")
            else:
                #print(question,length)
                new_set[1][question] = submission
                choosing += 0.5
                create_set_entry.config(state="disabled")
                time.sleep(0.5)
                create_set_entry.config(state="normal")
                create_set_entry.delete(0,END)
                if choosing > length:
                    print("done")
                    create_btn.config(state="active")
                    new_set_window.destroy()
                    add_new_set()
                else: new_set_question_label.config(text="question "+str(int(choosing))+"?")


def add_new_set():
    file = open("questions.txt","a")
    qs = ""
    for i in new_set[1]:
        qs += "-{}/{}".format(i,new_set[1].get(i))

    print(qs)
    file.write("\n>{}<".format(new_set[0]))
    file.write("\n"+qs)

    file.close()

    read_file()
 
root = Tk()

title_label = Label(root,text="Self Quizzer!!",font=font.Font(size=30))
title_label.grid(column=0,row=0,padx=10,pady=10)

quiz_btn = Button(root,text="take quiz",bg="pink",font=font.Font(size=20),command=load_set_selection)
quiz_btn.grid(column=0,row=1,padx=10,pady=10)

create_btn = Button(root,text="add new set of questions",bg="pink",font=font.Font(size=20),command=create_new_set)
create_btn.grid(column=0,row=2,padx=10,pady=10)

read_file()
root.mainloop()
