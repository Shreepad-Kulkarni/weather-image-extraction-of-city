
from tkinter import *
from PIL import Image,ImageTk
import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
import cv2
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
import urllib.request

#main window

win=Tk()
win.title('weather')

col='sky blue'
win.configure(background=col)

#pics
weather_image=ImageTk.PhotoImage(Image.open('weather.jpg'))
rock_image=ImageTk.PhotoImage(Image.open('rock.jpg'))

#insert pics
weather_label=Label(win,image=weather_image)

#grid
weather_label.grid(row=1,column=4)



def graphs():
    win.config(bg='grey')
   
    #  Image searching & downloading
    prefix='https://www.google.com/search?q='
    suffix='&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjUqrKjkMz1AhVyr1YBHR5uA-gQ_AUoAnoECAIQBA&biw=1366&bih=657&dpr=1'
    query=entry1.get()
    link=prefix+query+suffix

    n=3  #no of images to be saved
    driver=webdriver.Chrome()
    driver.get(link)

    # Sample XPATH of few images
    #//*[@id="islrg"]/div[1]/div[6]/a[1]/div[1]/img
    #//*[@id="islrg"]/div[1]/div[13]/a[1]/div[1]/img

    #creating folder with name same as of city
    folder_name="%s"%query
    if not os.path.exists(folder_name):
            os.mkdir(folder_name)
    for i in range(1,n+1):
        img=driver.find_element(By.XPATH,"""//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img"""%i)
        src=img.get_attribute("src")
    
        file_path=os.path.join("C:\\Users\\enter your folder address%s"%folder_name,'image_(%s).png'%i)
        urllib.request.urlretrieve(src,file_path)
    print('Download Complete')
    
    def showimg(city):
        path='C:\\Users\\enter your folder address'
        for img in glob.glob(path+f'{city}'+'\\*.png'):
            cv_img=cv2.imread(img)
    
            rock_label=Label(win,image=cv_img)
            rock_label.place(in_=weather_label,rely=0.3,relx=0.7)
    showimg(city)
   
#show image button
def graph_button():
    global next_
    next_ =Button(win,text='Show Images',command=graphs)
    next_.place(in_=weather_label,relx=0.3,rely=0.9)
graph_button()

def button_command():
    global data
    data =entry1.get()
    print(data)
    info(data)

#button to type text
entry1=Entry(win,width=20)
entry1.place(in_=weather_label,relx=0.3,rely=0.5,anchor='c')
search=Button(win,text='Search',width=20,height=2,bg='deep sky blue',command=button_command)
search.place(in_=weather_label,relx=0.5,rely=0.5,anchor='c')  #relx & rely to keep search at centre

#weather api
def info(data):
    global city
    city=data
    # creating url and requests instance
    url = "https://www.google.com/search?q="+"weather"+city
    html = requests.get(url).content

    # getting raw data
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

    # formatting data
    data = str.split('\n')
    time = data[0]
    sky = data[1]

    # getting all div tag
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text

    # getting other required data
    pos = strd.find('Wind')
    other_data = strd[pos:]

    # printing all data
    print("Current Weather of {} is ".format(city))
    print("Temperature is", temp)
    print("Time: ", time)
    print("Sky Description: ", sky)
    print(other_data)
    all_info =" Current weather of {}\nTemperature is {} \n Time:{}\n sky discription:{}".format(city,temp,time,sky,other_data)
    
    #button to display all collected info
    txt_button=Button(win,text=all_info,width=40,height=4,bg='deep sky blue')
    txt_button.place(in_=weather_label,relx=0.4,rely=0.7,anchor='c') 

win.mainloop()