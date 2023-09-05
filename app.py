from flask import Flask, render_template,request,redirect, url_for,flash,jsonify
from gtts import gTTS
import os
import speech_recognition as sr
import pyttsx3
import webbrowser
import openai
import datetime
import random
import numpy as np
from selenium import webdriver
import wikipedia

app=Flask(__name__)
openai.api_key = "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"
db = SQLAlchemy(app)

# class User(UserMixin,db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)



# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/login',methods=['GET','POST'])
# def login():
#     if request.method=='POST':
#         email=request.form.get('email')
#         password=request.form.get('password')
#         user=User.query.filter_by(email=email).first()
#         if user and password==user.password:
#             login_user(user)
#             return redirect('/')
#         else:
#             flash('invalid credentials ','danger')
#             return redirect('/login')
#     return render_template('login.html')

# @app.route('/register',methods=['GET','POST'])
# def register():
#     if request.method=='POST':
#         lst = []
#         ema=[]
#         username = request.form.get('username') 
#         email = request.form.get('email')
#         password = request.form.get('password')
#         usernames = User.query.all()
#         for un in usernames:
#             lst.append(un.username)
#         for em in usernames:
#             ema.append(em.email)
#         # if (username=='' or email=='' or password==''):
#         #     flash("Error: All fields are required","danger")   
#         #     return redirect('/register')
#         if username in lst and email in ema:
#             flash("Error: username  and email aleady exists! try with a different username and email  !",'danger')

#         elif username in lst:
#             flash("Error: username aleady exists! try with a different user name !",'danger')
            
#             return redirect('/register') 
#         elif email in ema:
#             flash("Error: email aleady exists!",'danger')
#             return redirect('/register')   
#         else:    
#             form = User(username=username,email=email,password=password)
#             db.session.add(form)
#             db.session.commit()
#             flash("User has been registered successfully",'success')
#             return redirect('/login')    
#     return render_template('register.html')

# @app.route('/logout')
# def logout():
#     logout_user()
#     flash("User has been Logout successfully",'success')
#     return redirect('/')

chatStr = ""
# https://youtu.be/Z3ZAJoi4x6Q
def chat(query):
    global chatStr
    global retStr
    retStr="Issue with OpenAI"
    try:
        #print(chatStr)
        #openai.api_key = "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"
        chatStr += f"Uday: {query}\n Apna AI: "
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(jsonify(response))
        print("TEST",response["choices"][0]["text"])
        #todo: Wrap this inside of a  try catch block
        #say(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        #retStr = response["choices"][0]["text"]
        #webdriver.Chrome().get("about:blank")
        #webdriver.Chrome().execute_script(f"window.localStorage.setItem('chat','{retStr}');")
        #webdriver.Chrome().quit()
        # with open("file.txt","a") as f:
        #     f.seek(0)
        #     f.write(retStr)
        #     f.close()
        # return retStr

        return response['choices'][0]['text']
    except:
        #webdriver.Chrome().get("about:blank")
        #retStr=webdriver.Chrome().execute_script(f"window.localStorage.setItem('chat');")
        #webdriver.Chrome().quit()
        # with open("file.txt","r") as f:
        #     f.seek(0)
        #     f.seek(-2,1)
        #     retStr=f.read(1)
        #     f.close()
        #os.remove('file.txt')
        return retStr


def ai(prompt):
    #openai.api_key = "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"
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # todo: Wrap this inside of a  try catch block
        # print(response["choices"][0]["text"])
        text += response["choices"][0]["text"]
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        r=prompt.split('intelligence')[1:] if "intelligence".lower() in prompt.lower() else prompt
        # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
        with open(f"Openai/{''.join(r).strip() }.txt", "w") as f:
            f.write(text)
        return "AI done it's job."
    except:
        return "Issue with OpenAI"

def appMain(test):
    while True:
        #print("Listening...")
        query=test
        # todo: Add more sites
        sites = [["facebook", "https://www.facebook.com"],["instagram", "https://www.instagram.com"],["flikart", "https://www.flikart.com"],["amazon", "https://www.amazon.com"],["linkedin", "https://www.linkedin.com"],["telegram", "https://web.telegram.org"],["whatsapp", "https://web.whatsapp.com"],["chatgpt", "https://chat.openai.com"],["fiem", "https://futureeducation.in/fiem/"],["future education", "https://futureeducation.in"],["xplorica", "https://xplorica.in"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                #say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                return "Opening "+site[0]+" sir..."

        # todo: Add a feature to play a specific song
        if "open music".lower() in query.lower():
            musicPath = "C:\\Users\\usutt\\Downloads\\multiverse1.png"
            #say("opening sir")
            os.system(f"start {musicPath}")
            return "opening sir"
        
        elif "open wikipedia."==query.lower():
            webbrowser.open("https://wikipedia.com")
            return "Opening wikipedia sir..."
        
        elif "open youtube."==query.lower():
            webbrowser.open("https://youtube.com")
            return "Opening youtube sir..."
        
        elif "open spotify."==query.lower():
            webbrowser.open("https://spotify.com")
            return "Opening spotify sir..."
        
        elif "open google."==query.lower():
            webbrowser.open("https://www.google.com")
            return "Opening google sir..."
        

        elif "wikipedia".lower() in query.lower():
            try:
                if ("about".lower() in query.lower()):
                    res=query.lower().split("about")
                    text=res[1]
                    result=wikipedia.summary(text, sentences=3)

                elif "search".lower() in query.lower():
                    res=query.lower().split("search")
                    text=res[1]
                    result=wikipedia.summary(text, sentences=3)

                elif "write".lower() in query.lower():
                    res=query.lower().split("write")
                    text=res[1]
                    result=wikipedia.summary(text, sentences=3)

                else :
                    text=query.lower()
                    result=wikipedia.summary(text, sentences=3)
            except:
                result="Issue with Wikipedia Library" 
            finally:   
                return result
        
        elif "the time".lower() in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            #say(f"Sir time is {hour} bajj  kee {min} minutes sir")
            return "Sir time is "+hour+" hours  and "+min+" minutes sir."

        elif ("open youtube and search".lower() in query.lower())or("using youtube".lower() in query.lower())or("search video".lower() in query.lower())or("open youtube search".lower() in query.lower()):
            # rrr= query=query  if query.split('search')  else query.split['youtube']
            # reccc=rrr[1].split(" ")
            # cccc="+".join(reccc)
            # seeee="https://www.youtube.com/results?search_query="+cccc
            # webbrowser.open(seeee)
            # return "Opening sir"
            song=query.lower().split("youtube") if("search".lower() in query.lower()) else query.lower().split("youtube")
            seee="https://www.youtube.com/results?search_query="+song[1]
            webbrowser.open(seee)
            return "Opening sir"
        
        elif ("open spotify and search".lower() in query.lower())or("using spotify".lower() in query.lower())or("search song".lower() in query.lower())or("open spotify and play song".lower() in query.lower()):
            # rr= query=query  if query.split('song')  else query.split['spotify']
            # recc=rr[1].split(" ")
            # ccc=" ".join(recc)
            song=query.lower().split("song") if("song".lower() in query.lower()) else query.lower().split("spotify")
            seee="https://open.spotify.com/search/"+song[1]+"/"
            webbrowser.open(seee)
            return "Opening sir"
        
        elif ("open google and search".lower() in query.lower())or("using google".lower() in query.lower())or("search from google".lower() in query.lower())or("open google search".lower() in query.lower()):
            # rr= query=query  if query.split('song')  else query.split['spotify']
            # recc=rr[1].split(" ")
            # ccc=" ".join(recc)
            song=query.lower().split("search") if("search".lower() in query.lower()) else query.lower().split("google")
            seee="https://www.google.com/search?q="+song[1]
            webbrowser.open(seee)
            return "Opening sir"


        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")
            return "Working on it"

        elif ("Using artificial intelligence".lower() in query.lower())or("write a program".lower() in query.lower())or("write a code".lower() in query.lower()):
            aires=ai(prompt=query)
            return aires

       # elif "alexa Quit".lower() in query.lower():
       #     exit()

        elif ("reset chat".lower() in query.lower())or("clear chat".lower() in query.lower()):
            chatStr = ""
            return "Chat cleared"

        else:
            #print("Chatting...")
            data45=chat(query)
            return data45



@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/generateimages/<prompt>')
def generate(prompt):
  print("prompt:", prompt)
  response = openai.Image.create(prompt=prompt, n=2, size="256x256") 
  print(response)
  return jsonify(response)


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/process-voice', methods=['POST'])
def process_voice():
    data = request.json
    voice_input = data.get('voiceInput')
    chatResp=appMain(voice_input)
    # Generate speech from text
    # print("Test Main",chatResp)
    # tts = gTTS(chatResp)
    # audio_path = 'static/output.mp3'
    # tts.save(audio_path)
    # return jsonify({"audioPath": audio_path})
    return jsonify({"chatResp": chatResp})



if __name__=="__main__":
    app.run(debug=True)
