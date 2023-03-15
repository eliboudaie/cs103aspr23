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
    return f'''
        <h1>GPT Demo</h1>
        <a href="{url_for('gptdemo')}">Ask questions to GPT</a>
        <a href="{url_for('about')}">About this application</a>
        <a href="{url_for('team')}">Meet the team</a>
        <a href="{url_for('index')}">Links</a>
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
@app.route('/index')
def index():
    ''' display links to team members' pages '''
    print('processing /index route')
    return '''
        <h1>Links</h1>
        <ul>
            <li><a href="https://github.com/eliboudaie/ ">Eli</a></li>
            <li><a href="https://github.com/felixc5">Bofan</a></li>
        </ul>
    '''


@app.route('/gptdemo', methods=['GET', 'POST'])
def gptdemo():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = gptAPI.getResponse(prompt)
        return f'''
        <h1>GPT Demo</h1>
        <pre style="bgcolor:yellow">{prompt}</pre>
        <hr>
        Here is the answer in text mode:
        <div style="border:thin solid black">{answer}</div>
        Here is the answer in "pre" mode:
        <pre style="border:thin solid black">{answer}</pre>
        <a href={url_for('gptdemo')}> make another query</a>
        '''
    else:
        return '''
        <h1>GPT Demo App</h1>
        Enter your query below
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        '''

if __name__=='__main__':
    # run the code on port 5001, MacOS uses port 5000 for its own service :(
    app.run(debug=True,port=5001)
