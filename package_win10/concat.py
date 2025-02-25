import pandas as pd
import natsort  # 自然排序库
def process_concat(file_path):
    # 读取拆分料表.xlsx
    df = pd.read_excel(file_path)
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


'''
代码解释：


导入必要的库：

pandas 用于数据处理

natsort 用于自然排序（确保位号按正确的顺序排序）



读取原始Excel文件：

使用 pd.read_excel() 读取原始数据



定义拆分函数 split_positions：

将每个单元格中的位号按逗号拆分成列表

复制当前行并为每个位号创建新行

返回拆分后的新数据框



应用拆分函数并保存结果：

使用 apply() 函数对每一行应用拆分

使用 concat() 合并所有拆分后的行

保存拆分后的数据到新的Excel文件



读取文本文件和拆分后的Excel文件：

使用 pd.read_table() 读取文本文件

使用 pd.read_excel() 读取拆分后的Excel文件



按自然顺序排序：

提取唯一的位号并按自然顺序排序

根据排序后的顺序重新排列数据框



提取需要合并的列：

从拆分后的数据框中提取 ‘位号’ 和 ‘型号规格’ 列



合并两个数据框：

使用 merge() 函数按 ‘位号’ 列进行左连接

左连接会保留文本文件中的所有行，并添加匹配到的 ‘型号规格’



保存最终结果：

使用 to_csv() 将合并后的结果保存为文本文件




注意事项：


确保安装了 natsort 库，可以使用 pip install natsort 安装

确保文件路径正确，特别是读取和保存文件时

如果文本文件的分隔符不是逗号，请修改 sep 参数

如果位号列中有空值或不规则格式，可能需要额外的处理
'''