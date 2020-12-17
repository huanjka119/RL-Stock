import sqlite3      #导入sqlite3
import pandas as pd
import os
#import datain     #导入sqlite3

OUTPUT = './TBMdata'



#pd.set_option('mode.use_inf_as_na', True)
database = r"D:\Project\Database\example.db"
#conn = sqlite3.connect(database)

try:
#    conn = conn = sqlite3.connect(path+'\csv.db')
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    print('数据库连接成功！')
    print(' ')
except:
    print('数据库连接失败！')
df = pd.read_sql_query("SELECT  \
                       时间,\
                       环号,\
                       推进状态,\
                       推进速度,\
                       总推力,\
                       刀盘扭矩,\
                       刀盘转速,\
                       土压01数值,\
                       土压02数值,\
                       土压03数值,\
                       土压04数值,\
                       土压05数值,\
                       土压06数值,\
                       螺旋机转速,\
                       螺旋机扭矩,\
                       前端里程\
                       from R_quick_load """, conn)# WHERE  推进速度>0 and 刀盘转速>0
df["土压平均值"] = (df["土压01数值"]+df["土压02数值"]+df["土压03数值"]+df["土压04数值"]+df["土压05数值"]+df["土压06数值"])/6
df["上土压"] = (df["土压01数值"]+df["土压02数值"])/2

min_miles = df.groupby("环号")['前端里程'].transform('min')
df['推进距离'] = df['前端里程'] - min_miles

df2 = df.groupby("环号").mean()
list1 = df.drop_duplicates(["环号"])["环号"].sort_index().reset_index(drop=True)
for index,row in list1.iteritems():
    df_select = df[df["环号"]==row]
    df_select.to_csv(r'D:\Project\rl-stock\get_data\%d.csv' %row, index=False, encoding='utf-8_sig')
    print(row)