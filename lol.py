import requests
import json
import os
import traceback
from tqdm import tqdm


def spider_lol():
    # 定义一个列表，用于存放英雄名称和对应的id
    hero_id = []
    skins = []
    url = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js?v=20'
    response = requests.get(url)
    text = response.text
    # 将json字符串转为列表
    hero_list = json.loads(text)['hero']
    # 遍历列表
    for hero in hero_list:
        # 定义一个字典
        hero_dict = {'name': hero['name'], 'id': hero['heroId']}
        # 将列表加入字典
        hero_id.append(hero_dict)
    # 得到每个英雄对应的id后，即可获得英雄对应皮肤的url
    # 英雄id + 001
    # 遍历列表
    for hero in hero_id:
        # 得到英雄名字
        hero_name = hero['name']
        # 得到英雄id
        hero_id = hero['id']
        # 创建文件夹
        os.mkdir('C:/Users/Administrator/Desktop/lol/' + hero_name)
        # 进入文件夹
        os.chdir('C:/Users/Administrator/Desktop/lol/' + hero_name)
        # 得到id后即可拼接存储该英雄信息的url
        hero_info_url = 'https://game.gtimg.cn/images/lol/act/img/js/hero/' + hero_id + '.js'
        # 通过访问该url获取英雄的皮肤数量
        text = requests.get(hero_info_url).text
        info_list = json.loads(text)
        # 得到皮肤名称
        skin_info_list = info_list['skins']
        skins.clear()
        for skin in skin_info_list:
            skins.append(skin['name'])
        # 获得皮肤数量
        skins_num = len(skin_info_list)
        # 获得皮肤数量后，即可拼接皮肤的url，如：安妮的皮肤url为：
        # https://game.gtimg.cn/images/lol/act/img/skin/big1000.jpg ~ https://game.gtimg.cn/images/lol/act/img/skin/big1012
        s = ''
        for i in tqdm(range(skins_num), '正在爬取' + hero_name + '的皮肤'):
            if len(str(i)) == 1:
                s = '00' + str(i)
            elif len(str(i)) == 2:
                s = '0' + str(i)
            elif len(str(i)) == 3:
                pass
            try:
                # 拼接皮肤url
                skin_url = 'https://game.gtimg.cn/images/lol/act/img/skin/big' + hero_id + '' + s + '.jpg'
                # 访问当前皮肤url
                im = requests.get(skin_url)
            except:
                # 某些英雄的炫彩皮肤没有url，所以直接终止当前url的爬取，进入下一个
                continue
            # 保存图片
            if im.status_code == 200:
                # 判断图片名称中是否带有'/'、'\'
                if '/' in skins[i] or '\\' in skins[i]:
                    skins[i] = skins[i].replace('/', '')
                    skins[i] = skins[i].replace('\\', '')
                with open(skins[i] + '.jpg', 'wb') as f:
                    f.write(im.content)


def main():
    try:
        spider_lol()
    except Exception as  e:
        # 打印异常信息
        print(e)


if __name__ == '__main__':
    main()
