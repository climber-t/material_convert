# 简单方法
# 导入必要的库
# pandas库用于数据处理，通常用pd作为别名
import pandas as pd
# re库用于正则表达式操作
import re
# 导入自然排序库
import natsort   # 自然排序库

class Generate_all():
    def __init__(self):
        self.name = 'generate_all'
# *****************************位号排序功能***********************************************
    def process_txt_file(self,txt_path):
        """
        处理VB文件，生成排序后的输出文件。

        参数:
            txt_path (str): 输入文件路径
            output_file (str): 输出文件路径
        """
        try:
            # 使用pandas读取输入文件，header=None表示没有标题行
            df1 = pd.read_table(txt_path, header=None)
            # 繁琐方法
            # 反选
            df2 = df1[~df1[0].str.contains("BOARD|UNITS|ENDHE|PART|FIDUC|HEADER|XP|XJ|XS")]
            df3 = df2.to_csv("暂存文件.txt", index=False)  # 加上index=False
            df4 = pd.read_table("暂存文件.txt", sep="\s+", names=["位号", "封装", "角度", "X坐标", "Y坐标", "正反", "ab"])
            df4.drop(0, axis=0, inplace=True)
            df4.drop("ab", axis=1, inplace=True)  # 删除最后一列ab

            # 定义一个自定义排序键函数，用于生成排序依据
            def custom_sort_key(x):
                # 初始化两个空字符串，分别用于存储字母部分和数字部分
                alpha = ""
                num = ""
                # 遍历输入字符串中的每一个字符
                for char in x:
                    # 检查当前字符是否为字母
                    if char.isalpha():
                        alpha += char  # 将字母添加到alpha字符串中
                    else:
                        num += char  # 将数字字符添加到num字符串中
                # 将num字符串转换为整数，如果num为空则设为0
                num = int(num) if num else 0
                # 根据alpha字符串的首字母生成不同的排序键
                if alpha.startswith('A'):
                    return (0, alpha, num)  # 以A开头的字符串排序优先级最高
                elif alpha.startswith('B'):
                    return (1, alpha, num)  # 以B开头的字符串排序优先级次高
                elif alpha.startswith('C'):
                    return (2, alpha, num)  # 以C开头的字符串排序优先级次次高
                elif alpha.startswith('Z'):
                    return (3, alpha, num)  # 以Z开头的字符串排序优先级次次次高
                return (4, alpha, num)  # 其他情况排序优先级最低

            # 将排序键函数应用到DataFrame的'位号'列，生成新的'sort_key'列用于排序
            df4['sort_key'] = df4['位号'].apply(custom_sort_key)
            # 根据'sort_key'列对DataFrame进行排序，结果存储在df5中
            df5 = df4.sort_values(by='sort_key')
            # 删除临时生成的'sort_key'列，清理数据
            df5 = df5.drop(columns=['sort_key'])
            # 将排序后的DataFrame保存为CSV文件，不包含行索引
            df5.to_csv("排序完成.txt", index=False)
            # 打印完成消息
            print("处理完成，已保存至 '排序完成.txt'")

        except Exception as e:
            # 如果发生错误，打印错误信息
            print(f"处理过程中发生错误：{e}")
    # *****************************料表位号拆分功能***********************************************
    def process_excel(self,excel_path):
        """
        处理料表Excel文件，合并位号并拆分范围。

        Args:
            excel_path (str): 输入Excel文件的路径。
        """

        # 读取指定路径的Excel文件到DataFrame中
        df = pd.read_excel(excel_path)  # 读取Excel文件

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

    # *****************************物料结合功能***********************************************
    def process_cancat(self):
        # 读取原始Excel文件
        df = pd.read_excel('拆分料表.xlsx')
        # 定义函数：拆分'位号'列并展开行
        def split_positions(row):
            positions = str(row['位号']).split(',')  # 将位号按逗号拆分成列表
            new_rows = pd.DataFrame([row] * len(positions))  # 复制当前行
            new_rows['位号'] = positions  # 更新位号为拆分后的值
            return new_rows

        # 应用函数到每一行，拆分并展开数据
        split_df = df.apply(split_positions, axis=1).reset_index(drop=True)
        split_df = pd.concat(split_df.tolist())  # 合并拆分后的行
        # 保存拆分后的结果
        split_df.to_excel('分行后.xlsx', index=False)
        # 读取文本文件和拆分后的Excel文件
        vb_df = pd.read_table("排序完成.txt", sep=",")
        split_df = pd.read_excel("分行后.xlsx")
        # 按自然顺序排序'位号'列
        sorted_order = natsort.natsorted(split_df['位号'].unique())
        split_df = split_df[split_df['位号'].isin(sorted_order)].sort_values('位号')
        # 提取需要合并的两列
        merge_df = split_df[['位号', '型号规格']]
        # 左连接两个数据框，根据'位号'列
        result_df = vb_df.merge(merge_df, on='位号', how='left')
        # 保存最终结果为文本文件
        result_df.to_csv('./最终.txt', index=False)