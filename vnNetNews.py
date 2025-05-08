from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from bs4 import BeautifulSoup
import pandas as pd
import schedule

#Đề tài Web việc làm VietNamNet
def DocBaoMoiNgay():
    #Vào website VietNamNet
    driver = webdriver.Edge()
    driver.get("https://vietnamnet.vn")
    time.sleep(4)

    #Click chọn một mục tin tức bất kì
    menu_links = driver.find_elements(By.CSS_SELECTOR, "nav a")
    valid_links = [link for link in menu_links if link.text.strip() and link.get_attribute("href")]
    random_link = random.choice(valid_links)
    random_link.click()
    time.sleep(4)

    #Cuộn trang (để cho nút tìm kiếm không bị quảng cáo che)
    scroll_pixels = 100
    driver.execute_script(f"window.scrollBy(0, {scroll_pixels});")

    #Bấm tìm kiếm
    try:
        search_button = driver.find_element(By.CLASS_NAME, "search-small__form-btn")
        search_button.click()
    except:
        print("Không bấm tìm kiếm được")

    time.sleep(5)

    #Cuộn trang 
    scroll_pixels = 500
    driver.execute_script(f"window.scrollBy(0, {scroll_pixels});")
    time.sleep(2)
    #lấy html
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    news_items = soup.find_all('div', class_='horizontalPost__main')

    data = []
    #Lấy tất cả dữ liệu(Tiêu đề, Mô tả, Hình ảnh, Nội dung bài viết) hiển thị ở bài viết.
    for item in news_items:
        #html = driver.page_source
        #soup = BeautifulSoup(html, "html.parser")
        #Lấy tiêu đề bài viết
        try:
            tieude_element = item.find('h3', class_=lambda x: x and 'title' in x) or item.find('a', class_=lambda x: x and 'title' in x)
            #tieude = soup.find('h3', class_='horizontalPost__main-title  vnn-title title-bold')
            tieude = tieude_element.get_text(strip=True)
        except:
            tieude = "Lỗi"

        #Lấy mô tả (tóm tắt nội dung)
        try:
            mota_element = item.find('div', class_=lambda x: x and 'desc' in x) or item.find('p')
            #mota = soup.find('div', class_='horizontalPost__main-desc')
            mota = mota_element.get_text(strip=True)
        except:
            mota = "Lỗi"

        #Lấy hình ảnh
        try:
            hinhanh = item.find_parent('div', class_='horizontalPost')
            img_tag = hinhanh.find('img') if hinhanh else item.find('img')

            hinhanh_url = img_tag.get('data-srcset') or img_tag.get('src') or "Không có ảnh"
            hinhanh_url = hinhanh_url.split('?')[0]
        except:
            hinhanh_url = "Không có ảnh"
        
        #Lấy nội dung bài viết
        #body = soup.find("div", id="maincontent")
        #try:
            #noidung = body.decode_contents()
        #except:
            #noidung = ""
        
        item = [tieude, mota, hinhanh_url]
        data.append(item)

    #Lưu dữ liệu đã lấy được vào file excel
    df1 = pd.DataFrame(data, columns=["Tiêu đề", "Mô tả", "Hình ảnh"])
    df1.to_excel("dtVNNetNews.xlsx")
    driver.quit()

#Set lịch chạy lúc 6h sáng everyday
schedule.every().day.at("06:00").do(DocBaoMoiNgay)
print("Đang chờ 6h sáng để chạy.")
while True:
    schedule.run_pending()
    time.sleep(60) 