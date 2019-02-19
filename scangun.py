import serial
import pandas as pd
import numpy as np
import time
from prettytable import PrettyTable
#
def initassetlib():
        dir = 'ju_assets.csv'
        # dir = 'qu_assets.csv'
        df = pd.read_csv(dir)
        return df.fillna('无')
#
def getasset(df_ass, id):
        return df_ass[df_ass['卡片编号'].str.contains(id)]
#
def assetlog(msg):
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        f = open('asset.log', 'a')
        f.write(str(now) + ',------,' + msg)
        f.close()
#
def ls2strls(ls):
        return [str(i) for i in ls]
#
def showasset(ass_d):
        if ass_d.empty == False:
                x = PrettyTable(['卡片编号', '资产名称', '存放地点', '使用人','备注'])
                np_ass = np.array(ass_d[['卡片编号', '资产名称', '存放地点', '使用人', '备注']])#.tolist()
                for i in np_ass:
                        x.add_row(i)
                        assetlog('P,' + ','.join(ls2strls(i)) + '\n')
                print(x)
        else:
                assetlog('F,' + ass_id + ',该编号无对应资产。\n')
                print('编号{}无对应资产。'.format(ass_id))

#
#
print('------------------------------------------------------------\n'+
      '----------------欢迎来到固定资产镭射管理中心----------------\n'+
      '-------------------------(^_^)------------------------------\n'+
      '------------------------------------------------------------')
#
flag = 0
ass_id = ''
#
df_ass = initassetlib()
ser = serial.Serial(port='COM1', baudrate=9600)
while 1 > 0:
        flag += 1
        print("\n将进行第{}次资产扫描......".format(flag))
        #
        ass_id = bytes.decode(ser.readline())
        ass_id = ass_id.replace('\r\n', '').replace(' ', '')
        ass_id = ass_id[3:]#舍弃前几位
        #
        ass_d = getasset(df_ass, ass_id)
        showasset(ass_d)
