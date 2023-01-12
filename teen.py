from selenium import webdriver
from bs4 import BeautifulSoup
import time
SCROLL_PAUSE_TIME = 5

# 크롬 headless 모드 사용
options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=800x1080')
options.add_argument("disable-gpu")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# browser = webdriver.Chrome(options=options)

# 크롬 드라이버 연결
# driver = webdriver.Chrome('C:/Users/82109/Downloads/chromedriver_win32/chromedriver.exe', options=options)
driver.get('https://teen.munjang.or.kr/archives/category/old-excl')
driver.implicitly_wait(3)

# 무한 스크롤 
# 마지막 창 높이 저장
last_height = driver.execute_script("return document.body.scrollHeight") 
 
cnt = 0

while True:
    # 창 높이까지 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
    
    # 페이지 로딩 기다리기
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(SCROLL_PAUSE_TIME)

    # 스크롤이 된 후의 창 높이를 새로운 높이로 저장하고, 이전 높이와 변하지 않았다면 스크롤 종료
    if new_height == last_height:
        cnt += 1
        print(cnt)
        break

    last_height = new_height

# 콘텐츠 주소 크롤링
html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

crawled = soup.find_all("a",{"rel":"bookmark"})

#BASE_URL = "https://teen.munjang.or.kr/archives"
post_links = [i["href"][0:] for i in crawled]
print(len(post_links))
print(post_links)

# 10개 내용 크롤링
driver.execute_script('window.open("https://google.com");')  #구글 창 새 탭으로 열기
time.sleep(2)
driver.switch_to.window(driver.window_handles[-1])  #새로 연 탭으로 이동

for idx, link in enumerate(post_links):
    i = idx
    driver.get(link)
    time.sleep(3)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    try :
        #print("제목")
        temp = soup.find('h1',{'class':"entry-title"})
        text = temp.text
        if text=="":
            print("empty text")
        else:
            with open(f"C:/Users/82109/Desktop/코딩/북커톤/글틴/book_{i}.txt", "w", -1, 'utf-8') as f:
                f.write(text)
            print(str(i)+" 제목")


        #print("카테고리")
        text = ''
        for tmp in soup.find_all('a',{'rel':"category tag"}):
            text += tmp.text
        if text=="":
            print("empty text")
        with open(f"C:/Users/82109/Desktop/코딩/북커톤/글틴/book_{i}.txt", "a", -1, 'utf-8') as f:
            f.write("\n")
            f.write(text)
            print(str(i)+" 카테고리")

        #print("내용")
        soup = BeautifulSoup(html_source, 'html.parser')
        text = ''
        for tmp in soup.find_all('div',{'class':"entry-content"}):
            text += tmp.text
        text = text.replace("\xa0", "")
        with open(f"C:/Users/82109/Desktop/코딩/북커톤/글틴/book_{i}.txt", "w", -1, 'utf-8') as f:
            f.write("\n")
            f.write(text)
            print(str(i)+" 내용")
    except: 
        print(str(i)+" error")
        continue
driver.close()  #링크 이동 후 탭 닫기
driver.switch_to.window(driver.window_handles[-1])  #다시 이전 창(탭)으로 이동
time.sleep(2)