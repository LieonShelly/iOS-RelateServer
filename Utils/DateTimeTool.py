import moment
import calendar
import time

# 返回当前时间戳
def return_time_now():
    return int(time.time() * 1000)

# moment对象转时间戳
def moment_to_timestamp(moment_obj):
    timetuple = moment_obj.date.timetuple()
    return time.mktime(timetuple)*1000


def datestr_2_timestamp(date_str):
    date = moment.date(date_str, "%Y-%m-%d").date
    time_tuple = date.timetuple()
    time_stamp = int(time.mktime(time_tuple) * 1000)
    return time_stamp

#  当天的开始时间
def today_timestamp():
   today_str = moment.now().format("YYYY-M-D")
   time_stamp = datestr_2_timestamp(today_str)
   return time_stamp

# 当天的结束时间-第二天的开始时间
def today_end_timestamp():
   today_str = moment.now().format("YYYY-M-D")
   time_stamp = datestr_2_timestamp(today_str) + 24 * 60 * 60 * 1000
   return time_stamp

def current_month_timestamp():
   month_str = moment.now().format("YYYY-M")
   time_stamp = datestr_2_timestamp(month_str)
   return time_stamp

def days_of_month(month_timestamp):
   month_date = moment.unix(month_timestamp/1000).date
   monthRange = calendar.monthrange(month_date.year, month_date.month)
   return monthRange[1]

def one_moth_timestamp(timestamp):
    return 24 * 60 * 60 * 1000 * days_of_month(timestamp) + timestamp

def current_year_start_timestamp():
    month_str = moment.now().format("YYYY")
    time_stamp = datestr_2_timestamp(month_str)
    return time_stamp


def current_year_end_timestamp():
    year_date = moment.now().date
    if calendar.isleap(year_date.year):
         return current_year_start_timestamp() + 366 * 24 * 60 * 60 * 1000
    else:
         return current_year_start_timestamp() + 365 * 24 * 60 * 60 * 1000

def fall_back_one_year_timestamp():
    return return_time_now() - 366 * 24 * 60 * 60 * 1000

def date_str(time_stamp):
   moment_obj =  moment.unix(time_stamp)
   return moment_obj.format("YYYY-M-D")

def timestamp_to_datestr(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime(time_stamp / 1000)
    str_date = time.strftime(format_string, time_array)
    return str_date

# 当前月1号开始的时间戳
def current_month_start_timestamp():
   day_now = time.localtime()
   day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
   return datestr_2_timestamp(day_begin)

# 当前月最后一天结束的时间戳
def current_month_end_timestamp():
   day_now = time.localtime()
   wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
   day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
   return datestr_2_timestamp(day_end) + 24 * 60 * 60 * 1000


