from numpy.core.einsumfunc import _update_other_results
import pandas as pd
import forecast
import processing
from fbprophet import Prophet
import matplotlib.pyplot as plt
from tkinter import *


#important running information - defaults
station_names = ['Elbow River at Bragg Creek', 'Elbow River at Sarcee Bridge',
 'Glenmore Reservoir at Calgary' ,'Elbow River below Glenmore Dam',
 'Bow River at Calgary', 'Jumpingpound Creek at Township Road 252',
 'Bearspaw Reservoir near Calgary']
update = True
selection  = 'Glenmore Reservoir at Calgary'
update = True
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

def plot(start_d, stop_d, start_m, stop_m, update, results = 2000000, data_plot_cond = True ):
    data_df = processing.get_data(selection, update, results)
    if(update):
        update = False
    model = forecast.create_and_train(data_df)
    if(data_plot_cond):
        data_df.plot(x ='ds', y='y', kind = 'line')
        plt.suptitle('River Levels vs Time')
        plt.show()

    forecast.predict(model, range_gen(start_m,stop_m,start_d,stop_d))

def submit():
    try:
        start_d = int(textentry1.get())
        stop_d = int(textentry2.get())
        start_m = int(textentry3.get())
        stop_m = int(textentry4.get())
        update = bool(textentry4.get())
        if(textentry6.get() not in station_names):
            raise('Invalid input for station name')
        else:
            selection = textentry6.get()
        plot(start_d, stop_d, start_m, stop_m, update)
    except TypeError:
        print('Invalid input')
    pass

#-----------------------------------------------------------

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

Label(window, text = 'Enter 1 to update to most recent values, nothing to leave it as is',bg = 'black',fg = 'white').grid(row=7, column=0, sticky=W)
textentry5 = Entry(window, width=20, bg = 'white')
textentry5.grid(row = 7, column =1)

Label(window, text = 'Enter a station name from the following - ',bg = 'black',fg = 'white').grid(row=8, column=0, sticky=W)
textentry6 = Entry(window, width=20, bg = 'white')
textentry6.grid(row = 9, column =1)
Label(window, text = """'Elbow River at Bragg Creek', 'Elbow River at Sarcee Bridge',
 'Glenmore Reservoir at Calgary' ,'Elbow River below Glenmore Dam',
 'Bow River at Calgary', 'Jumpingpound Creek at Township Road 252',
 'Bearspaw Reservoir near Calgary'""",bg = 'black',fg = 'white').grid(row=10, column=0, sticky=W)

Button(window, text = 'SUBMIT', width = 6, command = submit).grid(row = 11, column=0)

window.mainloop()

print('Desecration Smile :)')