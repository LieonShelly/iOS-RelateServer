from flask import jsonify

base_code_messages = {
    20000: '操作成功',
    20001: '操作失败',
    40000: '服务器忙，请稍后再试',
    40001: '参数错误'
}


def success(data={}, message="操作成功", code=20000):
    back = {"code": code, "data": data, "message": message}
    return jsonify(back)


def fail(data={}, message="操作失败", code=20001):
    back = {"code": code, "data": data, "message": message}
    return jsonify(back)


def response(result: tuple):
    if result[0] is False:
        return fail(message=result[1])
    return success(data=result[1])


def id_error(message):
    fail(message='id 不正确，数据获取失败')
