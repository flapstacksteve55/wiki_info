import requests
import re 
import sys
import pandas as pd
import os 
import json
import webbrowser
from tkinter import messagebox
import tkinter
import time
from pandastable import Table
from PIL import ImageTk, Image

home = os.path.expanduser('~')
downloads = os.path.join(home, 'Downloads')
def choose_date(month,day):
    while True: 
        if len(month) == 2 and re.match('[0-1]', month[0]) and re.match('[0-9]', month[1]):
            break
        else: 
            messagebox.showerror('ERROR','Please Try Again... Month must be formatted as a 2-digit number (i.e. "01" for "January," "02" for "February," etc,)')
            raise Exception("cause of the problem")
    while True: 
        if len(day) == 2 and re.match('[0-3]', day[0]) and re.match('[0-9]', day[1]):
            break
        else: 
            messagebox.showerror('ERROR','Please Try Again... Day must be formatted as a 2-digit number (i.e. "01" for "January 1st," "02" for "January 2nd," etc,)')
            raise Exception("cause of the problem")
    return month,day

def holiday_find(month,day):

    url = 'https://en.wikipedia.org/api/rest_v1/feed/onthisday/holidays/'+month+'/'+day+''
    headers = {
        'User-Agent': 'ValentinoBot/1.0'
    }

    response = requests.get(url,headers=headers)

    # Check if the response is OK and contains JSON
    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            print("Response is not valid JSON.")
    else:
        print(f"Request failed with status code {response.status_code}")

    # Initialize a list to store the data
    holiday_data = []

    for holiday in data.get("holidays", []):
            holidays = holiday.get("text", "Unknown")
            pages = holiday.get("pages", [])
            if pages:
                page = pages[0]  # Usually the first page is the main one
                desktop_url = page.get("content_urls", {}).get("desktop", {}).get("page", "No desktop URL")
                mobile_url = page.get("content_urls", {}).get("mobile", {}).get("page", "No mobile URL")
                titles = page.get("title", "No title")
                descriptions = page.get("description", "No description")

    # Append the data to the list
                holiday_data.append({
                    "Holiday": holidays,
                    "Title": titles,
                    "Description": descriptions,
                    "Desktop URL": desktop_url,
                    "Mobile URL": mobile_url
                })

    # Create a DataFrame from the collected data
    df = pd.DataFrame(holiday_data)
    #return df
    #df.to_csv(downloads+'/holidays_'+my_date[0]+"_"+my_date[1]+'.csv')
    frame = tkinter.Toplevel(window) #this is the new window
    frame.title("HOLIDAYS")
    table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()
def birth_find(month,day):
    
    url = f'https://en.wikipedia.org/api/rest_v1/feed/onthisday/births/{month}/{day}'
    
    headers = {
        'User-Agent': 'ValentinoBot/1.0'
    }

    response = requests.get(url,headers=headers)

    # Check if the response is OK and contains JSON
    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            print("Response is not valid JSON.")
    else:
        print(f"Request failed with status code {response.status_code}")

    
    # Initialize a list to store the data
    births_data = []

    for person in data.get("births", []):
            name = person.get("text", "Unknown")
            pages = person.get("pages", [])
            
            if pages:
                page = pages[0]  # Usually the first page is the main one
                extract = page.get("extract", "No extract available")
                
                desktop_url = page.get("content_urls", {}).get("desktop", {}).get("page", "No desktop URL")
              
                mobile_url = page.get("content_urls", {}).get("mobile", {}).get("page", "No mobile URL")
                

    # Append the data to the list
                births_data.append({
                    "Name": name,
                    "Description": extract,
                    "Desktop URL": desktop_url,
                    "Mobile URL": mobile_url
                })

    # Create a DataFrame from the collected data
    df = pd.DataFrame(births_data)


    frame = tkinter.Toplevel(window) #this is the new window
    frame.title("BIRTHS")
    table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()

def event_find(month,day):
    url = f'https://en.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}'

    headers = {
        'User-Agent': 'ValentinoBot/1.0'
    }

    response = requests.get(url,headers=headers)

    # Check if the response is OK and contains JSON
    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            print("Response is not valid JSON.")
    else:
        print(f"Request failed with status code {response.status_code}")

    # Initialize a list to store the data
    events_data = []

    for event in data.get("events", []):
            events = event.get("text", "Unknown")
            year = event.get("year", "Unknown")
            pages = event.get("pages", [])
            
            if pages:
                page = pages[0]  # Usually the first page is the main one
                
                desktop_url = page.get("content_urls", {}).get("desktop", {}).get("page", "No desktop URL")
                mobile_url = page.get("content_urls", {}).get("mobile", {}).get("page", "No mobile URL")

    # Append the data to the list
                events_data.append({
                    "Event": events,
                    "Year": year,
                    "Desktop URL": desktop_url,
                    "Mobile URL": mobile_url
                })

    # Create a DataFrame from the collected data
    df = pd.DataFrame(events_data)

    frame = tkinter.Toplevel(window) #this is the new window
    frame.title("EVENTS")
    table = Table(frame, dataframe=df, showtoolbar=True, showstatusbar=True)
    table.show()
def bored(month,day):
    #create a dictionary for the months
    monthDict={'01':'January', '02':'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July', '08':'August', '09':'September', '10':'October', '11':'November', '12':'December'}
    
    #print("Congrats! You have chosen: "+monthDict[month]+" "+ day+". Now it is time to find what happened on this day!")
    url = f'https://en.wikipedia.org/api/rest_v1/feed/featured/2024/{month}/{day}'
    headers = {
        'User-Agent': 'ValentinoBot/1.0'
    }
    response = requests.get(url,headers=headers) 
    data = response.json()
 
    image_of_the_day = data['image']['image']['source']
    webbrowser.open(image_of_the_day)
    image_descrip = data['image']['description']['text']
    window.iconify()
    time.sleep(3)
    messagebox.showinfo("Today's Image", "About today's image: "+image_descrip)

def bored_window():
    month = month_entry.get()
    day = date_entry.get()
    my_date = choose_date(month,day)
    bored(my_date[0],my_date[1])
def holiday_window():
    month = month_entry.get()
    day = date_entry.get()
    my_date = choose_date(month,day)
    holiday_find(my_date[0],my_date[1])
def birth_window():
    month = month_entry.get()
    day = date_entry.get()
    my_date = choose_date(month,day)
    birth_find(my_date[0],my_date[1])
def event_window():
    month = month_entry.get()
    day = date_entry.get()
    my_date = choose_date(month,day)
    event_find(my_date[0],my_date[1])

def erase(e):
    month_entry.set("")
def erase_2(e):
    date_entry.set("")
def reset(e):
    month_entry.set("Please enter the month formatted as a 2-digit number (i.e. "+ "'01'" + "for 'January,'"+  "'02'" + "for 'February,' etc,) ")
    date_entry.set("Please enter the day formatted as a 2-digit number (i.e. "+ "'01' " + "for 'January 1st,'"+  " '02' " + "for 'January 2nd,' etc.) ")
def exit_application():
    msg_box = tkinter.messagebox.askquestion('Exit', 'Are you sure you want to exit the application?',
                                        icon='warning')
    if msg_box == 'yes':
        window.destroy()
        sys.exit()
    else:
        pass

if __name__ == "__main__":

    
    window = tkinter.Tk()

    color = "#5041a6"
    window.geometry("1000x450")
    window.title("Wiki Info Finder!")
    window['background']=  color
    window.resizable(width=0,height=0)
    canvas= tkinter.Canvas(window, width=1000, height=450,bg=color)
    canvas.pack()
    
    tkinter.Label(window, text = "Let's have some fun and find out what happened today!",fg="white",bg=color,font="Verdana 20 bold").place(x=30, y= 0)
    q1 = tkinter.Label(window, text = "What month?",fg="white",bg=color,font= "Helvetica 14 bold").place(x = 30,y = 50)  
    month_entry= tkinter.StringVar(value="Please enter the month formatted as a 2-digit number (i.e. "+ "'01' " + "for 'January,'"+  " '02' " + "for 'February,' etc.) ")
    q1 = tkinter.Label(window, text = "What day?",fg="white",bg=color,font= "Helvetica 14 bold").place(x = 30,y = 135)  
    date_entry= tkinter.StringVar(value="Please enter the day formatted as a 2-digit number (i.e. "+ "'01' " + "for 'January 1st,'"+  " '02' " + "for 'January 2nd,' etc.) ")
    e1 = tkinter.Entry(window,width=120,textvariable=month_entry,font=('Times New Roman', 12,'bold'))
    e1.place(x = 30, y = 85)
    e2 = tkinter.Entry(window,width=120,textvariable=date_entry,font=('Times New Roman', 12,'bold'))
    e2.place(x = 30, y = 170)
   
    boredbutton = tkinter.Button(window, text = "I am bored!",command=bored_window,fg=color,bg="white",activeforeground="white",activebackground=color,font="Helvetica 10 bold").place(x=30,y=215)
    birthbutton = tkinter.Button(window, text = "Who was born today?",command=birth_window,fg=color,bg="white",activeforeground="white",activebackground=color,font="Helvetica 10 bold").place(x=230,y=215)
    eventbutton = tkinter.Button(window, text = "What happened today?",command=event_window,fg=color,bg="white",activeforeground="white",activebackground=color,font="Helvetica 10 bold").place(x=430,y=215)
    holidaybutton = tkinter.Button(window, text = "What can I celebrate?",command=holiday_window,fg=color,bg="white",activeforeground="white",activebackground=color,font="Helvetica 10 bold").place(x=630,y=215)
    exitbutton = tkinter.Button(window, text = "Close this window and exit the application!",command=exit_application,fg=color,bg="white",activeforeground="white",activebackground=color,font="Helvetica 10 bold").place(x=30,y=300)
    wiki = ImageTk.PhotoImage(Image.open("C:\\Users\svalentino\Downloads\wiki.jpg"))
    tkinter.Label(image=wiki).place(x=350,y=260)
    tkinter.Label(window,text="By Steven Valentino",fg="white",bg=color,font= "Helvetica 14 bold").place(x=750,y=300)
    clicked = e1.bind('<Button-1>', erase)
    clicked_2 = e2.bind('<Button-1>', erase_2)
    canvas.bind('<Button-1>', reset)

    window.protocol('WM_DELETE_WINDOW', exit_application)
    icon=ImageTk.PhotoImage(file="C:\\Users\svalentino\Downloads\wiki-icon.ico")
    window.iconphoto(True,icon)
    
    window.mainloop()
