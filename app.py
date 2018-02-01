import os, requests, json
import pandas as pd

from flask import Flask, render_template
from pandas.io.json import json_normalize
from tabulate import tabulate

CHALLENGE_API_URL = os.getenv('CHALLENGE_API_URL')

app = Flask(__name__)

class GridiumChallengeEntry():
    def __init__(self):
        self.url = CHALLENGE_API_URL
        self.df = None
        self.cols = [
            "id","initial","closing","peak","used","cost"]
        self.titles = [
            "ID", "Initial", "Closing", "Peak", "Used", "Cost"]
        self.update()

    def update(self):
        url = self.url
        cols = self.cols
        res = requests.get(url)
        data = json.loads(res.text)
        data = [{"id": x["id"],
                 "initial": x["attributes"]["initial"],
                 "closing": x["attributes"]["closing"],
                 "cost": x["attributes"]["cost"],
                 "peak": x["attributes"]["peak"],
                 "used": x["attributes"]["used"],}
                for x in data["data"]]
        df = pd.DataFrame(data)
        df.set_index("id")
        df = df[cols]
        df.columns = self.titles
        self.df = df
        print(df)


@app.route('/')
def index():
    tables = [gce.df.to_html(border=0, classes=[
        "table-bordered", "table-striped",
        "table-hover", "meter-table"])]
    return render_template('index.html', tables=tables)


gce = GridiumChallengeEntry()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
