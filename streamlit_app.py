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

input_text = st.text_area("داده‌های تاریخ را اینجا وارد یا پیست کنید:", height=200, key="date_input_area_multiline")

if st.button("محاسبه اختلاف", key="calculate_button_multiline"):
    if not input_text.strip():
        st.warning("لطفاً داده‌های تاریخ را وارد کنید.")
    else:
        input_lines = input_text.strip().split('\n')
        
        all_results_text_lines = [] # لیستی برای نگهداری تمام خطوط نتیجه
        
        for i, line_content in enumerate(input_lines):
            original_line_for_display = line_content.strip() 
            if not original_line_for_display: # از خطوط خالی صرف نظر کن
                continue

            parts = original_line_for_display.split(',')
            
            if len(parts) == 2:
                date_input1 = parts[0].strip()
                date_input2 = parts[1].strip()
                # فراخوانی تابع محاسبه
                result = calculate_shamsi_date_difference(date_input1, date_input2)

                if isinstance(result, tuple):
                    years_diff, months_diff = result
                    diff_text = f"{abs(years_diff)} سال و {abs(months_diff)} ماه"
                    if years_diff < 0 or (years_diff == 0 and months_diff < 0) :
                        diff_text += " (تاریخ دوم کوچکتر از تاریخ اول است)"
                    all_results_text_lines.append(f"خط {i+1} «{original_line_for_display}»: {diff_text}")
                else: # این به معنی این است که تابع محاسبه یک رشته خطا برگردانده
                    all_results_text_lines.append(f"خط {i+1} «{original_line_for_display}»: {result}")
            else: # خطا در پارس کردن خط (نبودن دو تاریخ جدا شده با کاما)
                all_results_text_lines.append(f"خط {i+1} «{original_line_for_display}»: خطا در فرمت خط. باید دو تاریخ جدا شده با کاما باشد.")
        
        if all_results_text_lines:
            st.subheader("نتایج کلی")
            st.markdown("---")
            final_output_block = "\n".join(all_results_text_lines)
            st.code(final_output_block, language=None) # نمایش به صورت یک بلوک متنی
        elif input_text.strip(): # اگر ورودی داده شده بود اما هیچ خط قابل پردازشی یافت نشد
            st.info("داده وارد شده، اما هیچ خط معتبری برای پردازش یافت نشد.")
        # اگر input_text.strip() خالی بود، هشدار اولیه قبلا نمایش داده شده است.

st.markdown("---")
st.markdown("ساخته شده با پایتون و Streamlit")
