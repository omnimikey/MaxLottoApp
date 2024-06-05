import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import statistics

import matplotlib.pyplot as plt





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
firstGraph.plot(x="months", y=["jackpot"], kind="kde")
plt.show()
graph_fig = firstGraph.get_figure() 
  
# use savefig function to save the plot and give a desired name to the plot. 
plt.savefig('my_plot1.png')
plt.close()
#print(firstGraph)

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

print(freq_frid_played(100))


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

    print(all_avg)

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

def find_min(arr):
    min=arr[0]

    for i in range(0, len(arr)):
        if (arr[i] < min):
            min=arr[i]
    return min     

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
    return (statistics.mean(perc))
    #return count

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

        
    
    
    













