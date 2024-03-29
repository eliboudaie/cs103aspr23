'''
gptwebapp shows how to create a web app which ask the user for a prompt
and then sends it to openai's GPT API to get a response. You can use this
as your own GPT interface and not have to go through openai's web pages.

We assume that the APIKEY has been put into the shell environment.
Run this server as follows:

On Mac
% pip3 install openai
% pip3 install flask
% export APIKEY="......."  # in bash
% python3 gptwebapp.py

On Windows:
% pip install openai
% pip install flask
% $env:APIKEY="....." # in powershell
% python gptwebapp.py
'''
from flask import request,redirect,url_for,Flask
from gpt import GPT
import os

app = Flask(__name__)
gptAPI = GPT(os.environ.get('APIKEY'))

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q789789uioujkkljkl...8z\n\xec]/'

@app.route('/')
def index():
    ''' display a link to the general query page '''
    print('processing / route')
    return '''
        <html>
            <head>
                <title>Tweet Generator</title>
                <style>
                    body {
                        background-color: #f5f5f5;
                        font-family: Arial, sans-serif;
                    }
                    h1 {
                        font-size: 36px;
                        color: #333333;
                        margin-top: 50px;
                    }
                    .button {
                        background-color: #4CAF50;
                        border: none;
                        color: white;
                        padding: 16px 32px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 24px;
                        margin: 20px;
                        cursor: pointer;
                        border-radius: 8px;
                    }
                    .button:hover {
                        background-color: #3e8e41;
                    }
                </style>
            </head>
            <body>
                <div style="text-align: center;">
                    <h1>Tweet Generator</h1>
                    <a href="/funnytweet" class="button">Generate your funny tweets</a>
                    <a href="/serioustweet" class="button">Generate your serious tweets</a>
                    <a href="/about" class="button">About this application</a>
                    <a href="/team" class="button">Meet the team</a>
                    <a href="/links" class="button">Links</a>
                </div>
            </body>
        </html>
    '''

@app.route('/about')
def about():
    ''' display information about the application '''
    print('processing /about route')
    return '''
        <h1>About</h1>
        <p>This application takes an article and turns it into either a funny or professional tweet</p>
    '''
@app.route('/team')
def team():
    ''' display information about the development team '''
    print('processing /team route')
    return '''
        <h1>Meet the Team</h1>
        <h2>Eli</h2>
        <p>Eli is a senior computer science and business major who worked on the serious tweet feature.</p>
        <h2>Bofan</h2>
        <p>Bofan is a sophomore who worked on the funny tweet feature.</p>
    '''
@app.route('/links')
def links():
    ''' display links to team members' pages '''
    print('processing /links route')
    return '''
        <h1>Useful Links</h1>
        <ul>
            <li><a href="https://github.com/eliboudaie/">Eli's GitHub page</a></li>
            <li><a href="https://github.com/felixc5">Bofan's GitHub page</a></li>
        </ul>
    '''



@app.route('/funnytweet', methods=['GET', 'POST'])
def funnytweet():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = gptAPI.getResponse(prompt)
        return f'''
        <h1>Funny Tweet Generator</h1>
        <pre style="bgcolor:yellow">{prompt}</pre>
        <hr>
        Here is the answer in text mode:
        <div style="border:thin solid black">{answer}</div>
        Here is the answer in "pre" mode:
        <pre style="border:thin solid black">{answer}</pre>
        <a href={url_for('funnytweet')}> make another query</a>
        '''
    else:
        return '''
        <h1>Funny Tweet Generator</h1>
        Enter your query below
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        '''
@app.route('/serioustweet', methods=['GET', 'POST'])
def serioustweet():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = gptAPI.getResponse2(prompt)
        return f'''
        <h1>Serious Tweet Generator</h1>
        <pre style="bgcolor:yellow">{prompt}</pre>
        <hr>
        Here is the answer in text mode:
        <div style="border:thin solid black">{answer}</div>
        Here is the answer in "pre" mode:
        <pre style="border:thin solid black">{answer}</pre>
        <a href={url_for('funnytweet')}> make another query</a>
        '''
    else:
        return '''
        <h1>Serious Tweet Generator</h1>
        Enter your query below
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        '''

if __name__=='__main__':
    # run the code on port 5001, MacOS uses port 5000 for its own service :(
    app.run(debug=True,port=5001)
