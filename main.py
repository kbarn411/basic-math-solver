from pywebio import start_server
from pywebio.platform.tornado_http import start_server as start_http_server
from pywebio import start_server as start_ws_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *

from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from sympy import *
from sympy.solvers import solve

def appHeading(app):
    put_button("Return to first screen", onclick=selection)
    put_markdown(f"## {app}")
    put_markdown("### Please enter values to calculate")

def integration():
    """Integration Calculator"""
    appHeading("INTEGRATION")

    put_input('function', label='Provide function to integrate', value='x')
    put_input('min', label='Provide lower limit for integration', type='float', value=0)
    put_input('max', label='Provide upper limit for integration', type='float', value=1)
    
    while True:
        changed = pin_wait_change('function', 'min', 'max')
        with use_scope('integ', clear=True):
            try:
                x = Symbol('x')
                result = integrate(pin.function, (x, pin.min, pin.max))
                put_text(f"Result is: {round(result, 4)}")
            except (SyntaxError, TypeError, SympifyError) as e:
                put_text("Incorrect data")
            finally:
                pass

def equation():
    """Equation Solver"""
    appHeading("EQUATION")

    put_input('function', label='Provide equation to solve', value='x-1')
    put_input('xzero', label='Provide starting estimate for the roots', type='float', value=1)
    
    while True:
        changed = pin_wait_change('function', 'xzero')
        with use_scope('equat', clear=True):
            try:
                x = Symbol('x')
                result = solve(pin.function, x)
                result = np.asarray(result)
                idx = (np.abs(result - pin.xzero)).argmin()
                put_text(f"Result is: {round(result[idx], 4)}")
            except (SyntaxError, TypeError, SympifyError, ValueError) as e:
                put_text("Incorrect data")
            finally:
                pass

def regression():
    """Linear Regression Calculator"""
    appHeading("REGRESSION")

    def doRegression():
        with use_scope('regre', clear=True):
            try:
                f = file_upload(label='Provide dataset', max_size='5M', accept='.xlsx')
                df = pd.read_excel(f['content'])
                x = df.iloc[:, :-1]
                y = df.iloc[:, -1]
                reg = LinearRegression()
                reg.fit(x,y)
                put_text(f"The coefficients of fitted equation are:")
                for c in reg.coef_:
                    put_text(f"{round(c, 4)}")
                put_text(f"The intercept: {round(reg.intercept_, 4)}")
                put_text(f"The R2 value: {round(reg.score(x,y), 3)}")
            except:
                put_text("Incorrect data")
                put_button("Try again", onclick=doRegression)
    doRegression()

def selection():
    with use_scope('sel', clear=True):
        put_markdown("# Basic Statistics and Maths App")
        appMode = select('Which program do you want to start?', ['integration', 'equation', 'regression'])
        if appMode ==  'integration':
            integration()
        elif appMode ==  'equation':
            equation()
        else:
            regression()

def main():
    """Basic Statistics and Maths App"""
    selection()
    
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--http", action="store_true", default=False, help='Whether to enable http protocol for communicates')
    args = parser.parse_args()

    #start_server(main, port=8080, debug=True)

    if args.http:
        start_http_server(main, port=args.port)
    else:
        start_ws_server(main, port=args.port, websocket_ping_interval=30)