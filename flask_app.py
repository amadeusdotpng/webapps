from flask import Flask, send_from_directory

app = Flask(__name__)


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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
