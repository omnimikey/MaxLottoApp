import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
import statistics
from math import sin


from kivy.uix.floatlayout import FloatLayout
from kivy_garden.graph import Graph, LinePlot, MeshLinePlot, MeshStemPlot

import matplotlib
matplotlib.use("module://kivy.garden.matplotlib.backend_kivy")
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvas, NavigationToolbar2Kivy, FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.uix.pagelayout import PageLayout
from kivymd.uix.button import MDFillRoundFlatIconButton, MDFillRoundFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


"""

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

lotto_list =[]
years = list(range(2009,2025))
url = "https://www.lottomaxnumbers.com/numbers/"

for i in range(0, len(years)):
    url = url + str(years[i])
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    url = url.removesuffix(str(years[i]))



    #finding parent <ul> tag with class=balls
    lott_parent=soup.findAll('ul', class_ = "balls")
    list_lott=[]
    temp_lott=[]


    #finds lotto draw results including the bonus number
    for lott in lott_parent:
        for li in lott.findAll('li'):
            list_lott.append(li.text)
        temp_lott.append(list_lott)
        list_lott = []

    temp_lott = temp_lott[::-1]

    months = ["January", "February", "March", "April", "May","June", "July", "August","September","October","November","December"]


    #find all dates 
    date_parent =  soup.findAll('a')
    dates=[]
    for date in date_parent:
        date_3=date.text
        date_4=date_3.split(" ")
        if (date_4[0] in months):
            dates.append(date_4)
    dates = dates[::-1]

    jackpot_parent = soup.findAll('td', class_="jackpot")
    jackpot_l=[]
    for jack in jackpot_parent:
        temp = jack.text[0:11]
        temp = temp.replace(",", "")
        temp = temp.replace("$", "")
        jackpot_l.append(temp)
    jackpot_l= jackpot_l[::-1]

    class Rollout:
        def __init__(self, date, sequence, jackpot):
            self.date = date
            self.sequence = sequence
            self.jackpot = jackpot


    

    for num in range(0,len(jackpot_l)):
        lotto_archive = {
        'date' : dates[num],
        'sequence' : temp_lott[num],
        'jackpot' : jackpot_l[num],
        
        }
        
        lotto_list.append(lotto_archive)
    

#for i in range(0, len(lotto_list)):
#    print(lotto_list[i].values())


print(len(lotto_list))

#convert into json
#file name is lottoJson

with open("lottoJson", "w") as final:
    json.dump(lotto_list, final)

#download the json file
#google.collab.download('lottoJson.json')
"""

file = open('lottoJson')

data = json.load(file)
count=0
df=pd.DataFrame(data)
#for i in range(0,len(data)):
#    print(data[i]['jackpot'])

file.close()


#print(df['jackpot'])

#will analyze frequence of jackpot wins


#Filter that changes Sequence and Jackpot columns from  strings to numbers
dataframe = pd.DataFrame(df, columns=["date","sequence","jackpot"])
jackpot_col =  dataframe['jackpot'].apply(pd.to_numeric)
sequence_col = dataframe['sequence'].apply(pd.to_numeric)
dataframe['jackpot'] = jackpot_col
dataframe['sequence'] = sequence_col

friday = dataframe[['date','sequence','jackpot']][::2]
tuesday = dataframe[['date','sequence','jackpot']][503::2]


#Filter that changes Sequence and Jackpot columns from  strings to numbers
dataframe = pd.DataFrame(df, columns=["date","sequence","jackpot"])
jackpot_col =  dataframe['jackpot'].apply(pd.to_numeric)
sequence_col = dataframe['sequence'].apply(pd.to_numeric)
dataframe['jackpot'] = jackpot_col
dataframe['sequence'] = sequence_col

friday = dataframe[['date','sequence','jackpot']][::2]
tuesday = dataframe[['date','sequence','jackpot']][503::2]

#Data for graphs
dataframe['years'] = dataframe['date'].apply(lambda x: list(x)[2]).apply(pd.to_numeric)    #years
dataframe['months']=dataframe['date'].apply(lambda x: list(x)[0])     #months
dataframe['one'] = dataframe['sequence'].apply(lambda x: list(x)[0])  #sequence[0]
dataframe['two'] = dataframe['sequence'].apply(lambda x: list(x)[1])  #sequence[1]
dataframe['three'] = dataframe['sequence'].apply(lambda x: list(x)[2])  #sequence[2]
dataframe['four'] = dataframe['sequence'].apply(lambda x: list(x)[3])  #sequence[3]
dataframe['five'] = dataframe['sequence'].apply(lambda x: list(x)[4])  #sequence[4]
dataframe['six'] = dataframe['sequence'].apply(lambda x: list(x)[5])  #sequence[5]
dataframe['seven'] = dataframe['sequence'].apply(lambda x: list(x)[6])  #sequence[6]

firstGraph= dataframe[dataframe['years'] == 2010]
#firstGraph.plot(x="months", y=["jackpot"], kind="kde")

fig, ax = plt.subplots()

canvas = fig.canvas



def freq_tues_played(num):
    count=0
    i=503
    leng = len(dataframe['sequence'])
    while ( i < leng):
        if (num in tuesday['sequence'][i]):
            count = count + 1
        i=i+2
    percent = count / len(tuesday['sequence']) * 100
    percent = round(percent,1)
    return percent

def freq_frid_played(num):
    count=0
    i=0
    
    leng = len(dataframe['sequence'])
    while ( i < leng):
        if (num in friday['sequence'][i]):
            count = count + 1
        i=i+2
    percent = count / len(friday['sequence']) * 100
    percent = round(percent,1)
    return percent

"""
def freq_jackpot(arr):
    count=0
    temp = arr[count]
    

    for i in range(1,len(arr)):
        if (arr[i] < arr[i-1]):
            count= count + 1
            max = arr[i]
    return count

total_wins = freq_jackpot(df['jackpot'])  # counts the total times a person won the lottery since 2009
win_percent = total_wins / len(df.index) * 100
#print(str(win_percent)[:4] + '%') #prints the percentage of times there is a jackpot winner
"""


#count amount of times a number has been played since 2009
lotto_num_count = list(range(1,51))


def freq_num_played(num):
    count=0
    for i in range(0,len(df['sequence'])):
        if (num in df['sequence'][i]):
            count= count + 1
    return count

#print(freq_num_played(str(30)))
     


#Times a sequence of numbers has been played and gives the average percentage of the averages of each number being played
def times_played(arr):
    count = 0
    for i in range(0, len(df['sequence'])):
        if (arr == df['sequence'][i]):
            count = count + 1

    perc=[]
    for i in range(0, len(arr)):
        percent = freq_num_played(str(arr[i])) / len(df['sequence'])
        perc.append(percent)
    #return (statistics.mean(perc))
    return count

def times_played2(arr):
    count = 0
    keep = 0
    for i in range(0, len(df['sequence'])):
        keep=df['sequence'][i].pop()
        if (arr == df['sequence'][i]):
            count = count + 1
        df['sequence'][i].append(keep)

    perc=[]
    for i in range(0, len(arr)):
        percent = freq_num_played(str(arr[i])) / len(df['sequence'])
        perc.append(percent)
    #return (statistics.mean(perc))
    return count

#pl = times_played([str(22),str(24),str(31),str(33),str(39),str(45),str(46),str(2)])
#print(pl)

#function that gives average of all numbers from the position order

def order_avg():
    all_avg =[]
    summer=0
    avg=0
    total_length = len(dataframe['sequence'])
    seq_length =  len(dataframe['sequence'][0])

    for j in range(0, seq_length):
        for i in range(0,total_length):
            summer += dataframe['sequence'][i][j]
        avg = int(round(summer / total_length, 0))
        all_avg.append(avg)
        summer=0
        avg = 0

    return all_avg

#Displays the n amount of max numbers
def most_common(num):
    common= []
    counts=[]
    
    for i in range(1, 51):
        counts.append(freq_num_played(str(i)))
    
    for i in range(0,num):
        if (num <= 10):
            max1 = (max(counts))
            index1 = counts.index(max1)
            common.append(index1+1) #enters max number into list using index
            counts[index1]=0
    
    return(common)


class Box5(GridLayout):
    count=0
    my_text = StringProperty()     #string property
    curr_state = StringProperty()
    prob_input = StringProperty()
    curr_state="OFF"

    def on_button_click(self):
        if (self.curr_state == "ON"):
            self.prob_input = self.ids.prob_pct.text
            self.my_text = str(freq_tues_played(int(self.prob_input))) + "%"
        else:
            self.prob_input = self.ids.prob_pct.text
            self.my_text = str(freq_frid_played(int(self.prob_input))) + "%" 

    def on_toggle_button_state(self, widget):
        print("toggle state" + widget.state)
        if widget.state == "normal":
            widget.text = "TUESDAY"
            self.curr_state = "OFF"
        else:
            #ON
            widget.text = "FRIDAY"
            self.curr_state="ON"

class Box1(BoxLayout):  

    my_text = StringProperty() #string property
    amount1 = StringProperty()
    output1 = StringProperty()

    def on_amount_num(self):
        self.amount1 = self.ids.amount_num.text
        self.output1 = str(freq_num_played(self.amount1))

class Box2(BoxLayout):

    seq1 = ObjectProperty(None)
    seq2 = ObjectProperty(None)
    seq3 = ObjectProperty(None)
    seq4 = ObjectProperty(None)
    seq5 = ObjectProperty(None)
    seq6 = ObjectProperty(None)
    seq7 = ObjectProperty(None)
    seq8 = ObjectProperty(None)

    seq_num = StringProperty()
    count_seq1 = StringProperty()
    seq_array = []
    
    def on_sequence_num(self):
        self.seq_array.append(int(self.seq1.text))
        self.seq_array.append(int(self.seq2.text))
        self.seq_array.append(int(self.seq3.text))
        self.seq_array.append(int(self.seq4.text))
        self.seq_array.append(int(self.seq5.text))
        self.seq_array.append(int(self.seq6.text))
        self.seq_array.append(int(self.seq7.text))
        self.seq_array.sort()
        self.seq_array = list(map(str, self.seq_array))

        self.seq_array.append(self.seq8.text)

        self.count_seq1 = str(times_played(self.seq_array))
        self.seq_array=[]
    
    def on_sequence_num1(self):
        self.seq_array.append(int(self.seq1.text))
        self.seq_array.append(int(self.seq2.text))
        self.seq_array.append(int(self.seq3.text))
        self.seq_array.append(int(self.seq4.text))
        self.seq_array.append(int(self.seq5.text))
        self.seq_array.append(int(self.seq6.text))
        self.seq_array.append(int(self.seq7.text))
        self.seq_array.sort()
        self.seq_array = list(map(str, self.seq_array))

        self.count_seq1 = str(times_played2(self.seq_array))
        self.seq_array=[]

class Box3(BoxLayout):
    
    all_averages = StringProperty()
    temp_avg = StringProperty()
    all_avg_array = []

    def average_all(self):
        self.all_averages=""
        self.temp_avg = ""
        self.all_avg_array = order_avg()

        for i in range (0, len(self.all_avg_array) -1):
            self.temp_avg += f"{self.all_avg_array[i]}, "
        
        self.temp_avg = self.temp_avg + f"Bonus: {self.all_avg_array[7]}"
    
        self.all_averages = self.temp_avg

class Box4(BoxLayout):

    show_nums = StringProperty()
    enter_num = StringProperty()
    most_comm = StringProperty()
    common_array2=[]

    def all_common(self):
        self.enter_num = self.ids.recur_len.text
        self.common_array2 = most_common(int(self.enter_num))

        for i in range(0, len(self.common_array2)):
            if (i < len(self.common_array2)-1):
                self.show_nums += f"{str(self.common_array2[i])}, "
            else:
                self.show_nums += f"{str(self.common_array2[i])}"

        self.most_comm = self.show_nums 
        self.show_nums = ""
        self.common_array2=[]

class Box6(BoxLayout):

    prob1 = ObjectProperty(None)
    prob2 = ObjectProperty(None)
    prob3 = ObjectProperty(None)
    prob4 = ObjectProperty(None)
    prob5 = ObjectProperty(None)
    prob6 = ObjectProperty(None)
    prob7 = ObjectProperty(None)

    slider1 =  StringProperty()
    slider1_lbl = StringProperty()
    slider1_prob = StringProperty()
    slider2 =  StringProperty()
    slider2_lbl = StringProperty()
    slider2_prob = StringProperty()
    slider3 =  StringProperty()
    slider3_lbl = StringProperty()
    slider3_prob = StringProperty()
    slider4 =  StringProperty()
    slider4_lbl = StringProperty()
    slider4_prob = StringProperty()
    slider5 =  StringProperty()
    slider5_lbl = StringProperty()
    slider5_prob = StringProperty()
    slider6 =  StringProperty()
    slider6_lbl = StringProperty()
    slider6_prob = StringProperty()
    slider7 =  StringProperty()
    slider7_lbl = StringProperty()
    slider7_prob = StringProperty()
    total_probability =  StringProperty()
    dat_length = len(dataframe['sequence'])
    mult= NumericProperty()
    mult1= NumericProperty()
    mult2= NumericProperty()
    mult3= NumericProperty()
    mult4=NumericProperty()
    mult5=NumericProperty()
    mult6=NumericProperty()
    init_arr=[False, False, False, False, False, False, False]

    def tot_prob(self):
        
        self.mult = (freq_num_played(str(int(self.prob1.text)))/self.dat_length)
        self.mult1 = (freq_num_played(str(int(self.prob2.text)))/self.dat_length)
        self.mult2 = (freq_num_played(str(int(self.prob3.text)))/self.dat_length)
        self.mult3 = (freq_num_played(str(int(self.prob4.text)))/self.dat_length)
        self.mult4 = (freq_num_played(str(int(self.prob5.text)))/self.dat_length)
        self.mult5 = (freq_num_played(str(int(self.prob6.text)))/self.dat_length)
        self.mult6 = (freq_num_played(str(int(self.prob7.text)))/self.dat_length)
        self.total_probability = str((self.mult * self.mult1 * self.mult2 * self.mult3 * self.mult4 * self.mult5 * self.mult6) * 100) + "%"


    def on_slider_value1(self, widget):
        
        print("Slider: " + str(int(widget.value)))
        self.slider1_lbl = str(int(widget.value))
        self.slider1_prob = str(round((freq_num_played(str(int(widget.value)))/self.dat_length),2)*100) + "%"
        
        self.init_arr[0]=True
        if (False not in self.init_arr):
            self.tot_prob()
        


    def on_slider_value2(self, widget):
        print("Slider: " + str(int(widget.value)))
        self.slider2_lbl = str(int(widget.value))
        self.slider2_prob = str(round((freq_num_played(str(int(widget.value)))/self.dat_length),2)*100) + "%"
        self.init_arr[1]=True
        if (False not in self.init_arr):
            self.tot_prob()
        

    def on_slider_value3(self, widget):
        print("Slider: " + str(int(widget.value)))
        self.slider3_lbl = str(int(widget.value))
        self.slider3_prob = str(round((freq_num_played(str(int(widget.value)))/self.dat_length),2)*100) + "%"
        self.init_arr[2]=True
        if (False not in self.init_arr):
            self.tot_prob()

    def on_slider_value4(self, widget):
        print("Slider: " + str(int(widget.value)))
        self.slider4_lbl = str(int(widget.value))
        self.slider4_prob = str(round((freq_num_played(str(int(widget.value)))/self.dat_length),2)*100) + "%"  
        self.init_arr[3]=True
        if (False not in self.init_arr):
            self.tot_prob()


    def on_slider_value5(self, widget):
        print("Slider: " + str(int(widget.value)))
        self.slider5_lbl = str(int(widget.value))
        self.slider5_prob = str(round((freq_num_played(str(int(widget.value)))/self.dat_length),2)*100) + "%"
        self.init_arr[4]=True
        if (False not in self.init_arr):
            self.tot_prob()

    def on_slider_value6(self, widget):
        print("Slider: " + str(int(widget.value)))
        self.slider6_lbl = str(int(widget.value))
        self.slider6_prob = str(round((freq_num_played(str(int(widget.value)))/self.dat_length),2)*100) + "%"
        self.init_arr[5]=True
        if (False not in self.init_arr):
            self.tot_prob()

    def on_slider_value7(self, widget):
        print("Slider: " + str(int(widget.value)))
        self.slider7_lbl = str(int(widget.value))
        self.slider7_prob = str(round((freq_num_played(str(int(widget.value)))/self.dat_length),2)*100) + "%"
        self.init_arr[6]=True
        if (False not in self.init_arr):
            self.tot_prob()

class BoxLayoutExample(BoxLayout):
    pass 

# Create Tabbed class  
class Tab(TabbedPanel): 
    pass

class GraphLayout(BoxLayout):


    def gnrt_graph(self):

        
        self.x_values = self.ids.x_value.text
        self.y_values = self.ids.y_value.text


        x_vl = self.x_values
        y_vl = self.y_values
        x=dataframe[x_vl]
        y=dataframe[y_vl]



        #firstGraph.plot(x="months", y=["jackpot"], kind="kde")
        plt.plot(x,y)
        plt.grid()

        canvas = FigureCanvasKivyAgg(plt.gcf())
        self.bx = self.ids.bx
        self.nav = NavigationToolbar2Kivy(canvas)

        self.bx.add_widget(self.nav.actionbar)
        self.bx.add_widget(canvas)

class MainWindow(Screen):
    pass

class SecondWindow(Screen):
    pass

class ThirdWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class TheLabApp2(MDApp):
    pass

class HomePage(BoxLayout):
    pass

    
TheLabApp2().run()













