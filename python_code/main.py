from numpy.core.einsumfunc import _update_other_results
import pandas as pd
import forecast
import processing
import precipitation
from fbprophet import Prophet
import matplotlib.pyplot as plt
from tkinter import *


#important running information - defaults
station_names = ['Elbow River at Bragg Creek', 'Elbow River at Sarcee Bridge',
 'Glenmore Reservoir at Calgary' ,'Elbow River below Glenmore Dam',
 'Bow River at Calgary', 'Jumpingpound Creek at Township Road 252',
 'Bearspaw Reservoir near Calgary']
update_choice = ['update', '']
plot_choice = ['plot', '']
update = True
selection  = 'Glenmore Reservoir at Calgary'
start_m = 1
stop_m = 4
start_d = 1
stop_d = 25
calendar = {1:31, 2:28, 3:31, 4:30, 5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
#

#range_generating functions and testing function
def date_produce(year, month, start_day = 1, end_day = 31):
    future = list()
    if(end_day>calendar[month]):
        end_day = calendar[month]
    for d in range(start_day, end_day+1):
	    date = f'{year}-{month}-%02d' % d
	    future.append([date])
    return future

def range_gen(start_month, stop_month, start_day, stop_day, year = 2021):
    future = []
    future+=date_produce(year, start_month, start_day)
    for m in range(start_month+1, stop_month-1):
        future+=date_produce(year, start_month, start_day)
    future+=date_produce(year, stop_month,1 ,stop_day)
    future = pd.DataFrame(future)
    future.columns = ['ds']
    future['ds']= pd.to_datetime(future['ds'])
    return future


#-----------------------------------------------------------
#Main Code

def plot(start_d, stop_d, start_m, stop_m, update, data_plot_cond, selection,results = 2000000):
    data_df = processing.get_data(selection, update, results)
    if(update):
        update = False
    model = forecast.create_and_train(data_df)
    if(data_plot_cond):
        data_df.plot(x ='ds', y='y', kind = 'line')
        plt.suptitle('River Levels vs Time')
        plt.ylabel('River Level')
        plt.xlabel('Time')
        plt.show()

    forecast.predict(model, range_gen(start_m,stop_m,start_d,stop_d))

def submit():
    try:
        start_d = int(textentry1.get())
        stop_d = int(textentry2.get())
        start_m = int(textentry3.get())
        stop_m = int(textentry4.get())
        update = bool(variable1.get())
        selection = variable2.get()
        plot_cond = variable3.get()
        plot(start_d, stop_d, start_m, stop_m, update,plot_cond,selection)
    except ValueError:
        print('Invalid input')

def ppt_plot():
    ppt_data = precipitation.scrape()
    plt.plot([ppt_data[x][0] for x in range(len(ppt_data))],[ppt_data[x][1] for x in range(len(ppt_data))])
    plt.suptitle('Precipitation Levels from Official Weather Canada Website')
    plt.xlabel('Day in the Current month')
    plt.ylabel('Precipitation in mm')
    plt.show()

#-----------------------------------------------------------
#GUI code

window = Tk()
window.title('River Mystic')
window.configure(background = 'black')

photo1 = PhotoImage(file='./mystic.png')
Label(window, image = photo1,bg = 'black').grid(row=0, column=0, sticky=W)
Label(window, text = 'Enter the details below',bg = 'black',fg = 'white').grid(row=2, column=0, sticky=W)

Label(window, text = 'Start Day',bg = 'black',fg = 'white').grid(row=3, column=0, sticky=W)
textentry1 = Entry(window, width=20, bg = 'white')
textentry1.grid(row = 3, column =1)

Label(window, text = 'End Day',bg = 'black',fg = 'white').grid(row=4, column=0, sticky=W)
textentry2 = Entry(window, width=20, bg = 'white')
textentry2.grid(row = 4, column =1)

Label(window, text = 'Start Month',bg = 'black',fg = 'white').grid(row=5, column=0, sticky=W)
textentry3 = Entry(window, width=20, bg = 'white')
textentry3.grid(row = 5, column =1)

Label(window, text = 'End Month',bg = 'black',fg = 'white').grid(row=6, column=0, sticky=W)
textentry4 = Entry(window, width=20, bg = 'white')
textentry4.grid(row = 6, column =1)

Label(window, text = 'Update choice - (empty string means no update)',bg = 'black',fg = 'white').grid(row=7, column=0, sticky=W)
variable1 = StringVar(window)
variable1.set(update_choice[0])
entry6 = OptionMenu(window, variable1, *update_choice).grid(row=7, column = 1)

Label(window, text = 'Enter a station name from the following - ',bg = 'black',fg = 'white').grid(row=8, column=0, sticky=W)
variable2 = StringVar(window)
variable2.set(station_names[0])
entry7 = OptionMenu(window, variable2, *station_names).grid(row=8, column = 1)

Label(window, text = 'Data plot choice - (empty string means no plot)',bg = 'black',fg = 'white').grid(row=9, column=0, sticky=W)
variable3 = StringVar(window)
variable3.set(plot_choice[0])
entry8 = OptionMenu(window, variable3, *plot_choice).grid(row=9, column = 1)

Button(window, text = 'SUBMIT', width = 6, command = submit).grid(row = 11, column=0)
Button(window, text = 'Precipitation Plot', width = 20, command = ppt_plot).grid(row = 12, column=0)

window.mainloop()

print('Desecration Smile :)')