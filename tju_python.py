# tju_python
import requests
import re
import os

class Question(object):
    questionlist = []
    def __init__(self, num, attr, question, ansdict, true_ans, type):
        self.num = len(Question.questionlist) + 1
        self.attr = attr
        self.type = type
        self.question = question
        self.ansdict = ansdict
        self.true_ans = true_ans
        Question.questionlist.append(self)
    
    def matchson(self, question):
        if self.question == question:
            return True
        else:
            return False

    def printall(self):
        print(self.num, self.question)
        print(self.ansdict)
        print(self.true_ans)

    @classmethod
    def match(cls, question):
        for que in cls.questionlist:
            if que.matchson(question):
                return que.true_ans
    
    def write(self):
        path = 'D:\\tju_exam\\'
        ans_str = ''
        for ans in self.ansdict.keys():
            ans_str += '{}：{}\n'.format(ans, self.ansdict[ans].strip())
        writestr = '#:#\n{}. {}\n{}\n正确答案：{}\n#*#\n\n'.format(self.num, self.question, ans_str.strip(), self.true_ans)
        if not os.path.exists(path):
            os.mkdir(path)
        path += self.type + '.txt'
        with open(path, 'a', encoding = 'utf-8') as f:
            f.write(writestr)


def getHTMLText(url, headers = {}, cookies = {}):
    try:
        r=requests.get(url, headers = headers, cookies = cookies)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text, r.apparent_encoding
    except:
        return 'get error!'

def getPostText(url, data, headers, cookies, encoding = ''):
    try:
        post = requests.post(url, data = data, headers = headers, cookies = cookies)
        post.raise_for_status()
        post.encoding = post.apparent_encoding
        if encoding:
            post.encoding = encoding
        return post.text, post.encoding
    except:
        print('post error!')

def getDict(text, patten):
    lis = text.split(patten)
    cookieDict = {}
    for str in lis:
        cookie = str.strip().split('=')
        cookieDict[cookie[0]] = cookie[1]
    return cookieDict

def get_headersDict(text):
    text = text.strip().split('\n')
    headers = {x.split(':', 1)[0].strip(): x.split(':', 1)[1].strip() for x in text}
    return headers

def get_questionclass(post, type):
    lis = re.findall('\d+&nbsp;&nbsp;[\s\S]+?正确答案[\s\S]+?</font>', post)
    for str in lis:
        str = re.sub('[\t\n]','', str)
        num = re.search('\d+&nbsp;&nbsp;', str).group(0).strip('&nbsp;&nbsp;')
        attr = re.search('&nbsp;&nbsp;[\s\S]+?<', str).group(0).strip('&nbsp;&nbsp;').strip('<')
        question = re.search('blank">.+?<', str).group(0).strip('blank"<>')
        true_ans = re.search('none;">.+?<', str).group(0).strip('none;"><').strip()
        anslist = re.findall('>[A-Z]+?&nbsp;.+?<', str)
        ansdict = {anslist[i].strip('<>').split('&nbsp;')[0]:anslist[i].strip('<>').split('&nbsp;')[1] for i in range(len(anslist))}
        temp = Question(num, attr, question, ansdict, true_ans, type)

def read_exam():
    path = 'D:\\tju_exam\\'
    listdir = os.listdir(path)
    for dir in listdir:
        s_path = path + dir
        type = dir.strip('.txt')
        with open(s_path, 'r', encoding = 'utf-8') as f:
            text = f.read()
        str = re.findall('#:#[\s\S]+?#\*#', text)
        for each in str:
            lis = each.strip('#*:\n').split('\n')
            num = lis[0].split('. ')[0]
            question = lis[0].split('. ')[1].strip()
            if not lis[1]:
                ansdict = {}
            else:
                ansdict = {lis[i].split('：')[0]:lis[i].split('：')[1] for i in range(1, len(lis) - 1)}
            true_ans = lis[-1].split('：')[1]
            if not ansdict:
                attr = '判断题'
            elif ',' in true_ans:
                attr = '多选题'
            else:
                attr = '单选题'
            tmp = Question(num, attr, question, ansdict, true_ans, type)
    # for each in Question.questionlist:
    #     ans_str = ''
    #     for ans in each.ansdict.keys():
    #         ans_str += '{}：{}\n'.format(ans, each.ansdict[ans].strip())
    #     writestr = '#:#\n{}. {}\n{}\n正确答案：{}\n#*#\n\n'.format(each.num, each.question, ans_str.strip(), each.true_ans)
    #     with open('D:\\all.txt','a',encoding='utf-8') as f:
    #         f.write(writestr)
        


    


def spider_exam():
    
    # url1 = 'http://aqjy.tongji.edu.cn/exam/studenttest/studentTestAction!gotoStudyThemePassAnswer.do'
    # url2 = 'http://aqjy.tongji.edu.cn/exam/studenttest/studentTestAction!gotoStudyThemePass.do'
    url_gettype = 'http://aqjy.tongji.edu.cn/exam/studenttest/studentTestAction!gotoStudy.do'
    url_getexam = 'http://aqjy.tongji.edu.cn/exam/studenttest/studentTestAction!gotoSearchTheme.do'
    headerstext = '''
    Host: aqjy.tongji.edu.cn
Connection: keep-alive
Content-Length: 0
Accept: */*
DNT: 1
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.59 Safari/537.36 Edg/85.0.564.30
Origin: http://aqjy.tongji.edu.cn
Referer: http://aqjy.tongji.edu.cn/userOperation!afterLogin.do
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=8de440372b138472daba9c9f6f822180
    '''
    headers = get_headersDict(headerstext)
    cookies = getDict('JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=8de440372b138472daba9c9f6f822180', ';')
    data = getDict('knowid=453697&deptId=0&searchword=&themelx=&pageNum=2&pageMax=20&TimeStemp=0.5242743930694707', '&')
    data_type = getDict('TimeStemp=0.9514742369670208','&')
    post,post_encoding = getPostText(url_gettype, data_type, headers, cookies)
    typelist = re.findall('value="\d+?">.+?</option>', post)
    typeDict = {re.search('\d+', each).group(0):re.search('>.+?<', each).group(0).strip('<>') for each in typelist}
    for key in typeDict.keys():
        type = typeDict[key]
        print('正在爬取{}'.format(type))
        data['knowid'] = key
        if '学院' in type:
            data['knowid'] = -1
            data['deptId'] = key
        post,post_encoding = getPostText(url_getexam, data, headers, cookies)
        minpage = re.search('\d+',re.search('javascript:goPageList[\s\S]+?最前页', post).group(0)).group(0)
        maxpage = re.search('\d+',re.search('下一页[\s\S]+?javascript:goPageList[\s\S]+?最后页', post).group(0)).group(0)
        for i in range(int(minpage), int(maxpage) + 1):
            print('第{}页'.format(i))
            data['pageNum'] = i
            post,post_encoding = getPostText(url_getexam, data, headers, cookies)
            get_questionclass(post, type)
        print('正在导出题库...')
        for i in Question.questionlist:
            i.write()

def get_single_question():
    url = 'http://aqjy.tongji.edu.cn/exam/studenttest/studentTestAction!gotoStudyThemePass.do'
    headerstext = '''
    Host: aqjy.tongji.edu.cn
Connection: keep-alive
Content-Length: 33
Cache-Control: max-age=0
Origin: http://aqjy.tongji.edu.cn
Upgrade-Insecure-Requests: 1
DNT: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.59 Safari/537.36 Edg/85.0.564.30
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://aqjy.tongji.edu.cn/exam/studenttest/studentTestAction!gotoStudyThemePassAnswer.do
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=146bfb76168425193b554a2daf8eee5b
    '''
    headers = get_headersDict(headerstext)
    cookies = getDict('JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=146bfb76168425193b554a2daf8eee5b', ';')
    data = getDict('pageNum=2&knowid=-1&deptId=447122', '&')
    for i in range(1,20):
        data['pageNum'] = i
        post, post_encoding = getPostText(url, data, headers, cookies)
        text_raw = re.search('>\d+?\.[\s\S]+?提交答案',post).group(0)
        text = re.sub('[\t\n]','', text_raw)
        num = re.search('\d+?\.', text).group(0).strip('.')
        question = re.search('<td style="border: 0;"[\s\S]+?<',text).group(0).split('>')[1].strip('>< ').strip()
        anstextlis = re.findall('answerradio" />[\s\S]+?&nbsp;[\s\S]+?<', text)
        ansdict = {ansstr.split('>')[1].strip('<> ').split('、&nbsp;')[0]:ansstr.split('>')[1].strip('<> ').split('、&nbsp;')[1] for ansstr in anstextlis}
        nid = re.search('ntThemeId" value="\d+?"', post).group(0).split('=')[1].strip('"')
        print('{}题设：{}'.format(num, question))
        true_ans = ''
        for each in Question.questionlist:
            if each.question == question:
                true_ans = each.true_ans
                print(true_ans)
                break
        if true_ans == '对':
            true_ans = 'A'
        elif true_ans == '错':
            true_ans = 'B'
        post_ans(num, nid, true_ans)

def post_ans(num, nid, true_ans):
    url = 'http://aqjy.tongji.edu.cn/exam/studenttest/studentTestAction!gotoStudyThemePassAnswer.do'
    headerstext = '''
    Host: aqjy.tongji.edu.cn
Connection: keep-alive
Content-Length: 163
Cache-Control: max-age=0
Origin: http://aqjy.tongji.edu.cn
Upgrade-Insecure-Requests: 1
DNT: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.59 Safari/537.36 Edg/85.0.564.30
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://aqjy.tongji.edu.cn/exam/studenttest/studentTestAction!gotoStudyThemePass.do
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=146bfb76168425193b554a2daf8eee5b
    '''
    headers = get_headersDict(headerstext)
    cookies = getDict('JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=146bfb76168425193b554a2daf8eee5b', ';')
    data = getDict('pageNum=11&ntThemeId=3300366&deptId=447122&knowid=-1&fk_type=3&maxPage=100&titleMsg=%BB%B7%BE%B3%BF%C6%D1%A7%D3%EB%B9%A4%B3%CC%D1%A7%D4%BA%CC%E2%BF%E2&answerradio=B', '&')
    data['pageNum'] = num
    data['answerradio'] = true_ans
    data['ntThemeId'] = nid
    post, post_encoding = getPostText(url, data, headers, cookies)
    num = re.search('>\d+?.<', post).group(0).strip('><.')
    question = re.search('题干.+?<', post).group(0).strip('<')
    receive = re.search('font color=".+?">.+?<', post).group(0).split('>')[1].strip('<').strip()
    print(num, question)
    print(receive)

def get_single_exam():
    data_raw = 'exameid=17434077&pageNum=2&paperid=6668769&answerRealtimeId=&answerRealtimeNum=1&userRealtimeId=17715962&fk_type=1&zc=&answerradio=B'
    data_rawdict = getDict(data_raw, '&')
    EXAMID = data_rawdict['exameid']
    PAPERID = data_rawdict['paperid']
    REALTIMEID = data_rawdict['userRealtimeId']
    if os.path.exists('d:\\error.log'):
        os.remove('d:\\error.log')
    url_start = 'http://aqjy.tongji.edu.cn/exam/studentexame/studentExameAction!gotoExame.do'
    url_sa = 'http://aqjy.tongji.edu.cn/exam/studentexame/studentExameAction!saveAnswerAndGetNextExameTheme.do'
    headerstext_sa = '''
Host: aqjy.tongji.edu.cn
Connection: keep-alive
Content-Length: 131
Cache-Control: max-age=0
Origin: http://aqjy.tongji.edu.cn
Upgrade-Insecure-Requests: 1
DNT: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.59 Safari/537.36 Edg/85.0.564.30
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://aqjy.tongji.edu.cn/exam/studentexame/studentExameAction!gotoExame.do
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=3890dfc3ca411f47f9f963b7c1803ea8
    '''
    headerstext_start ='''
Host: aqjy.tongji.edu.cn
Connection: keep-alive
Content-Length: 15
Cache-Control: max-age=0
Origin: http://aqjy.tongji.edu.cn
Upgrade-Insecure-Requests: 1
DNT: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.59 Safari/537.36 Edg/85.0.564.30
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://aqjy.tongji.edu.cn/exam/studentexame/studentExameAction!beforeGotoExame.do?exameid=1340246&TimeStemp=0.4999727373612728
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=3890dfc3ca411f47f9f963b7c1803ea8
    '''
    headers_start = get_headersDict(headerstext_start)
    headers_sa = get_headersDict(headerstext_sa)
    cookies = getDict('JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=3890dfc3ca411f47f9f963b7c1803ea8', ';')
    data_sa = getDict('exameid=1340246&pageNum=3&paperid=1340364&answerRealtimeId=&answerRealtimeNum=2&userRealtimeId=17706242&fk_type=1&zc=&answerradio=B', '&')
    data_start = getDict('exameid=1340246', '&')
    data_start['exameid'] = EXAMID
    data_sa['exameid'] = EXAMID
    data_sa['paperid'] = PAPERID
    data_sa['userRealtimeId'] = REALTIMEID
    post, post_encoding = getPostText(url_start, data_start, headers_start, cookies)
    page_total = int(re.search('共&nbsp;\d+?&nbsp;题', post).group(0).split('&nbsp;')[1])
    text_raw = re.search('>\d+?\.[\s\S]+?下一题',post).group(0)
    text = re.sub('[\t\n]','', text_raw)
    num = re.search('\d+?\.', text).group(0).strip('.')
    question = re.search('<td style="border: 0;"[\s\S]+?<',text).group(0).split('>')[1].split('(分数')[0].strip()
    attr = re.search('(判断|单选|多选)题', post).group(0)
    true_ans = ''
    for each in Question.questionlist:
        if each.question == question and each.attr == attr:
            true_ans = each.true_ans
            break
    if true_ans == '对':
        true_ans = 'A'
    elif true_ans == '错':
        true_ans = 'B'
    print(question)
    print(true_ans)
    page_total = 100
    for i in range(1, page_total + 1):
        data_sa['pageNum'] = i + 1
        if i == page_total:
            data_sa['pageNum'] = i - 1
        data_sa['answerRealtimeNum'] = i
        data_sa['answerradio'] = true_ans
        post, post_encoding = getPostText(url_sa, data_sa, headers_sa, cookies)
        if i == page_total:
            break
        if i != page_total - 1:
            text_raw = re.search('>\d+?\.[\s\S]+?下一题',post).group(0)
        else:
            text_raw = re.search('>\d+?\.[\s\S]+?上一题',post).group(0)
        text = re.sub('[\t\n]','', text_raw)
        num = re.search('\d+?\.', text).group(0).strip('.')
        question = re.search('<td style="border: 0;"[\s\S]+?<',text).group(0).split('>')[1].split('(分数')[0].strip()
        attr = re.search('(判断|单选|多选)题', post).group(0)
        print(num)
        print(question)      
        true_ans = ''
        for each in Question.questionlist:
            if each.question == question and each.attr == attr:
                true_ans = each.true_ans
                break
        if not true_ans:
            log = num + '\n' + question + '\n'
            with open('D:\\error.log','a',encoding='utf-8') as f:
                f.write(log)
        if true_ans == '对':
            true_ans = 'A'
        elif true_ans == '错':
            true_ans = 'B'
        print(true_ans)
    url_sub = 'http://aqjy.tongji.edu.cn/exam/studentexame/studentExameAction!submitPaperComputeGrade.do'
    headerstext_sub = '''
    Host: aqjy.tongji.edu.cn
Connection: keep-alive
Content-Length: 131
Cache-Control: max-age=0
Origin: http://aqjy.tongji.edu.cn
Upgrade-Insecure-Requests: 1
DNT: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.59 Safari/537.36 Edg/85.0.564.30
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://aqjy.tongji.edu.cn/exam/studentexame/studentExameAction!gotoExame.do
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: JSESSIONID=aOxZJqQDSDEgfMvOGp; oiosaml-fragment=; iPlanetDirectoryPro=146bfb76168425193b554a2daf8eee5b
    '''
    headers_sub = get_headersDict(headerstext_sub)
    data_sub = data_sa
    post, post_encoding = getPostText(url_sub, data_sub, headers_sub, cookies)

def main():
    read_exam()
    # get_single_question()
    # post_ans()
    get_single_exam()

    
    
    
    

if __name__ == '__main__':
    main()

        