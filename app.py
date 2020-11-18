from flask import Flask,render_template,request
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
    cur_page = int(request.args.get('page')) or 1
    movies = movie_service.select_page(cur_page)
    pages = movie_service.get_pages(cur_page)
    return render_template("movie.html", movies=movies, cur_page=cur_page, pages=pages)

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
