import sys, os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from email.mime.text import MIMEText
import smtplib
import configparser
import json

# クラウドワークス案件へのリンクテキストを整形する関数
def create_anker_text(body, anker):
    return '<a href="https://crowdworks.jp/public/jobs/' + anker + '">' + body + '</a><br>'

# メールを送信する関数
def send_gmail(send_subject, send_message):
    # MIMEの作成
    msg = MIMEText(send_message, "html")
    msg["Subject"] = send_subject
    msg["To"] = gmail_address
    msg["From"] = gmail_address

    # メール送信処理
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(gmail_address, gmail_pass)
    server.send_message(msg)
    server.quit()

# 実行ファイルのディレクトリパスを取得
directory_path = os.path.dirname(os.path.abspath(sys.argv[0]))

# 引数があればディレクトリパスを受け取る
if len(sys.argv) > 1:
    directory_path = sys.argv[1]

congigfile_path = directory_path + os.sep +'config.ini'
config = configparser.RawConfigParser()
config.read(congigfile_path)

crowdworks_account = 'Crowdworks Account'
cw_id = config.get(crowdworks_account, 'cw_id')
cw_pass = config.get(crowdworks_account, 'cw_pass')

gmail_account = 'Gmail Account'
gmail_address = config.get(gmail_account, 'gmail_address')
gmail_pass = config.get(gmail_account, 'gmail_pass')

cw_category_id = 'CW Category ID'
cw_category_id_list = json.loads(config.get(cw_category_id, 'cw_category_id_list').replace("'", '"'))

# Chromedriver設定
options = Options()
options.add_argument('--headless')
chromedriver_path = directory_path + os.sep +'chromedriver'
if os.name == 'nt':
    chromedriver_path = chromedriver_path + '.exe'
driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=options)
time.sleep(2)

# ログイン
cw_login_page_url = 'https://crowdworks.jp/login?ref=toppage_hedder'
driver.get(cw_login_page_url)
time.sleep(2)

elem = driver.find_element_by_xpath("//input[@id='username']")
elem.send_keys(cw_id)

elem = driver.find_element_by_xpath("//input[@id='password']")
elem.send_keys(cw_pass)

elem.send_keys(Keys.RETURN)
time.sleep(2)

html_body = ""

# カテゴリごとにページ情報チェック
for cw_category_id in cw_category_id_list:
    logfile_path = directory_path + os.sep +'cw_job_log_category_' + cw_category_id +'.txt'

    #前回結果読み込み
    job_offer_id_list_previous = []
    if os.path.exists(logfile_path):
        with open(logfile_path, mode = 'r') as fp:
            for line in fp.readlines():
                job_offer_id_list_previous.append(line.replace('\n', ''))

    # 今回結果取得
    job_offer_id_list_present = []
    driver.get('https://crowdworks.jp/public/jobs/search?category_id=' + cw_category_id + '&keep_search_criteria=true&order=new&hide_expired=true')
    time.sleep(2)
    elems = driver.find_elements_by_xpath("//li[@data-job_offer_id]") # TODO クラス名のみで取得
    for elem in elems:
        job_offer_id_list_present.append(elem.get_attribute('data-job_offer_id'))

    #新着がある場合
    if job_offer_id_list_previous != job_offer_id_list_present:
        # メール本文に新着案件情報を追加
        for job_offer_id in list(set(job_offer_id_list_present) - set(job_offer_id_list_previous)):
            job_offer_title = job_offer_id # TODO 新着案件タイトルを取得してメールに記載
            html_body += create_anker_text(job_offer_title, job_offer_id)

        # ログファイル更新
        with open(logfile_path, mode = 'w+') as fp:
            fp.write('\n'.join(job_offer_id_list_present))

# 新着がある場合メールを送信する
if html_body:
    send_gmail('クラウドワークス新着あり', html_body)

#ブラウザを閉じる
driver.quit()