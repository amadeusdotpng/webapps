from flask import Flask, send_from_directory, render_template, request, redirect, make_response, jsonify, session, abort
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
from urllib.parse import quote
import google.auth.transport.requests
import requests
import json
# import os


app = Flask(__name__)

app.secret_key = "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"
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # REMOVE THIS WHEN YOU DEPLOY

GOOGLE_CLIENT_ID = "919107238969-h5u692gck2e7j5v257bidtb75ohf6qg7.apps.googleusercontent.com"

flow = Flow.from_client_secrets_file(
    client_secrets_file = "login_creds.json",
	scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="https://orlinab.pythonanywhere.com/callback" # FIX THIS WHEN YOU DEPLOY
    # redirect_uri="http://localhost/callback" # FIX THIS WHEN YOU DEPLOY
)

cred = credentials.Certificate("./credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Login Wrapper
# -------------
def required_login(from_page):  # A function to check if the user is authorized or not
    def _decorator(func):
        def wrapper(*args, **kwargs):
            if "sub" not in session:  # Auth is required
                session['from_page'] = from_page
                return redirect("/login")
            else:
                return func()
        return wrapper
    return _decorator
    
# Login Things
# ------------
@app.route("/login") # Google login screen 
def login():
    if "sub" in session:
        return redirect(session.get('from_page', '/'))
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/logout") # Logout Endpoint
def logout():
    session.clear()
    return redirect("/")


@app.route("/callback") # Callback handler after authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session.update(id_info)
    return redirect(session.get('from_page', '/'))

# Landing Page
# ------------
@app.route('/')
def index():
    return send_from_directory(directory=app.static_folder, path='index.htm')

# Bio Site
# --------
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

# Cringe Stylesheets
# ------------------
@app.route('/cringe-stylesheets')
def cringess():
    return send_from_directory(directory=app.static_folder, path='cringe-stylesheets/index.htm')

# Zen Garden
# ----------
@app.route('/zengarden')
def zengarden():
    return send_from_directory(directory=app.static_folder, path='zengarden/index.htm')

# Quiz
# ----
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

# Game
# ----
@app.route('/game')
def game():
    return send_from_directory(directory=app.static_folder, path='game/index.htm')

# Survey
# ------
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

# Todo List
# ---------
@app.route('/todo')
def todo():
    return render_template('todo/index.htm')

@app.route('/todo/list')
def todo_list():
    docref = db.collection('todo_list')
    docs = docref.stream()
    out = []
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['listid'] = doc.id
        doc_items = docref.document(doc.id).collection('items').stream()
        items = []
        for item in doc_items:
            item_dict = item.to_dict()
            item_dict['itemid'] = item.id
            items.append(item_dict)
        doc_dict['items'] = items

        out.append(doc_dict)
    return jsonify(out)
    
@app.route('/todo/addlist')
def todo_addlist():
    if 'name' in request.args:
        name = request.args['name']
        db.collection('todo_list').add({
            'name': name,
            'timestamp': firestore.SERVER_TIMESTAMP,
        })
    return redirect('/todo')

@app.route('/todo/additem/<list_id>')
def todo_additem(list_id):
    if 'name' in request.args:
        docref = db.document(f'todo_list/{list_id}')
        if docref.get().exists:
            docref.collection('items').add({
                'name': request.args['name'],
                'is_complete': False,
                'timestamp': firestore.SERVER_TIMESTAMP,
            })
    return redirect('/todo')

@app.route('/todo/delitem/<list_id>/<item_id>')
def todo_delitem(list_id, item_id):
    db.document(f'todo_list/{list_id}/items/{item_id}').delete()
    return redirect('/todo')

@app.route('/todo/dellist/<list_id>')
def todo_dellist(list_id):
    docref = db.document(f'todo_list/{list_id}')
    docs = docref.collection('items').list_documents()
    for doc in docs:
        doc.delete()
    docref.delete()
    return redirect('/todo')

@app.route('/todo/toggleitem/<list_id>/<item_id>')
def todo_toggleitem(list_id, item_id):
    docref = db.document(f'todo_list/{list_id}/items/{item_id}')
    doc = docref.get()
    if doc.exists:
        is_complete = doc.to_dict().get('is_complete', False)
        docref.update({'is_complete': not is_complete})
    return redirect('/todo')


# Todo List with Login
# --------------------
@app.route('/todo-login', endpoint='todo_login')
@required_login('/todo-login')
def todo_login():
    return render_template('todo_login/index.htm')

def check_email_exists(email, docpath):
    docref = db.document(f'{docpath}/{email}')
    if not docref.get().exists:
        db.document(f'{docpath}/{email}').set({
            'name': session['name'],
            'timestamp': firestore.SERVER_TIMESTAMP
        })
    
@app.route('/todo-login/addlist')
def todo_login_addlist():
    email = session['email']
    # todo_list_login_users
    check_email_exists(email, 'todo_list_login_users')
    if 'name' in request.args:
        name = request.args['name']
        db.collection(f'todo_list_login_users/{email}/todo_list').add({
            'name': name,
            'timestamp': firestore.SERVER_TIMESTAMP,
        })
    return redirect('/todo-login')

@app.route('/todo-login/additem/<list_id>')
def todo_login_additem(list_id):
    email = session['email']
    check_email_exists(email, 'todo_list_login_users')
    if 'name' in request.args:
        docref = db.document(f'todo_list_login_users/{email}/todo_list/{list_id}')
        if docref.get().exists:
            docref.collection('items').add({
                'name': request.args['name'],
                'is_complete': False,
                'timestamp': firestore.SERVER_TIMESTAMP,
            })
    return redirect('/todo-login')

@app.route('/todo-login/delitem/<list_id>/<item_id>')
def todo_login_delitem(list_id, item_id):
    email = session['email']
    db.document(f'todo_list_login_users/{email}/todo_list/{list_id}/items/{item_id}').delete()
    return redirect('/todo-login')

@app.route('/todo-login/dellist/<list_id>')
def todo_login_dellist(list_id):
    email = session['email']
    docref = db.document(f'todo_list_login_users/{email}/todo_list/{list_id}')
    docs = docref.collection('items').list_documents()
    for doc in docs:
        doc.delete()
    docref.delete()
    return redirect('/todo-login')

@app.route('/todo-login/toggleitem/<list_id>/<item_id>')
def todo_login_toggleitem(list_id, item_id):
    email = session['email']
    docref = db.document(f'todo_list_login_users/{email}/todo_list/{list_id}/items/{item_id}')
    doc = docref.get()
    if doc.exists:
        is_complete = doc.to_dict().get('is_complete', False)
        docref.update({'is_complete': not is_complete})
    return redirect('/todo-login')

@app.route('/todo-login/list')
def todo_login_list():
    email = session['email']
    docref = db.collection(f'todo_list_login_users/{email}/todo_list')
    docs = docref.stream()
    out = []
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['listid'] = doc.id
        doc_items = docref.document(doc.id).collection('items').stream()
        items = []
        for item in doc_items:
            item_dict = item.to_dict()
            item_dict['itemid'] = item.id
            items.append(item_dict)
        doc_dict['items'] = items

        out.append(doc_dict)
    return jsonify(out)
 
# Movie Reviews
# -------------
def to_title(title):
    exceptions = [
        'and', 'as', 'but', 'for', 'if', 'nor', 'or', 'so', 'yet', 'a', 'an', 'the',
        'as', 'at', 'by', 'for', 'in', 'of', 'off', 'on', 'per', 'to', 'up', 'via'
    ]
    return ' '.join(t[0].upper() + t[1:] if i==0 or not t.lower() in exceptions else t.lower() for i,t in enumerate(title.split('-')))

@app.route('/movie')
def movie():
    return render_template('/movie/index.htm')

@app.route('/movie/make-post', endpoint='movie_make_post')
@required_login('/movie/make-post')
def movie_make_post():
    return send_from_directory(directory=app.static_folder, path='movie/make_post.htm')

@app.route('/movie/create-post', endpoint='movie_create_post')
@required_login('/movie/create-post')
def movie_create_post():
    email = session['email']
    check_email_exists(email, 'movie_users')
    if 'movie_title' in request.args and 'movie_rating' in request.args:
        title = request.args['movie_title']
        movie_id = '-'.join(title.lower().split())
        db.collection(f'movie_users/{email}/reviews').add({
            'movie_id': movie_id,
            'movie_rating': request.args['movie_rating'],
            'review_title': request.args['review_title'],
            'review_content': request.args['review_content'],
            'author_id': email,
            'author': session['name'],
            'timestamp': firestore.SERVER_TIMESTAMP,
        })
    return redirect('/movie')

@app.route('/movie/del-post/<post_id>', endpoint='movie_del_post')
def movie_del_post(post_id):
    if not 'email' in session:
        return redirect('/movie')
    email = session['email']
    db.document(f'movie_users/{email}/reviews/{post_id}').delete()
    return redirect('/movie')

@app.route('/movie/gettitles')
def movie_gettitles():
    titles = {}
    users_ref = db.collection('movie_users').stream()
    

    for user in users_ref:
        reviews_ref = db.collection(f'movie_users/{user.id}/reviews').stream()
        for review in reviews_ref:
            review_dict = review.to_dict()
            movie_id = review_dict['movie_id']
            data = titles.get(movie_id, {
                'review_count': 0,
                'total_rating': 0,
                'movie_title': to_title(movie_id),
            })
            titles[movie_id] = {
                'review_count': data['review_count'] + 1,
                'total_rating': data['total_rating'] + int(review_dict['movie_rating']),
                'movie_title': data['movie_title'],
            }
    return titles

@app.route('/movie/getreviews/<movie_id>')
def movie_getreviews(movie_id):
    users_ref = db.collection('movie_users').stream()
    out = []
    for user in users_ref:
        reviews_ref = db.collection(f'movie_users/{user.id}/reviews') \
            .where(filter=FieldFilter("movie_id", '==', movie_id)).stream()
        for review in reviews_ref:
            review_dict = review.to_dict()
            review_dict['id'] = review.id
            out.append(review_dict)
    return jsonify(sorted(out, key=lambda r: r['timestamp'], reverse=True))

@app.route('/movie/reviews/<movie_id>')
def movie_reviews(movie_id):
    return render_template('movie/reviews.htm', movie_id=quote(movie_id, safe=''), movie_title=to_title(movie_id))

@app.route('/movie/getreviewsself')
def movie_getreviewsself():
    if not 'email' in session:
        return redirect('/movie')
    email = session['email']
    reviews_ref = db.collection(f'movie_users/{email}/reviews').stream()
    out = []
    for review in reviews_ref:
        review_dict = review.to_dict()
        review_dict['id'] = review.id
        out.append(review_dict)
    return jsonify(sorted(out, key=lambda r: r['timestamp'], reverse=True))       

@app.route("/movie/profile", endpoint='movie_profile')
@required_login('/movie/profile')
def movie_profile():
    return render_template('movie/profile.htm', given_name=session['given_name'])

@app.route("/movie/login", endpoint='movie_login')
@required_login('/movie/login')
def movie_login():
    return redirect("/movie")

@app.route("/movie/logout") # Logout Endpoint
def movie_logout():
    session.clear()
    return redirect("/movie")
   
if __name__ == "__main__":
    app.json.sort_keys = False
    app.run(host='0.0.0.0', port=80, debug=True)
