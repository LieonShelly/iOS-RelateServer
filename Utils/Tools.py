# 判断一个变量是不是数字（字符串）
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def random_str(input_str: str = "User"):
    from Utils.DateTimeTool import return_time_now
    return input_str + str(return_time_now())