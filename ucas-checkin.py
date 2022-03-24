import webbrowser

print('正在为您搜索报到信息……')
webbrowser.open('https://www.baidu.com/s?wd=报到 site:ucas.ac.cn')
answer = input('找到报到信息了吗？（Y/N）')
if answer.lower() != 'y':
    print('不好意思，现在还没有到报到时间，改天再来试试吧 :)')
    exit(0)

webbrowser.open('https://www.baidu.com/s?wd=时间')
answer = input('现在的时间是报到时间吗？（Y/N）')
if answer.lower() != 'y':
    print('不好意思，现在还没有到报到时间，改天再来试试吧 :)')
    exit(0)

print('恭喜你，那么现在开始报到吧 :)')
webbrowser.open('https://sep.ucas.ac.cn/')

# # TODO
# def send_mail():
#     """
#     发送提醒邮件
#     """
#     webbrowser.open('https://mail.cstnet.cn/')
