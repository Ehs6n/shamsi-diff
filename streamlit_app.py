import streamlit as st
import jdatetime
from dateutil.relativedelta import relativedelta

# --- 1. تنظیمات صفحه باید اولین دستور Streamlit باشد ---
st.set_page_config(
    layout="wide",
    page_title="محاسبه‌گر اختلاف تاریخ شمسی",
    initial_sidebar_state="collapsed"
)

# --- 2. تعریف توابع اصلی برنامه ---
def calculate_shamsi_date_difference(date_str1, date_str2):
    """
    دو تاریخ شمسی را به صورت رشته دریافت کرده و اختلاف آن‌ها را
    به سال و ماه محاسبه می‌کند.
    """
    try:
        date_str1 = date_str1.strip()
        date_str2 = date_str2.strip()

        year1, month1, day1 = map(int, date_str1.split('/'))
        jalali_date1 = jdatetime.date(year1, month1, day1)

        year2, month2, day2 = map(int, date_str2.split('/'))
        jalali_date2 = jdatetime.date(year2, month2, day2)

        gregorian_date1 = jalali_date1.togregorian()
        gregorian_date2 = jalali_date2.togregorian()

        difference = relativedelta(gregorian_date2, gregorian_date1)

        years = difference.years
        months = difference.months
        return years, months
    except ValueError:
        return "خطا: فرمت تاریخ وارد شده نامعتبر است. لطفاً از فرمت 'YYYY/MM/DD' استفاده کنید."
    except Exception as e:
        return f"خطا در پردازش تاریخ‌ها: {e}"

# --- 3. اعمال CSS برای فونت وزیرمتن، RTL و تنظیمات خاص ---
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');

    /* تنظیمات عمومی برای فونت و راست‌چینی کل برنامه */
    html, body, [class*="st-"], .stApp {
        direction: rtl !important;
        font-family: 'Vazirmatn', Arial, sans-serif !important;
    }

    /* تنظیمات عمومی چینش متن برای اکثر المان‌ها */
    h1, h2, h3, h4, h5, h6, p, div:not([data-testid="stTextArea"]):not(.stButton), 
    span, li, table, .stMarkdown, .stTextInput input, .stCodeBlock pre {
        text-align: right !important;
    }
    /* اطمینان از فونت وزیر برای تمام دکمه‌ها */
     button, .stButton button {
         font-family: 'Vazirmatn', Arial, sans-serif !important;
    }

    /* ----- چپ‌چین کردن کادر ورود تاریخ ----- */
    /* Streamlit از data-testid برای شناسایی المان‌ها استفاده می‌کند که برای انتخاب پایدارتر است */
    div[data-testid="stTextArea"] textarea {
        direction: ltr !important;  /* جهت متن چپ‌چین */
        text-align: left !important; /* چینش متن به چپ */
        font-family: 'Vazirmatn', Arial, sans-serif !important; /* استفاده از فونت وزیر که اعداد لاتین را هم خوب نمایش می‌دهد */
    }
    /* چپ‌چین کردن placeholder در کادر ورود تاریخ */
    div[data-testid="stTextArea"] textarea::placeholder {
        direction: ltr !important;
        text-align: left !important;
        opacity: 0.7;
    }

    /* ----- وسط‌چین کردن دکمه محاسبه ----- */
    /* این استایل به div والد دکمه اعمال می‌شود */
    div.stButton {
        display: flex !important;          /* استفاده از Flexbox */
        justify-content: center !important; /* دکمه در مرکز افقی کانتینر خودش قرار می‌گیرد */
        width: 100%; /* اطمینان از اینکه کانتینر دکمه عرض کامل را اشغال می‌کند تا وسط‌چینی معنی‌دار باشد */
    }
    /* اگر می‌خواهید متن داخل خود دکمه هم وسط‌چین باشد (معمولا پیش‌فرض است) */
    /* div.stButton > button {
        text-align: center !important;
    } */

    /* برای اطمینان از نمایش صحیح متن در st.code (خروجی) */
    .stCodeBlock pre {
        text-align: right !important; /* خروجی راست‌چین */
        white-space: pre-wrap !important;
    }
</style>
""", unsafe_allow_html=True)


# --- 4. رابط کاربری Streamlit ---
st.title("محاسبه‌گر اختلاف دو تاریخ شمسی")
# st.markdown("این برنامه اختلاف بین دو تاریخ شمسی را بر حسب سال و ماه برای هر خط ورودی محاسبه می‌کند.") # این متن توسط CSS راست‌چین می‌شود

st.header("ورودی داده‌ها")
# st.markdown("تاریخ‌ها را ...") # این متن توسط CSS راست‌چین می‌شود

input_text = st.text_area(
    "داده‌های تاریخ را اینجا وارد یا پیست کنید (هر جفت تاریخ در یک خط، جدا شده با کاما. مثال: 1370/01/10,1375/02/15):",
    height=150,
    key="date_input_area_multiline_rtl_v3",
    placeholder="1370/01/01,1375/02/15\n1380/11/05,1382/01/20" # placeholder به صورت LTR نمایش داده خواهد شد
)

if st.button("محاسبه اختلاف", key="calculate_button_multiline_rtl_v3"):
    if not input_text.strip():
        st.warning("لطفاً داده‌های تاریخ را وارد کنید.")
    else:
        input_lines = input_text.strip().split('\n')
        
        simplified_output_lines = []
        detailed_log_lines = []
        any_valid_line_found_for_processing = False

        for i, line_content in enumerate(input_lines):
            original_line_for_display = line_content.strip() 
            if not original_line_for_display:
                continue
            
            any_valid_line_found_for_processing = True
            parts = original_line_for_display.split(',')
            
            if len(parts) == 2:
                date_input1 = parts[0].strip()
                date_input2 = parts[1].strip()
                result = calculate_shamsi_date_difference(date_input1, date_input2)

                if isinstance(result, tuple):
                    years_diff, months_diff = result
                    clean_diff_text = f"{abs(years_diff)} سال و {abs(months_diff)} ماه"
                    simplified_output_lines.append(clean_diff_text)
                    
                    full_info_diff_text = clean_diff_text
                    if years_diff < 0 or (years_diff == 0 and months_diff < 0) :
                        full_info_diff_text += " (تاریخ دوم کوچکتر از تاریخ اول است)"
                    detailed_log_lines.append(f"خط «{original_line_for_display}»: {full_info_diff_text}") # حذف شماره خط برای خوانایی بهتر لاگ
                else: 
                    error_msg = f"خط «{original_line_for_display}»: {result}"
                    detailed_log_lines.append(error_msg)
            else: 
                error_msg = f"خط «{original_line_for_display}»: خطا در فرمت خط. باید دو تاریخ جدا شده با کاما باشد."
                detailed_log_lines.append(error_msg)
        
        if simplified_output_lines:
            st.subheader("نتایج محاسبات (فقط اختلاف سال و ماه)")
            # st.markdown("---") # این خط توسط CSS راست‌چین می‌شود
            final_simplified_block = "\n".join(simplified_output_lines)
            st.code(final_simplified_block, language=None) # این بلوک توسط CSS راست‌چین می‌شود
        elif any_valid_line_found_for_processing: 
            st.info("هیچ نتیجه موفقیت آمیزی برای نمایش در لیست خلاصه وجود ندارد. لطفاً گزارش کامل را برای بررسی خطاها مشاهده کنید.")

        if detailed_log_lines: 
            st.subheader("گزارش کامل پردازش")
            # st.markdown("---") # این خط توسط CSS راست‌چین می‌شود
            full_log_block = "\n".join(detailed_log_lines)
            log_area_height = min(300, max(100, len(detailed_log_lines) * 25 + 20)) 
            st.text_area(
                "جزئیات پردازش هر خط:",
                value=full_log_block, 
                height=log_area_height,
                key="detailed_log_area_rtl_v3",
                disabled=True 
            ) # این text_area توسط CSS راست‌چین می‌شود
        
        if not any_valid_line_found_for_processing and input_text.strip():
             st.info("ورودی داده شد اما هیچ خطی که قابل پردازش باشد یافت نشد.")

