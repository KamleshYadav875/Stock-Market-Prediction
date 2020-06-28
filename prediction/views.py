from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AddToken
from yahoo_fin.stock_info import *
import numpy as np
import pandas as pd
from datetime import date, timedelta
import pandas_datareader as dr
from fbprophet import Prophet
import pandas_datareader as dr
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
import tensorflow as tf
import math
from sklearn.metrics import mean_squared_error
import numpy

def indexPage(request):
    return render(request, 'prediction/indexPage.html')

def about(request):
    return render(request, 'prediction/about.html')

def aboutUs(request):
    return render(request, 'admin/about.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('adminhome')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username= username,password= password)
            if user is not None:
                login(request, user)
                return redirect('adminhome')
            else:
                messages.info(request, 'Username OR password is incorrect')
        
    contest = {}
    return render(request, 'prediction/loginPage.html', contest)

@login_required(login_url='loginPage')
def adminHome(request):
    dropdowntoken = AddToken.objects.all()
    contest = {'tokens':dropdowntoken}
    return render(request, 'admin/adminHome.html', contest)


def logoutUser(request):
    logout(request)
    return redirect("indexPage")


    
def predict(request):
    dropdowntoken = AddToken.objects.all()
    context = {'tokens':dropdowntoken}
    if request.method == 'POST':
        token = request.POST.get('comp')
        df  = dr.data.get_data_yahoo(token, start=(date.today()) - timedelta(days=1080),end=date.today())
        index = df.index.tolist()
        df.reset_index(drop=True, inplace=True)
        df['Date'] = index
        x = (df['Date'].dt.strftime('%Y-%m-%d')).tolist()
        y = df['Close'].tolist()

        
        dataset = df[["Date", "Close"]]
        dataset = dataset.rename(columns={"Date":"ds", "Close":"y"})
        dataset["y"] = np.log(dataset["y"])
        dataset["y"] = np.sqrt(dataset["y"])
        m = Prophet()
        m.fit(dataset)
        future = m.make_future_dataframe(periods=10,freq='D', include_history=True)
        forcast = m.predict(future)
        forcast[["yhat","yhat_lower","yhat_upper"]] = np.square(forcast[["yhat","yhat_lower","yhat_upper"]])
        forcast[["yhat","yhat_lower","yhat_upper"]] = np.exp(forcast[["yhat","yhat_lower","yhat_upper"]])
        x_next_ten_Day = forcast['ds'].tail(10)
        y_next_ten_day = forcast['yhat'].tail(10)
        # print(y_next_ten_day)
        n = []
        pre = []
        for i in range(1,11):
            d = ((date.today()) + timedelta(days=i))
            n.append(d.strftime('%Y-%m-%d'))
        for i in y_next_ten_day:
            pre.append(i)
        


        context = { 'x':x, 'y':y,'t':token, 'tokens':dropdowntoken,'n':n ,'pre':pre}
    return render(request, 'admin/prediction.html', context)


def upredict(request):
    dropdowntoken = AddToken.objects.all()
    context = {'tokens':dropdowntoken}
    if request.method == 'POST':
        token = request.POST.get('comp')
        df  = dr.data.get_data_yahoo(token, start=(date.today()) - timedelta(days=1080),end=date.today())
        index = df.index.tolist()
        df.reset_index(drop=True, inplace=True)
        df['Date'] = index
        x = (df['Date'].dt.strftime('%Y-%m-%d')).tolist()
        y = df['Close'].tolist()

        
        dataset = df[["Date", "Close"]]
        dataset = dataset.rename(columns={"Date":"ds", "Close":"y"})
        dataset["y"] = np.log(dataset["y"])
        dataset["y"] = np.sqrt(dataset["y"])
        m = Prophet()
        m.fit(dataset)
        future = m.make_future_dataframe(periods=10,freq='D', include_history=True)
        forcast = m.predict(future)
        forcast[["yhat","yhat_lower","yhat_upper"]] = np.square(forcast[["yhat","yhat_lower","yhat_upper"]])
        forcast[["yhat","yhat_lower","yhat_upper"]] = np.exp(forcast[["yhat","yhat_lower","yhat_upper"]])
        x_next_ten_Day = forcast['ds'].tail(10)
        y_next_ten_day = forcast['yhat'].tail(10)
        # print(y_next_ten_day)
        n = []
        pre = []
        for i in range(1,11):
            d = ((date.today()) + timedelta(days=i))
            n.append(d.strftime('%Y-%m-%d'))
        for i in y_next_ten_day:
            pre.append(i)
        


        context = { 'x':x, 'y':y,'t':token, 'tokens':dropdowntoken,'n':n ,'pre':pre}
    return render(request, 'prediction/prediction.html', context)



def addtoken(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        tk = request.POST.get('token')
        add = AddToken(token = tk, name = name)
        add.save()
        return redirect('addtoken')
    return render(request , 'admin/addtoken.html')


def viewdata(request):
    dropdowntoken = AddToken.objects.all()
    df = None
    if request.method == "POST":
        token = request.POST.get('comp')
        df  = dr.data.get_data_yahoo(token, start=(date.today()) - timedelta(days=360),end=date.today())
    df = pd.DataFrame(df)
    df.index = pd.to_datetime(df.index)
    df  = df.round(3)

    contest = {'tokens':dropdowntoken, 'df':df}
    return render(request, 'admin/viewdata.html', contest)