#执行模块
import main

#暂时访问空间锁上的好友会报错
usr = input('请输入你的QQ号:')
pwd = input('请输入你的密码(盗号木马什么的,这个真没有...):')

main.begin(usr,pwd)