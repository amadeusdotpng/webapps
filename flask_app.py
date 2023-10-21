from flask import Flask, send_from_directory, render_template, request, redirect
import firebase_admin
from firebase_admin import credentials, firestore

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
    return send_from_directory(directory=app.static_folder, path='survey/index.htm')

@app.route('/survey/vote')
def survey_vote():
    if request.referrer is None:
        return redirect('/survey/verify')

    return send_from_directory(directory=app.static_folder, path='survey/vote.htm')

@app.route('/survey/verify')
def survey_verify():
    if request.referrer is None:
        return redirect('/survey')
    # Check if user's already voted

    return redirect('/survey/vote')

@app.route('/survey/process', methods=['POST'])
def survey_process():
    if request.referrer is None:
        return redirect('/survey')

    vote = {
        'lang': request.form.get('lang'),
        'os': request.form.get('os'),
        'editor': request.form.get('editor'),
        'gaang': request.form.get('gaang'),
        'timestamp': firestore.SERVER_TIMESTAMP,
    }

    db.collection('survey').add(vote)
    return redirect('/survey/success')

@app.route('/survey/success')
def survey_success():
    if request.referrer is None:
        return redirect('/survey')

    return send_from_directory(directory=app.static_folder, path='survey/success.htm')
    
    

if __name__ == "__main__":
#   app.secret_key = 'a_key_that_is_super_duper_secretive_and_no_one_knows_it'
    app.run(host='0.0.0.0', port=80, debug=True)
