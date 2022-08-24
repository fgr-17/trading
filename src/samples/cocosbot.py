# -*- coding: utf-8 -*-
"""CocosBot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1obExFe71JgZmfhq_sbgSNeFAftpp-R03
"""

# !pip install pyhomebroker --upgrade --no-cache-dir

from pyhomebroker import HomeBroker
import datetime
import pandas as pd
import requests

"""En esta notebook vamos a mostrar como armar un portfolio de manera programática (usando algun criterio) y comprarlo. Además, mostramos código para rebalancear. La estrategia que elegimos es una forma de 1/N. Es una estretegia sencilla que suele usarse como baseline. (Esto no es una recomendacion de compra ni nada por el estilo, solamente tiene fines didácticos y busca mostrar como operar usando python).
El código está hecho para ser mas claro que performante: puede optimizarse mucho, pero esta es la forma mas clara que encontré de explicarlo.
"""

#Primero me conecto a cocos capital usando pyhomebroker.

codigo_broker = 265 # cocos capital

dni_cuenta = 123456 # tu dni
user_cuenta = 'usuario' # tu nombre de usuario
user_password = 'password' # tu contraseña
comitente = 11111 # tu comitente

## homebroker 265 es cocos capital
hb = HomeBroker(codigo_broker)

## log in: aca usar las credenciales propias
hb.auth.login(dni=dni_cuenta, user=user_cuenta, password=user_password, raise_exception=True)
hb.online.connect()

"""Vamos a definir una estrategia de tipo 1/N. Voy a setear un monto de plata a invertir en el portfolio (capital) y voy a dividir esa plata entre un numero predefinido de acciones (en este caso 10). 
Voy a usar plazo de liquidacion de 48 hs.

¿Como voy a elegir esas 10 acciones? De una forma pava: calculo la mediana de la distribucion de retornos en los ultomos n_dias (60 acá) y lo divido por el mad. Los ordeno de mayor a menor y tomo el top 10. Nada muy loco ni muy elaborado. Es solo para probar como funciona la conexion.
"""

n_dias = 60
n_assets = 10
capital = 50000
plazo = '48hs'

## voy a elegir entre los tickers del panel lider, pero podriamos extenderlo
tickers = [
    "ALUA", "BBAR", "BMA", "BYMA",
    "CEPU", "COME", "CRES", "CVH",
    "EDN", "GGAL", "HARG", "LOMA",
    "MIRG", "PAMP", "SUPV", "TECO2",
    "TGNO4", "TGSU2", "TRAN", "TXAR",
    "VALO", "YPFD"
]

## algunas funciones auxiliares: 

def ticker_get_data(hb, ticker, n_dias):
    ''' Toma una lista de tickers y un objeto homebroker y 
        busca los precios desde hoy hasta n_dias atras.
        Devuelve un dataframe con esa data. '''
    
    data = hb.history.get_daily_history(ticker, 
                                        datetime.date.today() - datetime.timedelta(days=n_dias),
                                        datetime.date.today()
                                       )
    
    data.loc[:,"date"] = pd.to_datetime(data.loc[:,"date"])
    data = data.set_index("date")
    return data


def get_dataset(hb, tickers, n_dias):
    ''' Toma una lista de tickers y un objeto homebroker. Para cada ticker llama
        a la funcion ticker_get_datas y se queda con el precio de cierre.
        Concatena todas las Series en un dataframe y lo devuelve. '''
    
    df = []
    for t in tickers:
        ticker_data = ticker_get_data(hb, t, n_dias)
        ticker_data = ticker_data.close
        ticker_data.name = t
        df.append(ticker_data)
        
    return pd.concat(df,1)


def ticker_get_current_price(hb, ticker):
    ''' Devuelve el precio actual de un ticker '''
    return hb.history.get_intraday_history(ticker).tail(1).close.values[0]

df = get_dataset(hb,tickers, n_dias)

## convierto los precios en retornos (%). Se podría buscar una alternativa mejor
returns = df.pct_change().dropna() 

## tomo la mediana de cada columna y la divido por el mad. Ordeno y me quedo con el top n_assets
## (de vuelta, se puede hacer *mucho* mejor que esto)
top_choice = returns.median()/returns.mad()
top_choice = top_choice.sort_values(ascending=False)[:n_assets]
portfolio_tickers = list(top_choice.index)

## estos van a ser los tickers para mi portfolio:
portfolio_tickers

"""Cuando fui a comprar me di cuenta que hay algunas reglas a tener en cuenta. Como que si el precio es mayor a 250, tenes que redondearlo a multiplos de 50 centavos. O que si está entre 100 y 250 tenes que redondear a multiplos de 25 centavos. Esto lo meto en una funcion para redondear precios:"""

def round_price(price):
    decimals = price % 1
    price_no_decimals = price//1 
    
    if (price > 250) and (decimals != 0.5):
        price = round(price)
        
    elif (price > 100) and (price <=250) and (decimals not in [0, .25, .5, .75]):
        if decimals <.25:
            price =  price_no_decimals
        elif decimals >.25 and decimals <.5:
            price = price_no_decimals + 0.25
        elif decimals >.5 and decimals <.75:
            price = price_no_decimals + 0.5
        else:
            price = price_no_decimals + 0.75
    
    return price

"""Y para armar el portfolio de 1/N:"""

def get_1overN_portfolio(hb, tickers, capital):
    
    ''' Toma una lista de tickers y un monto de dinero. Divide el monto
        en la cantidad de tickers, obtiene el precio actual de la accion,
        la redondea segun las reglas de round_price y calcula cuantas puede
        comprar. 
        Devuelve una lista de tuplas, donde cada tupla tiene ticker, precio 
        y cantidad a comprar.'''
    
    money_per_asset = capital/len(tickers)
    portfolio = []
    for t in tickers:
        current_price = ticker_get_current_price(hb, t)
        current_price = round_price(current_price)
        n_assets = money_per_asset//current_price
        portfolio.append((t, current_price, n_assets))

    return portfolio

portfolio = get_1overN_portfolio(hb, portfolio_tickers, capital)

## este es el portfolio que nos queda: 
## una lista de tuplas. En cada tupla: ticker, precio y cantidad
portfolio

"""Iteramos sobre cada tupla del portfolio y llamamos al método "send_order_buys" para hacer las compras:"""

## y con esto lo compramos
for p in portfolio:
    ## si la cantidad es mayor a 0, compramos:
    if p[2] > 0: 
        order_number = hb.orders.send_order_buy(p[0], plazo, p[1], int(p[2]))

"""Con esto ya tenemos un primer portfolio andando!

### Y para rebalancear?

Vamos a tener que rebalancear cada tanto el portfolio. Lo bueno es que cocos no te cobra comisiones y podes rebalancear todas las veces que quieras. 
La idea seria meter este pedacito de codigo en un cron y olvidarte.

Vamos por partes: lo primero es traerme el portfolio actual:
"""

def portfolio_get_current_positions(hb, comitente):
    
    '''Esta funcion hace un request contra /Consultas/GetConsultas al proceso 22. Esto te devuelve tu comitente'''
    
    payload = {'comitente': str(comitente),
     'consolida': '0',
     'proceso': '22',
     'fechaDesde': None,
     'fechaHasta': None,
     'tipo': None,
     'especie': None,
     'comitenteMana': None}
    
    portfolio = requests.post("https://cocoscap.com/Consultas/GetConsulta", cookies=hb.auth.cookies, json=payload).json()
    portfolio = portfolio["Result"]["Activos"][1]["Subtotal"]
    
    ## esto devuelve el ticker, el precio y la cantidad que tenes
    portfolio = [( x["NERE"], float(x["PCIO"]), float(x["CANT"]) ) for x in portfolio]
    return portfolio

"""Y con el portfolio actual, más el portfolio que quiero tener (que lo voy a sacar usando la funcion que ya defini para calcular el portfolio 1/N) voy a generar las ordenes para llegar al portfolio nuevo.
Las proximas dos funciones van a hacer eso:
"""

def get_changes(old_portfolio, new_portfolio):
    
    ''' Recibe un portfolio viejo y un portfolio nuevo y calcula la diferencia entre ambos.
        Devuelve un diccionario "changes" con las modificaciones en cantidad de acciones 
        que hay que realizar'''
    
    changes = {}
    old_portfolio = dict([
                ( x[0], [x[1],x[2]] ) for x in old_portfolio
    ])
    
    for row in new_portfolio:
        ticker = row[0]
        price = row[1]
        quantity = row[2]
        
        if ticker in old_portfolio:
            changes[ticker] = [price, quantity - old_portfolio[ticker][1]]
        else:
            changes[ticker] = [price, quantity]
    return changes

def changes2orders(changes, plazo):
    
    ''' Toma un diccionario de changes y devuelve una lista de ordenes
        Esto lo usamos en conjunto con get_changes para armar las ordenes 
        que vamos a usar para rebalancear '''
    
    orders = []
    for ticker, price_quantity in changes.items():
        price, quantity = price_quantity
        if quantity < 0:
            order = ("V",ticker,plazo,price, quantity )
            orders.append(order)
    return orders

"""Solo para emprolijar un poco: juntamos las dos funciones anteriores."""

def get_orders(old_portfolio, new_portfolio, plazo):
    
    ''' Combinamos get_changes y changes2orders para tomar el portfolio que tenias
        y generar ordenes. Con estas ordenes vamos a hacer los cambios necesarios
        para convertir nuestro portfolio actual en el portfolio que queremos '''
    
    changes = get_changes(old_portfolio, new_portfolio)
    orders = changes2orders(changes, plazo)
    return orders

"""Y nos quedaria armar una funcion que ejecute esas órdenes:"""

def execute_orders(hb, orders):
    
    '''Toma las ordenes que generamos con get_orders y las manda al broker para comprar y vender
       lo que necesitamos '''
    
    for order in orders:
        if order[0] == "V":
            order_number = hb.orders.send_order_sell(order[1], order[2], order[3], int(abs(order[4])))
        elif order[0] == "C":
            order_number = hb.orders.send_order_buy(order[1], order[2], order[3], int(abs(order[4])))

## obtenemos el portfolio actual
current = portfolio_get_current_positions(hb, comitente)

## y esto es nuestro capital: ¿cuanto vale nuestro portfolio?
## esa plata la vamos a dividir para rebalacearlo
capital = sum([x[1]*x[2] for x in current])

## generamos el nuevo portfolio y las ordenes para llevar
## del portfolio que tenemos al portfolio que queremos
new_portfolio = get_1overN_portfolio(hb, tickers,capital)
orders = get_orders(current, new_portfolio, plazo)

## y con esto ejecutamos las ordenes
execute_orders(hb, orders)