import requests
import lxml.html as lh
import pandas as pd

def scrape():
    url='https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=50430&Year=2021&Month=2&Day=13'
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')

    #Create empty list
    col=[]
    i=0
    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        i+=1
        name=t.text_content()
        col.append((name,[]))

    #Since out first row is the header, data is stored on the second row onwards
    for j in range(1,len(tr_elements)):
        #T is our j'th row
        T=tr_elements[j]
        
        #If row is not of size 12, the //tr data is not from our table 
        if len(T)!=12:
            break
        
        #i is the index of our column
        i=0
        
        #Iterate through each element of the row
        for t in T.iterchildren():
            data=t.text_content() 
            #Check if row is empty
            if i>0:
            #Convert any numerical value to integers
                try:
                    data=int(data)
                except:
                    pass
            #Append the data to the empty list of the i'th column
            col[i][1].append(data)
            #Increment i for the next column
            i+=1

    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    df = df.iloc[:-5,8 ]
    precipitations = df.tolist()
    for x in range(len(precipitations)):
        try:
            precipitations[x] = float(precipitations[x])
        except ValueError:
            precipitations[x] = 0.0
    precipitations = [(x, precipitations[x-1]) for x in range(1,len(precipitations)+1)]
    return precipitations

