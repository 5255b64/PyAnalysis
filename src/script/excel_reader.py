# -*- coding:utf-8 -*-
import json
import sys
import xlrd

"""
从excel中读取bibip的人工测试用例数据
组成json文件
"""
# ROW_START = 7  # 从第8行开始读取数据
# ROW_END = 39  # 读取到39行为止
ROW_HEADER = 6  # 第7行保存header信息
# COL_START = 7  # 从第8列开始读取数据
# COL_END = 57  # 读取到30列为止
COL_LEVEL = 1  # 第2列保存了level信息
COL_PARAM_NAME = 2  # 第3列保存了参数名
COL_PARAM_TYPE = 4  # 第4列保存了参数类型

DEFAULT_OBJ_TYPE = 'object'  # 默认类型


def fun(input_excel_file_addr: str, input_excel_sheet_name: str, output_json_path: str, ROW_START: int, ROW_END: int,
        COL_START: int, COL_END: int):
    """

    :param input_excel_sheet_name:
    :param input_excel_file_addr:
    :param output_json_path:
    :return:
    """
    wb = xlrd.open_workbook(filename=input_excel_file_addr)  # 打开文件
    sheet = wb.sheet_by_name(input_excel_sheet_name)  # 通过名字获取表格

    # nrows = sheet.nrows  # 表格的行数
    # ncols = sheet.ncols  # 表格的列数

    # 栈结构 保存从obj到ptr的属性路径
    # 格式为[param_name, param_type, list_num](属性名，属性类型，列表中的地址)
    # 属性类型分为 'object' 'array<object>' 和其他（string）
    attr_path = list()
    obj = dict()  # 最终输出的对象
    level = 0  # 当前的level等级
    header = sheet.row_values(ROW_HEADER)

    # 定义内部方法
    def insert(attr_path: list(), obj: dict(), param_name, param_type, data):
        # 将栈的最后一个对象出栈
        # 将新对象入栈
        # 如果插入的是list 那么会默认在list中插入一个空的dict()
        # 如果需要插入的list已存在 那么会在已存在的list中插入一个空的dict()
        # 如果向list中插入新的熟悉 那么默认向list的最后一个dict()中插入
        # 需要插入的对象
        obj2insert = None
        if param_type == 'object':
            obj2insert = dict()
        elif param_type == 'array<object>':
            obj2insert = list()
            # 如果插入的是list 那么会默认在list中插入一个空的dict()
            obj2insert.append(dict())
        else:
            obj2insert = data

        # 被插入的节点
        obj_inserted = obj
        obj_inserted_type = DEFAULT_OBJ_TYPE
        obj_inserted_name = None
        for i in range(len(attr_path) - 1):
            [param_name_i, param_type_i, list_num_i] = attr_path[i]
            if obj_inserted_type == 'object':
                obj_inserted = obj_inserted[param_name_i]
            elif obj_inserted_type == 'array<object>':
                obj_inserted = obj_inserted[list_num_i]
                i = i + 1  # 跳过attr_path中的空数据
            else:
                # 有问题
                print("error", file=sys.stderr)
            obj_inserted_type = param_type_i
            obj_inserted_name = param_name_i

        # 将新对象插入obj中
        list_num = -1
        if obj_inserted_type == 'object':
            # 判断目标熟悉是否已存在
            # 若已存在 则不插入
            # print("obj_inserted ",obj_inserted)
            # print("obj2insert ", obj2insert)
            if param_name not in obj_inserted.keys():
                # 插入
                obj_inserted[param_name] = obj2insert
            # 重新获取新加入的对象
            obj2insert = obj_inserted[param_name]
        elif obj_inserted_type == 'array<object>':
            # 如果向list中插入新的属性 那么默认向list的最后一个dict()中插入
            # 判断目标属性是否已存在
            if param_name in obj_inserted[-1].keys():
                # 如果需要插入的list已存在 那么会在已存在的list中插入一个空的dict()
                obj_inserted.append(dict())
            obj_inserted[-1][param_name] = obj2insert
            # 重新获取新加入的对象
            # obj2insert = obj_inserted[-1][param_name]

            # 最后一个对象出栈
            attr_path.pop(len(attr_path) - 1)
            # list出栈
            attr_path.pop(len(attr_path) - 1)
            # list入栈
            list_num = len(obj_inserted) - 1
            attr_path.append([obj_inserted_name, obj_inserted_type, list_num])
            # 空对象入栈
            attr_path.append([])
        else:
            # 有问题
            print("error", file=sys.stderr)

        # 最后一个对象出栈
        attr_path.pop(len(attr_path) - 1)
        # 新对象入栈
        attr_path.append([param_name, param_type, list_num])

        # 如果新对象是一个list

        return attr_path, obj

    def level_up(attr_path: list()):
        # 向栈中插入一个空对象
        attr_path.append([])
        return attr_path

    def level_down(attr_path: list):
        # 最后一个对象出栈
        attr_path.pop(len(attr_path) - 1)
        return attr_path

    # 遍历执行
    for col_num in range(COL_START, COL_END):
        data_group = header[col_num]  # 数据组名
        if data_group not in obj.keys():
            obj[data_group] = dict()
        # attr_path.append([data_group, DEFAULT_OBJ_TYPE, -1])
        attr_path = [[data_group, DEFAULT_OBJ_TYPE, -1]]
        level = 0
        for row_num in range(ROW_START, ROW_END):
            # rows = sheet.row_values(row_num)  # 获取行内容
            str_level = sheet.cell_value(row_num, COL_LEVEL)  # 当前的level信息
            value_level = len(str_level)
            param_name = sheet.cell_value(row_num, COL_PARAM_NAME)  # 当前的参数名
            param_type = sheet.cell_value(row_num, COL_PARAM_TYPE)  # 当前的参数类型

            # data = sheet.cell_value(col_num, row_num)  # 获取数据
            data = sheet.cell_value(row_num, col_num)  # 获取数据

            if value_level is level + 1:
                level = value_level
                # 升级
                attr_path = level_up(attr_path=attr_path)
                attr_path, obj = insert(attr_path=attr_path, obj=obj, param_name=param_name, param_type=param_type,
                                        data=data)

            elif value_level is level - 1:
                level = value_level
                # 降级
                attr_path = level_down(attr_path=attr_path)
                attr_path, obj = insert(attr_path=attr_path, obj=obj, param_name=param_name, param_type=param_type,
                                        data=data)

            elif value_level is level:
                # 同级
                attr_path, obj = insert(attr_path=attr_path, obj=obj, param_name=param_name, param_type=param_type,
                                        data=data)
            else:
                # 有问题
                print("|value_level-level|>1 " + str(value_level), file=sys.stderr)
                print("value_level=" + str(value_level), file=sys.stderr)
                print("level=" + str(level), file=sys.stderr)
        # print(obj)
    # print(obj)
    # 输出json文件
    counter = 0
    for key in obj.keys():
        output_obj = obj[key]
        output_json_file_path = output_json_path + "\\test" + str(counter) + ".json"
        counter = counter + 1
        with open(output_json_file_path, 'w') as out_f:
            json.dump(output_obj, out_f, ensure_ascii=True)


if __name__ == "__main__":
    ROW_START = 7  # 从第8行开始读取数据
    COL_START = 7  # 从第8列开始读取数据

    # 比例
    # ROW_END = 40  # 读取到39行为止
    # COL_END = 57  # 读取到57列为止
    # input_excel_file_addr = "C:\\GX\\Study\\ECNU\\小论文\\数据\\中资外币债\\准出材料\\数据用例\\中资外币债_比例.xlsx"
    # input_excel_sheet_name = '中资外币债_比例'
    # output_json_path = "C:\\GX\\Study\\ECNU\\小论文\\程序\\PyAnalysis\\resource\\人工测试用例\\比例"

    # 地区
    # ROW_END = 35  # 读取到35行为止
    # COL_END = 92  # 读取到92列为止
    # input_excel_file_addr = "C:\\GX\\Study\\ECNU\\小论文\\数据\\中资外币债\\准出材料\\数据用例\\中资外币债_地区.xlsx"
    # input_excel_sheet_name = '中资外币债_地区'
    # output_json_path = "C:\\GX\\Study\\ECNU\\小论文\\程序\\PyAnalysis\\resource\\人工测试用例\\地区"

    # 类型
    ROW_END = 40  # 读取到40行为止
    COL_END = 117  # 读取到117列为止
    input_excel_file_addr = "C:\\GX\\Study\\ECNU\\小论文\\数据\\中资外币债\\准出材料\\数据用例\\中资外币债_类型.xlsx"
    input_excel_sheet_name = '中资外币债_类型'
    output_json_path = "C:\\GX\\Study\\ECNU\\小论文\\程序\\PyAnalysis\\resource\\人工测试用例\\类型"
    fun(input_excel_file_addr=input_excel_file_addr, input_excel_sheet_name=input_excel_sheet_name,
        output_json_path=output_json_path, ROW_START=ROW_START, ROW_END=ROW_END, COL_START=COL_START, COL_END=COL_END)
