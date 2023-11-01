from flask import Flask, send_from_directory, render_template, request, redirect, make_response
import firebase_admin
from firebase_admin import credentials, firestore
import json

app = Flask(__name__)

cred = credentials.Certificate("./credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    return send_from_directory(directory=app.static_folder, path='index.htm')

@app.route('/bio-site')
def bio_site():
    return send_from_directory(directory=app.static_folder, path='bio-site/index.htm')

@app.route('/bio-site/bio')
def bio_site_bio():
    return send_from_directory(directory=app.static_folder, path='bio-site/bio.htm')

@app.route('/bio-site/schedule')
def bio_site_schedule():
    return send_from_directory(directory=app.static_folder, path='bio-site/schedule.htm')
    
@app.route('/bio-site/favorites')
def bio_site_favorites():
    return send_from_directory(directory=app.static_folder, path='bio-site/favorites.htm')

@app.route('/cringe-stylesheets')
def cringess():
    return send_from_directory(directory=app.static_folder, path='cringe-stylesheets/index.htm')

@app.route('/zengarden')
def zengarden():
    return send_from_directory(directory=app.static_folder, path='zengarden/index.htm')

@app.route('/quiz')
def quiz():
    return send_from_directory(directory=app.static_folder, path='quiz/index.htm')

@app.route('/quiz/questions')
def quiz_questions():
    # 0: HOUSE
    # 1: FOREMAN
    # 2: CAMERON
    # 3: CHASE

    questions = {
        1:"Which author do you like the most?",
        2:"Pick the quote that you like the most.",
        3:"Which Greek Mythology figure do you like the most?",
        4:"Which song do you like the most?",
        5:"Which programming language do you like the most?",
    }

    answers = {
        1:{0:["Franz Kafka", "kafka.jpg"],
           1:["Shakespeare", "shakespeare.png"],
           2:["Jane Austen", "jane_austen.png"],
           3:["I don't read books", "nobooks.jpg"]},
        2:{0:["\"The meaning of life is that it stops.\""],
           1:["\"Eighty percent of success is showing up.\""],
           3:["\"If you want something done right, do it yourself.\""],
           2:["\"To err is human; to forgive, divine.\""]},
        3:{2:["Rhea", "rhea.png"],
           1:["Prometheus", "prometheus.jpg"],
           3:["Artemis", "artemis.jpg"],
           0:["Sisyphus", "sisyphus.png"]},
        4:{0:["Georgia on My Mind - Ray Charles"],
           2:["Perfect - Ed Sheeran"],
           1:["Cheek to Cheek - Ella Fitzgerald"],
           3:["Everlong - Foofighters"]},
        5:{0:["C++", "cpp.png"],
           2:["Julia", "julia.png"],
           3:["Rust", "rust.jpg"],
           1:["Python", "python.png"]}
    }

    results = {
        0:["Gregory House",
           "You're super duper smart but you're also freaking mean. stop that.",
           "house.png"],
        1:["Eric Foreman",
           "You're rational and a hard worker. You've put in the elbow grease to get where you are.",
           "foreman.jpg"],
        2:["Allison Cameron",
           "You're sympathetic and care a lot about other people. You're a social butterfly",
           "cameron.png"],
        3:["Robert Chase",
           "You're great at what you do. A little arrogant but that's okay.",
           "chase.png"],
    }

    if "quiz_num" in request.args:
        quiz_num = int(request.args["quiz_num"])

        if quiz_num == len(questions):
            res = [0,0,0,0]
            for i in range(len(questions)):
                answer_num = int(request.args[f"q{i+1}"])
                res[answer_num] += 1
            quiz_res = results[res.index(max(res))]
            name = request.args["name"]
            return render_template("quiz/result.htm",
                                    name=name,
                                    result=quiz_res[0],
                                    result_par=quiz_res[1],
                                    result_img=quiz_res[2])

        return render_template("quiz/questions.htm",
                               question=questions[quiz_num+1],
                               answers=answers[quiz_num+1],
                               quiz_num=quiz_num,
                               args=request.args)

    return render_template("quiz/name.htm")

@app.route('/game')
def game():
    return send_from_directory(directory=app.static_folder, path='game/index.htm')

@app.route('/survey')
def survey():
    survey = {
        'lang':{"java":0, "python":0, "c":0, "cpp":0, "csharp":0, "rust":0, "haskell":0, "javascript":0, "bash":0, },
        'os':{"windows":0, "macos":0, "linux":0},
        'editor':{"vim":0, "emacs":0, "neovim":0, "nano":0, "geany":0, "vscode":0, },
        'gaang':{"aang":0, "katara":0, "sokka":0, "toph":0, "zuko":0, "suki":0, "appa":0, "momo":0, }
    }
    for doc in db.collection('survey').stream():
        vote = doc.to_dict()
        survey['lang'][vote['lang']]     += 1
        survey['os'][vote['os']]         += 1
        survey['editor'][vote['editor']] += 1
        survey['gaang'][vote['gaang']]   += 1

    return render_template('survey/index.htm', data=json.dumps(survey))

@app.route('/survey/vote')
def survey_vote():
    cookie = request.cookies.get('cookie')
    if cookie is not None:
        doc = db.collection('survey').document(cookie).get()
        if doc.exists:
            return redirect('/survey/failure')

    return send_from_directory(directory=app.static_folder, path='survey/vote.htm')

@app.route('/survey/verify', methods=['POST'])
def survey_verify():
    if request.referrer is None:
        return redirect('/survey')

    cookie = request.cookies.get('cookie')
    doc = db.collection('survey').document(cookie).get()
    if doc.exists:
        return redirect('/survey/failure')

    return redirect('/survey/process', code=307) # Code 307 preserves POST request

@app.route('/survey/process', methods=['GET', 'POST'])
def survey_process():
    if request.referrer is None:
        return redirect('/survey')

    opt = {
        "lang":["java", "python", "c", "cpp", "csharp", "rust", "haskell", "javascript", "bash"],
        "os":["windows", "macos", "linux"],
        "editor":["vim", "emacs", "neovim", "nano", "geany", "vscode"],
        "gaang":["aang", "katara", "sokka", "toph", "zuko", "suki", "appa", "momo"],
    }
    
    vote = {}
    for key in opt:
        input = request.form[key]
        if input not in opt[key]:
            return redirect('/survey/error')
        vote[key] = input
    vote['timestamp'] = firestore.SERVER_TIMESTAMP
    vote_ref = db.collection('survey').add(vote)
    resp = make_response(redirect('/survey/success'))
    resp.set_cookie('cookie', vote_ref[-1].id)
    return resp

@app.route('/survey/success')
def survey_success():
    if request.referrer is None:
        return redirect('/survey')
    return send_from_directory(directory=app.static_folder, path='survey/success.htm')

@app.route('/survey/failure')
def survey_failure():
    if request.referrer is None:
        return redirect('/survey')
    return send_from_directory(directory=app.static_folder, path='survey/failure.htm')

@app.route('/survey/error')
def survey_error():
    if request.referrer is None:
        return redirect('/survey')
    return send_from_directory(directory=app.static_folder, path='survey/error.htm')
    

if __name__ == "__main__":
    app.json.sort_keys = False
    app.run(host='0.0.0.0', port=80, debug=True)
