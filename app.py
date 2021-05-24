from flask import Flask, render_template
import sqlite3
app = Flask(__name__)


# 路由解析，通过用户访问的路径，匹配相应的函数
# 返回给用用户选然后的文件
@app.route("/")
def movie():
    datalist = []
    score = []  # 评分
    num = []  # 每个评分所统计出的电影数量
    con = sqlite3.connect("doubantop250.db")
    cur = con.cursor()
    sql = "select * from doubantop250"
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

    return render_template("movie.html", movies=datalist, score=score, num=num)


if __name__ == '__main__':
    app.run(debug=True)
