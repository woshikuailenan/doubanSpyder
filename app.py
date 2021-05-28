from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


# 路由解析，通过用户访问的路径，匹配相应的函数
# 返回给用用户选然后的文件
@app.route("/movie")
def movie():
    movies = []
    con = sqlite3.connect("doubantop250.db")
    cur = con.cursor()
    sql = "select * from doubantop250 order by score desc"
    data = cur.execute(sql)
    for item in data:
        movies.append(item)

    cur.close()
    con.close()
    return render_template("movie.html", movies=movies)


# 评分统计
@app.route("/score")
def score():
    datalist = []
    score = []  # 评分
    num = []  # 每个评分所统计出的电影数量
    con = sqlite3.connect("doubantop250.db")
    cur = con.cursor()
    sql = "select * from doubantop250 order by score desc"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    print(datalist)
    print("cname", datalist[0][0])
    sql = "select score,count(score) from doubantop250 group by score "
    data = cur.execute(sql)
    for item in data:
        score.append(str(item[0]))
        num.append(item[1])

    cur.close()
    con.close()
    return render_template("score.html", movies=datalist, score=score, num=num)


# 关键词
@app.route("/keyword")
def keyword():
    return render_template("keyword.html")


# 小组成员
@app.route("/team")
def team():
    return render_template('team.html')


# 情感分析
@app.route("/sentimentAnalyze")
def sentimentAnalyze():
    return render_template('sentimentAnalyze.html')


# 模板
@app.route("/temp")
def temp():
    return render_template('temp.html')


if __name__ == '__main__':
    app.run(debug=True)
