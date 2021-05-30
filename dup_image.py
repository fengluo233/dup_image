import os
import numpy as np
import cv2
import argparse

def main():
    remove_simillar_picture_by_perception_hash()

def process_arguments():
    parser = argparse.ArgumentParser(description = '图片去重')
    
    parser.add_argument('--path',
                       action='store',
                       default='image',
                       help="请选择图片所在位置，默认为当前目录下image文件夹")
    
    parser.add_argument('--delete',
                       action = 'store_true',
                       help="带上delete参数即为直接删除，建议先大概查看")

    parser.add_argument('--accu',
                       action = 'store',
                       default=5,
                       help="指定检测的敏感度，默认为5（一般都够用）")
    
    return parser.parse_args()


def remove_simillar_picture_by_perception_hash():
    # 获取图片的位置
    path = process_arguments().path
    img_list = os.listdir(path)
    hash_dic = {}
    hash_list = []
    hash_name = []
    count_num = 0
    # 这里加载图片
    for img_name in img_list:
        # 将图片转化为黑白
        try:
            img = cv2.imread(os.path.join(path, img_name))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            count_num += 1
        except:
            continue

        # 将图片变成8*8的缩略图并且与平均值比较求和，得到哈希值
        img = cv2.resize(img,(8,8))
        avg_np = np.mean(img)
        img = np.where(img>avg_np,1,0)
        hash_dic[img_name] = img
        if len(hash_list)<1:
            hash_list.append(img)
            hash_name.append(img_name)
        else:
            for index,i in enumerate(hash_list):
                flag = True
                # 获取两张图片的哈希值差距矩阵，异或运算
                dis = np.bitwise_xor(i,img)

                # 我们暂时认为当哈希值差距有五位不同就是不同
                if np.sum(dis) < int(process_arguments().accu):
                    flag = False
                    if process_arguments().delete == True:
                        os.remove(os.path.join(path, img_name))
                    print(img_name + " is similar to " + hash_name[index])
                    break
            if flag:
                hash_list.append(img)
                hash_name.append(img_name)

if __name__ == '__main__':
    main()