from flask import Flask

app = Flask(__name__) # create app

@app.route('/') # set url route

def home():
    return 'Hello, Flask!' # display this msg when open page

if __name__ == '__main__':
    app.run(debug=True) # start server