from flask import Flask, redirect,render_template, request
import json, requests, os
app = Flask(__name__)

# @app.route('/')
# def Git_Pages():
#     return redirect("https://ilumii.github.io", code=302)

with open('data.json') as f:
        data = json.load(f)

# print(json.dumps(data, indent=2))

for name in data:
    # print(name["name"], name["completed"])
    item = name["name"], name["completed"]

@app.route('/todo')
def main():
    return render_template('main.html', file=data)

@app.route('/')
def login():
    r=requests.get('https://hunter-todo-api.herokuapp.com/user?username=abc123')
    print(r.text)
    return render_template('login.html',text=' ')
    

@app.route('/userdata', methods=['POST','GET'])
def userdata():
    if request.method == 'POST':
        print('POST request recieved')
        user = request.form['username']
        print("username:" + user)
        cookies = dict(cookies_are='sillyauth')
        s=requests.Session()
        s.post('https://hunter-todo-api.herokuapp.com/auth', json={"username":request.form['username']})
        tasks=s.get('https://hunter-todo-api.herokuapp.com/todo-item')
        data = json.loads(tasks.text)
        # y=requests.post('https://hunter-todo-api.herokuapp.com/todo-item',cookies=x.cookies, json={"content":"do a thing"})
        # requests.delete('https://hunter-todo-api.herokuapp.com/todo-item/546', cookies=x.cookies)
        # print(x)
        # if x.status_code==200:
        #     print('yes')
        # else:
        #     print('no')
        # print(tasks.content)
        # print(y)
        return render_template('info.html', username=user, data=data)
    
@app.route('/delete/<id>/<username>', methods=['POST','GET'])
def dele(id,username):
#     cookies= {'auth':'sillyauth'}
#     num=id
#     x=requests.post('https://hunter-todo-api.herokuapp.com/auth', cookies=cookies, json={"username":username})
#     y=requests.delete('https://hunter-todo-api.herokuapp.com/todo-item/{{num}}', cookies=x.cookies)
    return render_template('/login.html')

@app.route('/register')
def register():
    return render_template('register.html', text= ' ')

@app.route('/new_user', methods=['POST'])
def new_user():
    response = requests.post('https://hunter-todo-api.herokuapp.com/user', json={"username":request.form['username']})
    if response.status_code == 200:
        print('registration success')
        return render_template('login.html', text='registration success')
    else:
        print('fail')
        return render_template('register.html', text='username taken')

if __name__ == "__main__":
        port = int(os.enviorn.get("PORT",5000))
        app.run(host="0.0.0.0", port=port, threaded=True)