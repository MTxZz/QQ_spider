
from selenium import webdriver
import time
import re
from QQ_cookie import Cookie
from QQ_friend import fri_list
from QQ_Data import get_Data
from QQ_Processing import get_wordcloud,jieba

#用户命令存进列表,也可以输入一个命令,执行一条
def usr_cmd():
    print('下面请输入的命令,1代表是,输入其他字符代表否')
    cmdList = []
    fri_cmd = input('是否输出你的好友列表(1/Other):')
    cmdList.append(fri_cmd)
    print('OK!')
    fri = input('请输入你想要挖掘的好友QQ号(会输出ta的信息哦):')
    cmdList.append(fri)
    print('OK!')
    pic_cmd = input('是否下载此好友的所有相册(1/Other)(由于下载照片很费时间,暂时只是输出图片链接哦):')
    cmdList.append(pic_cmd)
    print('OK!')
    note_cmd = input('是否保存此好友的留言板,进行分词处理并以词云展示(1/Other)(可能会刷屏哦):')
    cmdList.append(note_cmd)
    print('OK!')

    print('请稍等,马上开始...')

    return cmdList

#自动化登录QQ空间,前几次登录有时需要人工输入验证码,如果来不及输完,可以将time.sleep改为20
def begin(usr,pwd):
    try:
        driver = webdriver.Chrome()#实例化出一个Firefox浏览器
        driver.set_window_position(20, 40)#设置浏览器窗口的位置和大小
        driver.set_window_size(1100,700)
        driver.get('https://user.qzone.qq.com/')#打开一个页面（QQ空间登录页）
        '''
        click()方法对于一些标签不是<button>、<a>的按钮无效，
        而QQ空间触屏版中的按钮大多数都不是<button>标签，
        例如”继续打开触屏版”为<b>标签，“登录”为<div>标签。
        所以在调用FireFox等浏览器中直接click()的方式不行，
        可以看到,登录表单在页面的框架中，所以要切换到该框架
        '''
        driver.switch_to_frame('login_frame')
        #通过使用选择器选择到表单元素进行模拟输入和点击按钮提交 
        driver.find_element_by_id('switcher_plogin').click()#模拟登陆过程
        qq = driver.find_element_by_id('u')
        qq.clear()
        qq.send_keys(usr)
        password = driver.find_element_by_id('p')
        password.clear()
        password.send_keys(pwd)
        driver.find_element_by_id('login_button').click()
        time.sleep(5)

        icookie = driver.get_cookies()    #得到原始cookie
        html = driver.page_source        #得到页面html
        driver.quit()   #退出浏览器

    except:
        print('呵~  自己qq密码都记不住吗?  还有,请不要尝试登录别人的qq哦~')

    #从html中找到qzonetoken(很重要),为了得到qq的好友列表
    xpat = r'window\.g_qzonetoken = \(function\(\)\{ try{return \"(.*)";'
    qzonetoken = re.compile(xpat).findall(html)[0]
    run(usr,icookie,qzonetoken)



def run(usr,icookie,qzonetoken):
    cmdList = usr_cmd()
    #获得真实cookie
    #1
    realCookie = {}
    for c in icookie:
        realCookie[c['name']] = c['value']
    #2
    cookie = Cookie(realCookie)
    #从原始cooki中获得g_tk:
    g_tk = cookie.get_g_tk()
    #3
    #从原始cookie里获得session
    session = cookie.get_session()
    #获取好友列表下载图片
    fri = fri_list(usr,session,g_tk,qzonetoken)
    friend = fri.get_friend_list()
    if cmdList[0] == '1':
        for f in friend:
            print('QQ号:'+ f +'   昵称:' + str(friend[f]))
    else:
        pass
    #得到数据,这里代码写的好丑
    informations_Dict = {}
    fri_id = cmdList[1]
    pic = get_Data(g_tk,session,qzonetoken,fri_id,usr)
    if fri_id in friend:
        print('QQ号为:  '+fri_id+'    此人是你的好友:  '+str(friend[fri_id]))
        print('他/她/ta的信息为:  ')
        print('QQ号码:  ' + str(fri_id) + '    昵称:  ' + friend[fri_id])
        pic.informations(informations_Dict)
    else:
        print('此人不是你的好友')


    
    if cmdList[2] == '1':
        print('正在下载好友相册...')
        try:
            pic.download()
            print('照片下载完毕')
            f = True
        except Exception as e:
            f = False
            print('对不起出现错误' + e)
    else:
        pass
    #爬取留言板
    if cmdList[3] == '1':
        print('正在爬取好友留言板...')
        pic.note()
        print('爬取完毕,并已经存入note.csv')
        print('正在处理...')
        get_wordcloud('note.txt')
        print('处理完毕')
    else:
        pass
        #print('不好意思了,这位朋友禁止你访问他的空间')


