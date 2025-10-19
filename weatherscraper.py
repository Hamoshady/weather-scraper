import re  # مكتبة regular expressions للبحث داخل النصوص باستخدام أنماط معينة

def get_forecast_data():
    # ✅ استيراد المكتبات المطلوبة داخل الدالة (بتشتغل وقت التنفيذ فقط)
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup

    # ✅ إعداد خيارات تشغيل متصفح Chrome
    options = Options()
    options.add_argument('--headless')       # تشغيل المتصفح في الخلفية بدون واجهة
    options.add_argument('--disable-gpu')    # تعطيل استخدام كارت الشاشة (لتقليل الحمل)
    options.add_argument('--no-sandbox')     # منع مشاكل الصلاحيات في بعض الأنظمة
    options.add_argument('--log-level=3')    # تقليل الرسائل التحذيرية في الكونسول

    # ✅ تعطيل تحميل الصور والإشعارات والميديا لتسريع تحميل الصفحة
    prefs = {
        "profile.default_content_setting_values": {
            "images": 2,          # تعطيل الصور
            "plugins": 2,         # تعطيل الإضافات
            "popups": 2,          # تعطيل النوافذ المنبثقة
            "notifications": 2,   # تعطيل الإشعارات
            "media_stream": 2,    # تعطيل الميديا (كاميرا/مايك)
        }
    }
    options.add_experimental_option("prefs", prefs)

    # ✅ إنشاء متصفح Chrome بالإعدادات السابقة
    driver = webdriver.Chrome(options=options)

    # ✅ زيارة الموقع حتى يتم تسجيل الدومين (ضروري قبل إضافة الكوكي)
    driver.get("https://world-weather.info/")

    # ✅ إضافة كوكي لتفعيل درجة الحرارة بوحدة "السيلسيوس"
    driver.add_cookie({"name": "celsius", "value": "1"})

    # ✅ تحديث الصفحة لتطبيق الكوكي فعليًا
    driver.refresh()

    # ✅ أخذ نسخة من كود HTML بعد تفعيل الكوكي
    html = driver.page_source

    # ✅ تحليل الصفحة باستخدام مكتبة BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # ✅ إيجاد القسم اللي يحتوي على بيانات المدن والطقس
    resorts = soup.find("div", id="resorts")

    # ✅ استخراج أسماء المدن باستخدام تعبير منتظم (Regular Expression)
    re_cities = r'">([\w\s]+)</a><span>'
    cities = re.findall(re_cities, str(resorts))

    # ✅ استخراج درجات الحرارة من الصفحة
    re_temps = r'<span>(\+\d+|-\d+)<span'
    temps = re.findall(re_temps, str(resorts))

    # ✅ تحويل القيم النصية للأرقام (int)
    temps = [int(temp) for temp in temps]

    # ✅ البحث عن كل العناصر اللي تحتوي على الحالة الجوية (Tooltip)
    conditions_tags = resorts.find_all('span', class_='tooltip')

    # ✅ استخراج وصف الحالة الجوية من خاصية "title"
    conditions = [condition.get('title') for condition in conditions_tags]

    # ✅ دمج المدن + درجات الحرارة + الحالات الجوية في قائمة واحدة
    data = zip(cities, temps, conditions)

    # ✅ عرض النتائج في شكل قائمة من التابعات (tuples)
    print(list(data))

    # ✅ إغلاق المتصفح بعد الانتهاء
    driver.quit()


# ✅ تشغيل الدالة
get_forecast_data()
