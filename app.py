from flask import Flask,render_template
from service import movie_service
from service import score_service
from service import word_service

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return index()

@app.route('/movie')
def movie():
    movies = movie_service.select_all()
    return render_template("movie.html", movies=movies)

@app.route('/score')
def score():
    score, score_count = score_service.score_statistic()
    return render_template("score.html", score=score, score_count=score_count)

@app.route('/word')
def word():
    path = word_service.get_wordcloud()
    return render_template("word.html", img_path = path)

@app.route('/team')
def team():
    return render_template("team.html")


if __name__ == '__main__':
    app.run()
