import jieba  # 分词
from matplotlib import pyplot  # 绘图
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算
import sqlite3  # 数据库

con = sqlite3.connect('doubantop250.db')
cur = con.cursor()
sql = "select introduction from doubantop250"
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
cur.close()
con.close()

cut = jieba.cut(text)
string = ' '.join(cut)

img = Image.open(r'.\static\assets\img\aosika.png')
img_arr = np.array(img)
wc = WordCloud(
    background_color='white',
    mask=img_arr,
    font_path='STLITI.TTF'
)
wc.generate_from_text(string)

fig = pyplot.figure(1)
pyplot.imshow(wc)
pyplot.axis('off')

pyplot.savefig(r'.\static\assets\img\word.png', dpi=500)
