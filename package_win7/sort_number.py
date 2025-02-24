# 简单方法
# 导入必要的库
# pandas库用于数据处理，通常用pd作为别名
import pandas as pd
# re库用于正则表达式操作
import re
# 定义一个函数，用于处理VB文件
def process_txt_file(input_file):
    """
    处理VB文件，生成排序后的输出文件。

    参数:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    try:
        # 使用pandas读取输入文件，header=None表示没有标题行
        df1 = pd.read_table(input_file, header=None)
        # 繁琐方法
        # 反选
        df2 = df1[~df1[0].str.contains("BOARD|UNITS|ENDHE|PART|FIDUC|HEADER|XP|XJ|XS")]
        df3 = df2.to_csv("vb2_1.txt", index=False)  # 加上index=False
        df4 = pd.read_table("vb2_1.txt", sep="\s+", names=["位号", "封装", "角度", "X坐标", "Y坐标", "正反", "ab"])
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

'''
代码解释


导入必要的库
import pandas as pd
import re


pandas 是用于数据处理和分析的库，pd 是其常用别名。

re 是正则表达式模块，用于字符串操作。



定义自定义排序键函数 custom_sort_key(x)
def custom_sort_key(x):
    # 使用正则表达式提取字母和数字部分
    alpha = re.sub(r'\d', '', x)  # 保留字母部分，去除数字
    num = re.sub(r'\D', '', x)    # 保留数字部分，去除字母
    num = int(num) if num else 0   # 将数字部分转换为整数，如果为空则设为0
    
    # 定义首字母优先级映射
    priority = {'A': 0, 'B': 1, 'C': 2, 'Z': 3}  # 映射首字母到优先级
    # 获取首字母的优先级，如果不存在则设为4
    prefix_priority = priority.get(alpha[0] if alpha else '', 4)  # 根据首字母获取优先级
    
    return (prefix_priority, alpha, num)  # 返回排序键元组


提取字母和数字部分：使用正则表达式 re.sub 分离字符串中的字母和数字。re.sub(r'\d', '', x) 将数字替换为空字符串，得到字母部分；re.sub(r'\D', '', x) 将非数字字符替换为空字符串，得到数字部分。

处理数字部分：将提取的数字字符串转换为整数，如果数字部分为空，则设为0。

定义优先级映射：使用字典 priority 映射首字母到优先级。例如，‘A’ 映射到0，‘B’ 映射到1，依此类推。

获取优先级：通过 priority.get 方法获取首字母的优先级，如果首字母不在映射中，则默认优先级为4。

返回排序键：返回一个元组 (prefix_priority, alpha, num)，用于后续的排序。



排序 DataFrame
df5 = df4.sort_values(by='位号', key=lambda x: custom_sort_key(x))  # 使用自定义排序键进行排序


使用 sort_values 方法对 DataFrame df4 进行排序。

by='位号' 指定排序的列。

key=lambda x: custom_sort_key(x) 使用自定义的排序键函数 custom_sort_key 生成排序依据。

排序后的结果存储在 df5 中。



保存排序后的 DataFrame
df5.to_csv("vb_fina1.txt", index=False)  # 保存结果，不包含索引


使用 to_csv 方法将排序后的 DataFrame df5 保存为 CSV 文件。

index=False 表示在保存时不包含行索引。




优化说明


使用正则表达式简化字符分离

原始代码通过遍历每个字符来分离字母和数字，优化后使用正则表达式 re.sub 一次性提取，代码更简洁，效率更高。



使用字典映射优先级

原始代码通过多个条件判断来确定优先级，优化后使用字典 priority 映射首字母到优先级，代码更简洁，也更容易扩展。



直接使用自定义排序键

原始代码生成临时的 ‘sort_key’ 列，优化后直接在 sort_values 中使用 key 参数，避免了生成和删除临时列的步骤，代码更简洁。



精简注释

优化后的注释更加简洁明了，每行代码都有清晰的解释，适合初学者理解和学习。
'''