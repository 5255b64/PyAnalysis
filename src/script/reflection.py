import csv
from decimal import Decimal

def run(input_csv_file_addr: str, output_csv_file_addr: str):
    with open(input_csv_file_addr, 'r', encoding='utf-8') as f_in:
        with open(output_csv_file_addr, 'w', encoding='utf-8') as f_out:
            f_out_csv = csv.writer(f_out)
            f_in_csv = csv.reader(f_in)
            headers = next(f_in_csv)
            f_out_csv.writerow(["百分比数/达到该百分比所需的测试用例数"] + list(range(101)))
            for row in f_in_csv:
                if len(row) > 0 and "覆盖率" in row[0]:
                    input_line_data = row
                    output_line_data = [row[0]]
                    max_coverage = row[-1]
                    # 反射
                    percentage = [row[0]]
                    for i in range(101):
                        # 计算所需覆盖率
                        coverage = Decimal(max_coverage) * i / 100
                        percentage.append(coverage)
                    ptr_input = 1
                    ptr_percentage = 1
                    while ptr_percentage < len(percentage):
                        if ptr_input < len(input_line_data) and Decimal(input_line_data[ptr_input]) < Decimal(
                                percentage[ptr_percentage]):
                            ptr_input = ptr_input + 1
                        else:
                            ptr = ptr_input
                            if ptr >= len(input_line_data):
                                ptr = len(input_line_data) - 1
                            output_line_data.append(headers[ptr])
                            ptr_percentage = ptr_percentage + 1
                    f_out_csv.writerow(output_line_data)


if __name__ == "__main__":
    # input_csv_file_addr = "..\\..\\resource\\FxDealLogParser_1000_all.csv"
    # output_csv_file_addr = "..\\..\\resource\\FxDealLogParser_1000_all_reflection.csv"
    # run(input_csv_file_addr=input_csv_file_addr,
    #     output_csv_file_addr=output_csv_file_addr)
    #
    # input_csv_file_addr = "..\\..\\resource\\FxclDealLogParser_1000_all.csv"
    # output_csv_file_addr = "..\\..\\resource\\FxclDealLogParser_1000_all_reflection.csv"
    # run(input_csv_file_addr=input_csv_file_addr,
    #     output_csv_file_addr=output_csv_file_addr)

    input_csv_file_addr = "..\\..\\resource\\BcbipType1_1000_all.csv"
    output_csv_file_addr = "..\\..\\resource\\BcbipType1_1000_all_reflection.csv"
    run(input_csv_file_addr=input_csv_file_addr,
        output_csv_file_addr=output_csv_file_addr)

    input_csv_file_addr = "..\\..\\resource\\BcbipType2_1000_all.csv"
    output_csv_file_addr = "..\\..\\resource\\BcbipType2_1000_all_reflection.csv"
    run(input_csv_file_addr=input_csv_file_addr,
        output_csv_file_addr=output_csv_file_addr)

    input_csv_file_addr = "..\\..\\resource\\BcbipType3_1000_all.csv"
    output_csv_file_addr = "..\\..\\resource\\BcbipType3_1000_all_reflection.csv"
    run(input_csv_file_addr=input_csv_file_addr,
        output_csv_file_addr=output_csv_file_addr)

    # input_csv_file_addr = "..\\..\\resource\\BcbipType_all_1000_all.csv"
    # output_csv_file_addr = "..\\..\\resource\\BcbipType_all_1000_all_reflection.csv"
    # run(input_csv_file_addr=input_csv_file_addr,
    #     output_csv_file_addr=output_csv_file_addr)
