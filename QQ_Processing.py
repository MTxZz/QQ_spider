#对数据进行处理
import jieba.analyse
import jieba
import matplotlib.pyplot as plt 
from wordcloud import WordCloud#词云可视化

#词云
def get_wordcloud(file):
	path = file
	f = open(path,'r',encoding='UTF-8').read()

	# 结巴分词，生成字符串，wordcloud无法直接生成正确的中文词云
	jieba.analyse.set_stop_words('stopword.txt')
	cut_text = " ".join(jieba.cut(f))
	wordcloud = WordCloud(
	   #设置字体，不然会出现口字乱码，文字的路径是电脑的字体一般路径，可以换成别的
	   font_path="YaHei.ttf",
	   #设置了背景，宽高
	   background_color="white",width=2000,height=1500).generate(cut_text)

	plt.imshow(wordcloud, interpolation="bilinear")
	plt.axis("off")
	plt.show()

#get_wordcloud('note.txt')