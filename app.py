from flask import Flask, render_template
app = Flask(__name__)


# 路由解析，通过用户访问的路径，匹配相应的函数
# 返回给用用户选然后的文件
@app.route("/")
def movie():
    return render_template("movie.html")


if __name__ == '__main__':
    app.run(debug=True)
