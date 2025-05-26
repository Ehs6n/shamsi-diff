import streamlit as st
import jdatetime
from dateutil.relativedelta import relativedelta

# تابع اصلی محاسبه اختلاف تاریخ بدون تغییر باقی می‌ماند
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
        return "خطا: فرمت تاریخ وارد شده نامعتبر است. باید 'YYYY/MM/DD' باشد."
    except Exception as e:
        return f"خطا در پردازش تاریخ‌ها: {e}"

# --- CSS برای فونت وزیرمتن و RTL ---
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');

    html, body, [class*="st-"], .stApp, div.stButton > button, 
    .stTextArea textarea, .stTextInput input, .stCodeBlock pre, .stMarkdown p,
    h1, h2, h3, h4, h5, h6, div, span, li, table {
        direction: rtl !important;
        font-family: 'Vazirmatn', Arial, sans-serif !important;
        text-align: right !important;
    }
    /* برای اطمینان از نمایش صحیح متن در st.code */
    .stCodeBlock pre {
        text-align: right !important;
        white-space: pre-wrap !important; /* برای شکستن خطوط طولانی در خروجی */
    }
    /* placeholder در کادرهای ورودی */
    .stTextArea textarea::placeholder,
    .stTextInput input::placeholder {
        text-align: right !important;
        opacity: 0.7; /* بهبود خوانایی placeholder */
    }
    /* دکمه‌ها ممکن است به تنظیمات خاص‌تری برای وسط‌چین کردن متن نیاز داشته باشند اگر text-align:right ظاهر خوبی ندهد */
    /* div.stButton > button { text-align: center !important; } */
</style>
""", unsafe_allow_html=True)


# --- رابط کاربری Streamlit ---
st.set_page_config(layout="wide", page_title="محاسبه‌گر اختلاف تاریخ شمسی")

st.title("محاسبه‌گر اختلاف دو تاریخ شمسی")
st.markdown("این برنامه اختلاف بین دو تاریخ شمسی را بر حسب سال و ماه برای هر خط ورودی محاسبه می‌کند.")

st.header("ورودی داده‌ها")

st.markdown("""
تاریخ‌ها را در کادر زیر وارد کنید. هر خط باید شامل دو تاریخ شمسی با فرمت `YYYY/MM/DD` باشد که با کاما (,) از هم جدا شده‌اند.
مثال:1390/05/11,1399/11/12
1384/12/12,1388/10/22
""")

input_text = st.text_area("داده‌های تاریخ را اینجا وارد یا پیست کنید:", height=150, key="date_input_area_multiline_rtl", placeholder="مثلاً: 1370/01/01,1375/02/15")

if st.button("محاسبه اختلاف", key="calculate_button_multiline_rtl"):
    if not input_text.strip():
        st.warning("لطفاً داده‌های تاریخ را وارد کنید.")
    else:
        input_lines = input_text.strip().split('\n')
        
        simplified_output_lines = [] # لیست برای خروجی ساده شده (فقط سال و ماه)
        detailed_log_lines = []      # لیست برای گزارش کامل با جزئیات خطا
        
        any_valid_line_processed = False # برای بررسی اینکه آیا حداقل یک خط معتبر پردازش شده یا خیر

        for i, line_content in enumerate(input_lines):
            original_line_for_display = line_content.strip() 
            if not original_line_for_display: # از خطوط خالی صرف نظر کن
                continue
            
            any_valid_line_processed = True
            parts = original_line_for_display.split(',')
            
            if len(parts) == 2:
                date_input1 = parts[0].strip()
                date_input2 = parts[1].strip()
                result = calculate_shamsi_date_difference(date_input1, date_input2)

                if isinstance(result, tuple):
                    years_diff, months_diff = result
                    
                    # فقط سال و ماه برای لیست ساده شده
                    clean_diff_text = f"{abs(years_diff)} سال و {abs(months_diff)} ماه"
                    simplified_output_lines.append(clean_diff_text)
                    
                    # گزارش کامل شامل جزئیات بیشتر
                    full_info_diff_text = clean_diff_text
                    if years_diff < 0 or (years_diff == 0 and months_diff < 0) :
                        full_info_diff_text += " (تاریخ دوم کوچکتر از تاریخ اول است)"
                    detailed_log_lines.append(f"خط {i+1} «{original_line_for_display}»: {full_info_diff_text}")
                else: 
                    error_msg = f"خط {i+1} «{original_line_for_display}»: {result}"
                    detailed_log_lines.append(error_msg)
            else: 
                error_msg = f"خط {i+1} «{original_line_for_display}»: خطا در فرمت خط. باید دو تاریخ جدا شده با کاما باشد."
                detailed_log_lines.append(error_msg)
        
        # نمایش نتایج ساده شده
        if simplified_output_lines:
            st.subheader("نتایج محاسبات (فقط اختلاف)")
            st.markdown("---")
            final_simplified_block = "\n".join(simplified_output_lines)
            st.code(final_simplified_block, language=None)
        elif any_valid_line_processed: # اگر خطوطی پردازش شدند اما هیچکدام موفقیت آمیز نبودند
            st.info("هیچ نتیجه موفقیت آمیزی برای نمایش در لیست خلاصه وجود ندارد. لطفاً گزارش کامل را بررسی کنید.")
        # اگر input_text.strip() خالی بود، هشدار اولیه قبلا نمایش داده شده است.

        # نمایش گزارش کامل (شامل خطاها)
        if detailed_log_lines:
            st.subheader("گزارش کامل پردازش")
            st.markdown("---")
            full_log_block = "\n".join(detailed_log_lines)
            # ارتفاع text_area را می‌توان بر اساس تعداد خطوط تنظیم کرد
            log_area_height = min(300, max(100, len(detailed_log_lines) * 23)) 
            st.text_area("جزئیات پردازش هر خط:", full_log_block, height=log_area_height, key="detailed_log_area_rtl")
        
        if not any_valid_line_processed and input_text.strip():
             st.info("ورودی داده شد اما هیچ خط معتبری برای پردازش یافت نشد (مثلاً تمام خطوط خالی بودند).")


st.markdown("---")
st.markdown("ساخته شده با پایتون و Streamlit")
