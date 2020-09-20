import sys
import xlrd

"""
从excel中读取bibip的人工测试用例数据
组成json文件
"""
ROW_START = 7  # 从第8行开始读取数据
ROW_END = 39  # 读取到39行为止
ROW_HEADER = 6  # 第7行保存header信息
COL_START = 7  # 从第8列开始读取数据
COL_END = 30  # 读取到30列为止
COL_LEVEL = 1  # 第2列保存了level信息
COL_PARAM_NAME = 2  # 第3列保存了参数名
COL_PARAM_TYPE = 4  # 第4列保存了参数类型

DEFAULT_OBJ_TYPE = "object"     # 默认类型


def fun(excel_file_addr: str):
    wb = xlrd.open_workbook(filename=excel_file_addr)  # 打开文件
    sheet = wb.sheet_by_name('中资外币债_比例')  # 通过名字获取表格

    nrows = sheet.nrows  # 表格的行数
    ncols = sheet.ncols  # 表格的列数

    attr_path = list()  # 保存从obj到ptr的属性路径
    obj = dict()  # 最终输出的对象
    ptr = obj  # 指针 指向当前处理的属性
    ptr_type = DEFAULT_OBJ_TYPE  # 当前处理属性的类型
    level = 0  # 当前的level等级
    header = sheet.row_values(ROW_HEADER)
    for col_num in range(COL_START, COL_END):
        data_group = header[col_num]  # 数据组名
        ptr = dict()
        obj[data_group] = ptr
        for row_num in range(ROW_START, ROW_END):
            # rows = sheet.row_values(row_num)  # 获取行内容
            str_level = sheet.cell_value(row_num, COL_LEVEL)  # 当前的level信息
            value_level = len(str_level)
            param_name = sheet.cell_value(row_num, COL_PARAM_NAME)  # 当前的参数名
            param_type = sheet.cell_value(row_num, COL_PARAM_TYPE)  # 当前的参数类型

            data = sheet.cell_value(col_num, row_num)  # 获取数据

            if value_level is level + 1:
                # 升级
                level = value_level
                obj2insert = None
                if param_type == 'object':
                    obj2insert = dict()
                elif param_type == 'array<object>':
                    obj2insert = list()
                else:
                    obj2insert = data

                list_num = -1
                if ptr_type == 'object':
                    ptr[param_name] = obj2insert
                elif ptr_type == 'array<object>':
                    list_num = len(ptr)
                    ptr.append(obj2insert)
                else:
                    # 有问题
                    print("普通类型 level up", file=sys.stderr)
                attr_path.append([param_name, param_type, list_num])
                ptr_type = param_type
                ptr = obj2insert

            elif value_level is level - 1:
                # 降级
                level = value_level
                # 找到父节点（根据attr_path的信息）
                father = obj[data_group]
                father_type = DEFAULT_OBJ_TYPE
                for i in range(len(attr_path) - 2):
                    param_name_i, param_type_i, list_num_i = attr_path[i]
                    father_type = param_type_i
                    if param_type_i == 'object':
                        father = father[param_name_i]
                    elif param_type_i == 'array<object>':
                        father = father[list_num_i]
                    else:
                        # 有问题
                        print("同级 father 为普通类型", file=sys.stderr)
                # 插入元素
                obj2insert = None
                if param_type == 'object':
                    obj2insert = dict()
                elif param_type == 'array<object>':
                    obj2insert = list()
                else:
                    obj2insert = data

                list_num = -1
                if father_type == 'object':
                    father[param_name] = obj2insert
                elif father_type == 'array<object>':
                    list_num = len(ptr)
                    father.append(obj2insert)
                else:
                    # 有问题
                    print("同级 father 为普通类型", file=sys.stderr)

                # 降级
                attr_path.pop(len(attr_path)-1)
                attr_path.pop(len(attr_path)-1)
                attr_path.append([param_name, param_type, list_num])
                ptr_type = param_type
                ptr = obj2insert

            elif value_level is level:
                # 同级
                # 找到父节点（根据attr_path的信息）
                father = obj[data_group]
                father_type = DEFAULT_OBJ_TYPE
                for i in range(len(attr_path) - 1):
                    param_name_i, param_type_i, list_num_i = attr_path[i]
                    father_type = param_type_i
                    if param_type_i == 'object':
                        father = father[param_name_i]
                    elif param_type_i == 'array<object>':
                        father = father[list_num_i]
                    else:
                        # 有问题
                        print("同级 father 为普通类型", file=sys.stderr)
                # 插入元素
                obj2insert = None
                if param_type == 'object':
                    obj2insert = dict()
                elif param_type == 'array<object>':
                    obj2insert = list()
                else:
                    obj2insert = data

                list_num = -1
                if father_type == 'object':
                    father[param_name] = obj2insert
                elif father_type == 'array<object>':
                    list_num = len(ptr)
                    father.append(obj2insert)
                else:
                    # 有问题
                    print("同级 father 为普通类型", file=sys.stderr)
                # 降级
                attr_path.pop(len(attr_path)-1)
                attr_path.append([param_name, param_type, list_num])
                ptr_type = param_type
                ptr = obj2insert
            else:
                # 有问题
                print("|value_level-level|>1" + str(value_level), file=sys.stderr)
                print("value_level=" + str(value_level), file=sys.stderr)
                print("level=" + str(level), file=sys.stderr)
        print(obj)


def demo():
    excel_file_addr = "..\\..\\resource\\excel_demo.xlsx"
    wb = xlrd.open_workbook(filename=excel_file_addr)  # 打开文件

    print(wb.sheet_names())  # 获取所有表格名字

    sheet1 = wb.sheet_by_index(0)  # 通过索引获取表格

    sheet2 = wb.sheet_by_name('年级')  # 通过名字获取表格

    print(sheet1, sheet2)

    print(sheet1.name, sheet1.nrows, sheet1.ncols)

    rows = sheet1.row_values(2)  # 获取行内容

    cols = sheet1.col_values(3)  # 获取列内容

    print(rows)

    print(cols)

    print(sheet1.cell(1, 0).value)  # 获取表格里的内容，三种方式

    print(sheet1.cell_value(1, 0))

    print(sheet1.row(1)[0].value)


if __name__ == "__main__":
    excel_file_addr = "C:\\GX\\Study\\ECNU\\小论文\\数据\\中资外币债\\准出材料\\数据用例\\中资外币债_比例.xlsx"
    fun(excel_file_addr=excel_file_addr)
    print("hello world")
