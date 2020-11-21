import tkinter,random,io,os
from PIL import Image,ImageTk


progress_file = 'countries_to_learn.csv'
original_file = 'countries_to_capitals.csv'
seen_all_cards = False


def get_countries_and_mappings():
    countries = []
    countries_to_capitals = {}

    try:
        with io.open(progress_file,'r',encoding='utf-8') as f:
            for line in f:
                country,capital = line.strip().split(',')
                countries_to_capitals[country] = capital
                countries.append(country) 
    except FileNotFoundError:
        with io.open(original_file,'r',encoding='utf-8') as f:
            for i,line in enumerate(f):
                if i == 0:
                    continue
                country,capital = line.strip().split(',')
                countries_to_capitals[country] = capital
                countries.append(country)
                if i == 4:
                    break

    random.shuffle(countries)
    return countries,countries_to_capitals



countries,countries_to_capitals = get_countries_and_mappings()
countries_index = len(countries) - 1

def switch_country():
    global current_country,timer,countries_index,seen_all_cards,showing_answer
    showing_answer = False
    window.after_cancel(timer)
    countries_index -= 1
    if countries_index < 0:
        seen_all_cards = True
        canvas.itemconfig(label,text='',fill='black')
        canvas.itemconfig(country_text,text="All Cards Seen!",fill='black')
        canvas.itemconfig(card_image,image=front_image)
        if len(countries_to_capitals) > 0:
            with io.open(progress_file,'w',encoding='utf-8') as f:
                for country,capital in countries_to_capitals.items():
                    f.write(country + ',' + capital + '\n')
        else:
            if os.path.exists(progress_file):
                os.remove(progress_file)
    else:
        current_country = countries[countries_index]
        canvas.itemconfig(card_image,image=front_image)
        canvas.itemconfig(label,text='Country',fill='black')
        canvas.itemconfig(country_text,text=current_country,fill='black')
        timer = window.after(3000,flip_card)

def flip_card():
    global showing_answer
    showing_answer = True
    canvas.itemconfig(card_image,image=back_image)
    canvas.itemconfig(label,text='Capital',fill='white')
    canvas.itemconfig(country_text,text=countries_to_capitals[current_country],fill='white')

def know_it():
    
    if seen_all_cards or not showing_answer: 
        return
    del countries_to_capitals[current_country]
    switch_country()

def do_not_know_it():
    if seen_all_cards or not showing_answer: 
        return
    switch_country()

BACKGROUND_COLOR = "#B1DDC6"

showing_answer = False
window = tkinter.Tk()
window.configure(bg=BACKGROUND_COLOR,padx=50,pady=50)


timer = window.after(3000,flip_card)

canvas = tkinter.Canvas(width=800,height=526,highlightthickness=0)
canvas.configure(bg=BACKGROUND_COLOR)
image = Image.open('images\card_front.png')
front_image = ImageTk.PhotoImage(image)
back_image  = tkinter.PhotoImage(file='images\card_back.png')
card_image = canvas.create_image(400,526//2,image=front_image)

current_country = countries[countries_index]
label = canvas.create_text(400,150,text='Country',font=('Arial',40,'italic'))
country_text = canvas.create_text(400,526//2,text=current_country,font=('Arial',60,'bold'))
canvas.grid(row=0,column=0,columnspan=2)


wrong_image = tkinter.PhotoImage(file="images/wrong.png")
wrong_button = tkinter.Button(image=wrong_image,highlightthickness=0,command=do_not_know_it)
wrong_button.grid(row=1,column=0)

right_image = tkinter.PhotoImage(file="images/right.png")
right_button = tkinter.Button(image=right_image,highlightthickness=0,command=know_it)
right_button.grid(row=1,column=1)

def reset():
    global timer
    try:
        window.after_cancel(timer)
    except:
        pass
    global seen_all_cards,countries,countries_to_capitals,countries_index,current_country,showing_answer
    showing_answer = False
    countries,countries_to_capitals = get_countries_and_mappings()
    random.shuffle(countries)
    countries_index = len(countries) - 1
    current_country = countries[countries_index]
    canvas.itemconfig(label,text='Country')
    canvas.itemconfig(country_text,text=current_country)
    timer = window.after(3000,flip_card)

reset_button = tkinter.Button(text="RESET",font=('Arial','40','normal'),command=reset)
reset_button.grid(row=2,column=0,columnspan=2)




window.mainloop()
if not seen_all_cards:
    # create write_to_file functiocn
    with open(progress_file,'w',encoding='utf-8') as f:
        for country,capital in countries_to_capitals.items():
            f.write(country + ',' + capital + '\n')








