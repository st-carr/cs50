from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys

from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives)
    
    # validate screen_name
    screen_name = request.args.get("screen_name", "").lstrip("@")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, 100)
    if tweets == None:
        print("exit")
        sys.exit(3)
    
    pos_num = 0
    neg_num = 0
    nut_num = 0
    score = 0
    for tweet in tweets:
        score = analyzer.analyze(tweet)
        if score > 0.0:
            pos_num += 1
        elif score < 0.0:
            neg_num += 1
        else:
            nut_num += 1

    total = nut_num + pos_num + neg_num
    nut_per = nut_num / total
    pos_per = pos_num / total
    neg_per = neg_num / total


    # TODO
    positive, negative, neutral = pos_per, neg_per, nut_per

    # generate chart
    chart = helpers.chart(positive, negative, neutral)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
