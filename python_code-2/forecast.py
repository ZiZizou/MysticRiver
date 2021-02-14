import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet


def create_and_train(data):
    #defining the model
    model = Prophet(interval_width=0.95, daily_seasonality=True)
    #fitting the model
    model.fit(data)
    return model



def predict(m, future):
    forecast = m.predict(future)
    m.plot(forecast)
    plt.suptitle('River Level Prediction (Blue line) vs Time')
    plt.xlabel('Time')
    plt.ylabel('River Level')
    plt.show()