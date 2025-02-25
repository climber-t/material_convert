# 导入Pandas库，用于数据处理和分析
import pandas as pd
# 导入正则表达式库，用于字符串匹配和处理
import re


# 定义一个函数，用于处理料表Excel文件
def process_excel(input_path):
    """
    处理料表Excel文件，合并位号并拆分范围。

    Args:
        input_path (str): 输入Excel文件的路径。
    """

    # 读取指定路径的Excel文件到DataFrame中
    df = pd.read_excel(input_path)  # 读取Excel文件

    # 定义一个内部函数，用于合并"位号1"和"位号2"列
    def concat_columns(row):
        """
        合并行的"位号1"和"位号2"列。

        Args:
            row (Series): DataFrame的一行。

        Returns:
            str: 合并后的位号。
        """
        # 将"位号1"和"位号2"的值转换为字符串并拼接
        return str(row["位号1"]) + str(row["位号2"])
        # 按行应用合并函数，结果存储在新列"位号"中

    df["位号"] = df.apply(concat_columns, axis=1)
    # 将"位号"列中可能的"nan"替换为空字符串
    df["位号"] = df["位号"].str.replace("nan", "")

    # 定义一个内部函数，用于拆分范围格式的位号
    def split_range(value):
        """
        拆分范围格式的位号。

        Args:
            value (str): 位号字符串。

        Returns:
            str: 拆分后的位号，按逗号分隔。
        """
        # 如果值是字符串且包含"~"符号，表示是范围格式
        if isinstance(value, str) and '~' in value:
            result = []  # 用于存储拆分后的结果
            # 使用正则表达式匹配范围格式（如A1~A5）
            ranges = re.findall(
                r'([A-Za-z]+)(\d+)([A-Za-z]*)~([A-Za-z]+)(\d+)([A-Za-z]*)',
                value
            )
            # 遍历匹配到的范围
            for prefix1, start_num, suffix1, prefix2, end_num, suffix2 in ranges:
                # 确保范围的前缀和后缀相同
                if prefix1 == prefix2 and suffix1 == suffix2:
                    start = int(start_num)  # 提取起始数字
                    end = int(end_num)  # 提取结束数字
                    # 生成从start到end的所有数字
                    for i in range(start, end + 1):
                        # 拼接成完整的位号格式
                        result.append(prefix1 + str(i) + suffix1)
            # 将结果用逗号连接成字符串
            return ','.join(result)
            # 如果不是范围格式，直接返回原值
        return value
        # 对"位号"列应用拆分函数

    df['位号'] = df['位号'].apply(split_range)
    # 将处理后的结果保存到新的Excel文件
    df.to_excel('./拆分料表.xlsx', index=False)  # 不保存索引列

'''
代码解释：

导入库：
pandas：用于数据处理和操作。

re：用于正则表达式操作，处理字符串。


读取Excel文件：

使用 pd.read_excel() 读取原始料表数据。



合并位号：

concat_columns 函数将两列数据拼接。

使用 apply() 方法对每一行应用该函数。

替换 nan 值，确保数据干净。



保存中间结果：

将合并后的数据保存到 合并位号.xlsx。



拆分范围：

split_range 函数处理包含 ~ 的范围值。

使用正则表达式提取前缀、数字和后缀。

遍历范围内的所有数字，生成完整位号。



保存最终结果：

将处理后的数据保存到 拆分料表.xlsx。




主要功能：


合并位号：将两列数据拼接成一列。

拆分范围：将类似 AA1~AA3 的范围拆分成 AA1,AA2,AA3。


注意事项：


确保Excel文件路径正确。

如果位号格式不同，可能需要调整正则表达式。

处理大数据时，注意性能优化。

'''