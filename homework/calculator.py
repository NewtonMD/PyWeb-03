'''______________________________________________________
Mike Newton
newton33@uw.edu
Web Programming With Python 100
University of Washington, Spring 2016
Last Updated:  20 April 2016
Python Version 3.5.1
______________________________________________________'''

import operator as oper
import functools as ft


def add(*args):
    
    """ Returns a STRING with the sum of the arguments """
    #convert args to floats so we can do the maths
    values = list(args)
    for x in range(len(values)):
        values[x] = float(values[x])
       
    summation = str(ft.reduce(oper.add,values))
    return summation

def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    #convert args to floats so we can do the maths
    values = list(args)
    for x in range(len(values)):
        values[x] = float(values[x])
    product = str(ft.reduce(oper.mul,values))

    return product

def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    #convert args to floats so we can do the maths
    values = list(args)
    for x in range(len(values)):
        values[x] = float(values[x])

    try:
        quotient = str(ft.reduce(oper.truediv,values))
    except ZeroDivisionError:
        quotient = "You can't divide by zero!  Everyone knows that!"

    return quotient

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    #convert args to floats so we can do the maths
    values = list(args)
    for x in range(len(values)):
        values[x] = float(values[x])
        
    difference = str(ft.reduce(oper.sub,values))

    return difference

def home(*args):
    """ Returns a STRING with the instructions for using calculator """
    home_page = """To use this calculator, simply type the desired mathematic operation<br>
                after the http://localhost:8080/ in your browser's address bar.<br>
                Your choices are:<br>
                    add/<br>
                    subtract/<br>
                    multiply/<br>
                    divide/<br>
                Follow your mathematic operation in the address with as many operands as you want.<br>
                <br>
                Example:  http://localhost:8080/add/5/3/2/6/10 will return a value of 26 to your browser.<br>"""

    return home_page


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    args = path.strip("/").split("/")
    func_name = args.pop(0)
    if not func_name:
        func = home
    else:
        func = {
            "add": add,
            "subtract": subtract,
            "divide": divide,
            "multiply": multiply
        }.get(func_name.lower())

    return func, args

def application(environ, start_response):

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
