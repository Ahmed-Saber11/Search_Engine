import requests
from bs4 import BeautifulSoup
import os
import re
from datetime import datetime

# ملفات الإدخال والإخراج
urls_file = r'C:\Users\khaled\Desktop\Project_Big_Data\urls.txt'
output_folder = r'C:\Users\khaled\Desktop\Project_Big_Data\Pages'
saved_urls_file = os.path.join(output_folder, 'saved_urls.txt')

# تجهيز مجلد الإخراج
os.makedirs(output_folder, exist_ok=True)

# تحميل الروابط اللي اتحفظت قبل كده (لو فيه)
if os.path.exists(saved_urls_file):
    with open(saved_urls_file, 'r', encoding='utf-8') as f:
        saved_urls = set(line.strip() for line in f if line.strip())
else:
    saved_urls = set()

# دالة لتحويل الرابط إلى اسم ملف آمن مع الوقت
def safe_filename(url):
    url_clean = re.sub(r'^https?://', '', url)
    filename = re.sub(r'[\\/*?:"<>|]', '_', url_clean)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{filename}_{timestamp}.txt"

# قراءة الروابط من الملف (من السطر 99980)
with open(urls_file, 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in list(f)[113637:] if line.strip()]

# إزالة التكرار مع الحفاظ على الترتيب
urls = list(dict.fromkeys(urls))

# معالجة كل رابط
for url in urls:
    if url in saved_urls:
        print(f'[⚠] Already downloaded: {url}')
        continue

    try:
        # اسم الملف الناتج
        filename = safe_filename(url)
        filepath = os.path.join(output_folder, filename)

        # تحميل الصفحة
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # استخراج النص
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text(separator='\n', strip=True)

        # كتابة النص في الملف
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(page_text)

        # تسجيل الرابط في ملف saved_urls
        with open(saved_urls_file, 'a', encoding='utf-8') as f:
            f.write(url + '\n')

        print(f'[✔] Saved: {filename}')

    except Exception as e:
        print(f'[✖] Error fetching {url}: {e}')
