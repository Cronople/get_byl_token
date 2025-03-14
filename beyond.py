import time
import requests
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from lxml import etree
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def get_media_token(url):
    try:
        options = Options()
        options.add_argument("--headless")  # 브라우저 창을 열지 않음
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(5)  # 페이지 로드 대기
        
        cookies = driver.get_cookies()
        driver.quit()
        
        for cookie in cookies:
            if cookie['name'] == 'mediaToken':
                return cookie['value']
    except Exception as e:
        print(f"Error getting media token: {e}")
    return None

def get_mpd_url(url, media_token):
    try:
        headers = {"authorization": f"Bearer {media_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_data = response.json()
            return json_data.get("singleHdDashUrl")
    except Exception as e:
        print(f"Error getting MPD URL: {e}")
    return None

def parse_mpd_and_download(url):
    downloaded_init_files = set()  # 이미 다운로드된 init 파일 추적
    
    while True:
        try:
            media_token = get_media_token(url)
            if not media_token:
                print("Media Token을 찾을 수 없습니다.")
                continue
            
            mpd_url = get_mpd_url(url, media_token)
            if not mpd_url:
                print("MPD URL을 찾을 수 없습니다.")
                continue
            
            headers = {"authorization": f"Bearer {media_token}"}
            response = requests.get(mpd_url, headers=headers)
            if response.status_code != 200:
                print("MPD 파일을 가져오지 못했습니다.")
                continue
            
            tree = etree.fromstring(response.content)
            namespace = {'mpd': 'urn:mpeg:dash:schema:mpd:2011'}
            
            adaptation_sets = tree.xpath("//mpd:AdaptationSet", namespaces=namespace)
            selected_ids = [0, 4]
            
            for adaptation_set in adaptation_sets:
                adaptation_id = adaptation_set.get("id")
                if adaptation_id and int(adaptation_id) in selected_ids:
                    segment_template = adaptation_set.find(".//mpd:SegmentTemplate", namespaces=namespace)
                    if segment_template is not None:
                        init_url = segment_template.get("initialization")
                        media_url = segment_template.get("media")
                        
                        if adaptation_id not in downloaded_init_files:
                            try:
                                init_data = requests.get(init_url, headers=headers).content
                                with open(f"init_{adaptation_id}.m4s", "wb") as f:
                                    f.write(init_data)
                                print(f"Init file saved: init_{adaptation_id}.m4s")
                                downloaded_init_files.add(adaptation_id)
                            except Exception as e:
                                print(f"Error downloading init file: {e}")
                        
                        try:
                            media_data = requests.get(media_url, headers=headers).content
                            with open(f"media_{adaptation_id}.m4s", "wb") as f:
                                f.write(media_data)
                            print(f"Media file saved: media_{adaptation_id}.m4s")
                        except Exception as e:
                            print(f"Error downloading media file: {e}")
                        
            print("20초 대기 중...")
            time.sleep(20)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(20)

if __name__ == "__main__":
    webpage_url = "https://example.com"  # 실제 웹페이지 URL
    parse_mpd_and_download(webpage_url)
