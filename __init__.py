# __init__.py 为初始化加载文件
## 本脚本为快手直播间自动关注脚本 具有用户采集功能 自动关注功能
# 导入系统资源模块
from ascript.android.system import R
from ascript.android.ui import Dialog
# 导入动作模块
from ascript.android import action
# 导入节点检索模块
from ascript.android import node
# 导入图色检索模块
from ascript.android import screen
# 控件查找
from ascript.android.node import Selector
import time
from ascript.android import system
import json
import os
from ascript.android.system import Device
from ascript.android import action
from ascript.android.ui import WebWindow
from ascript.android.system import R
import re
config = None
def tunner(k,v):
    global config
    if k == 'running':
        # 解析前端传来的JSON数据
        config = json.loads(v)
        time.sleep(0.5)
    elif k == 'close_window':
        print("关闭")
        ## 关闭程序
        system.exit()
    

w =  WebWindow(R.ui("index.html"))
w.tunner(tunner) # 在这里设置消息通道
w.show()
print("脚本已执行")
while config is None:
    print("等待数据")
    time.sleep(0.1)
print(config)

## 导入控件
# new_user = Selector(3).id("com.smile.gifmaker:id/live_comment_bottom_container").type("FrameLayout").packageName("com.smile.gifmaker").find_all()
## 在线观众人数选择

from .selector import Online_text_se,Online_user_se,follow_user_se,user_name_se,zhubo_name_se,comment_section_user_se,follow_comment_section_username_se,follow_comment_section_user_se


# 创建保存已处理用户的文件路径
processed_users_file = R.sd("kuaishou_processed_users.txt")

# 读取已处理过的用户
processed_user_names = set()
try:
    with open(processed_users_file, "r", encoding='utf-8') as f:
        processed_user_names = set(line.strip() for line in f.readlines())
    print(f"已从文件加载 {len(processed_user_names)} 个处理过的用户")
except FileNotFoundError:
    print("未找到已处理用户记录文件，将创建新文件")

## 本脚本用控件编写 通用脚本


# 记录总用户数
# total_users = len(Online_user)

def get_scroll_coordinates():
    """获取基于屏幕尺寸的滑动坐标"""
    display = Device.display()
    screen_width = display.widthPixels
    screen_height = display.heightPixels
    
    # X轴位置：屏幕宽度的中间偏右位置
    x_position = int(screen_width * (1/2))
    
    # 起始点Y：屏幕底部往上 1/4 处
    start_y = int(screen_height * (10/12))
    # 终点Y：屏幕顶部往下 1/4 处
    end_y = int(screen_height * (7/12))
    print(x_position, start_y, x_position, end_y)
    
    # 返回相同的X坐标，不同的Y坐标
    return x_position, start_y, x_position, end_y

def toast(msg, dur=3000):
    Dialog.toast(msg, dur=dur, gravity=1 | 16, x=0, y=200, bg_color="#000000", color="#FFFFFF")

def process_online_users(config):
    type_value = config['type']  # 获取类型
    follow_count = config['followCount']  # 获取关注人数
    follow_delay = config['followDelay']  # 获取关注延迟
    processed_users = 0  # 初始化已处理用户计数

    toast(f"类型: {type_value}")
    toast(f"关注人数: {follow_count}")
    toast(f"关注延迟: {follow_delay}")

    # 获取主播用户名
    zhubo_name = zhubo_name_se()
    streamer_name = ""
    if zhubo_name:
        streamer_name = zhubo_name.text
        toast(f"当前直播间主播: {streamer_name}")
    else:
        toast("未能获取到主播名称")

    element_Online_text = None
    while True:
        Online_text = Online_text_se()
        toast("等待在线列表元素出现")
        if Online_text:
            toast("在线列表元素已出现")
            element_Online_text = True
        if element_Online_text:
            break
    Online_text.click()

    # 对在线的用户进行操作
    while True:
        current_users = Online_user_se()
        if not current_users:
            toast("未检测到用户列表，等待3秒后重试")
            time.sleep(3)
            continue
        
        current_page_size = len(current_users)
        toast(f"当前页面用户数量: {current_page_size}")
        
        # 处理当前页面的用户
        for i in range(current_page_size):
            user_name_preview = None
            try:
                user_name_preview = current_users[i].child(2).text
            except:
                toast("无法获取用户名预览，跳过该用户")
                continue
            
            if not user_name_preview:
                continue
            
            if "***" in user_name_preview:
                toast("主播已开启用户名隐私保护，无法获取用户列表，结束操作")
                action.Key.back()
                toast(f"处理完成，共处理 {processed_users} 个用户")
                return
            
            if user_name_preview == streamer_name:
                toast("已处理到主播名称，表示已到达列表底部")
                action.key.back()
                toast(f"处理完成，共处理 {processed_users} 个用户")
                return
            
            # 检查是否已经处理过这个用户
            if user_name_preview in processed_user_names:
                toast(f"用户 {user_name_preview} 已经处理过，跳过")
                continue
            
            toast(f"正在处理第 {processed_users + 1} 个用户")
            current_users[i].click()
            
            ## 获取用户名
            time.sleep(3)
            user_name = user_name_se()
            
            if user_name:
                user_name_text = user_name.text
                toast(f"正在操作用户: {user_name_text}")
                
                # 检查是否已经处理过这个用户
                if user_name_text in processed_user_names:
                    toast(f"用户 {user_name_text} 已经处理过，跳过")
                    action.Key.back()
                    continue
                
                if user_name_text == "不待":
                    toast("用户为自己，跳过")
                    action.Key.back()
                    continue
                
                ## 查看是否已经关注
                time.sleep(3)
                follow_user = follow_user_se()
                if follow_user:
                    if follow_user.child(1).text != "关注":
                        toast("用户已关注")
                        # 记录已关注的用户
                        with open(processed_users_file, "a", encoding='utf-8') as f:
                            f.write(f"{user_name_text}\n")
                        processed_user_names.add(user_name_text)
                        action.Key.back()
                        continue
                    else:
                        follow_user.click()
                        toast("用户已关注")
                        # 记录新关注的用户
                        with open(processed_users_file, "a", encoding='utf-8') as f:
                            f.write(f"{user_name_text}\n")
                        processed_user_names.add(user_name_text)
                        action.Key.back()

                processed_users += 1  # 增加已处理用户计数

                # 输出进度
                toast(f"已处理用户: {processed_users}/{follow_count}")

                # 检查是否达到关注数量
                if processed_users >= follow_count:
                    toast(f"已达到关注数量 {follow_count}，停止操作")
                    action.Key.back()
                    return

                # 等待关注延迟
                time.sleep(follow_delay)

        # 处理完当前页面后滑动到下一页
        toast("当前页面处理完毕，滑动到下一页")
        start_x, start_y, end_x, end_y = get_scroll_coordinates()
        action.slide(start_x, start_y, end_x, end_y, 3000)
        time.sleep(2)  # 等待页面加载

    toast(f"处理完成，共处理 {processed_users} 个用户")


## 新加入用户操作
def comment_section_user_follow_handling(config):
    """新加入用户操作"""
    type_value = config['type']  # 获取类型
    follow_count = config['followCount']  # 获取关注人数
    follow_delay = config['followDelay']  # 获取关注延迟
    processed_users = 0  # 初始化已处理用户计数

    toast(f"类型: {type_value}")
    toast(f"关注人数: {follow_count}")
    toast(f"关注延迟: {follow_delay}")

    while processed_users < follow_count:  # 循环直到达到关注数量
        element_comment_section_user = None
        while True:
            comment_section_user = comment_section_user_se()
            if comment_section_user:
                element_comment_section_user = True
                str_rect = str(comment_section_user.rect)
                # 使用正则表达式提取数字
                numbers = re.findall(r'\d+', str_rect)
                x1, y1, x2, y2 = map(int, numbers)
                # 进行计算
                click_x = (x2 - x1) / 4
                click_y = (y2 + y1) / 2

                action.click(click_x, click_y)
                toast("已点击")
            if element_comment_section_user:
                toast("已找到评论区入口")
                break

        ## 对用户进行操作
        element_follow_comment_section_user = None
        while True:
            time.sleep(1)
            follow_comment_section_user = follow_comment_section_username_se()
            if follow_comment_section_user:
                element_follow_comment_section_user = True
            if element_follow_comment_section_user:
                toast("已打开用户界面")
                break
            else:
                toast("主播设置隐私访问，请更换直播间")

        ## 判断是否已经处理过了
        time.sleep(1)
        username = follow_comment_section_user.text
        toast(f"开始处理用户 {username}")
        if username in processed_user_names:
            toast(f"用户 {username} 已经处理过了，跳过")
            action.Key.back()
        else:
            follow_comment_section_user = follow_comment_section_user_se()
            if follow_comment_section_user:
                if follow_comment_section_user.text != "关注":
                    toast("用户已关注")
                    # 记录已关注的用户
                    with open(processed_users_file, "a", encoding='utf-8') as f:
                        f.write(f"{username}\n")
                    processed_user_names.add(username)
                    action.Key.back()
                else:
                    follow_comment_section_user.parent(1).click()
                    toast("用户已关注")
                    # 记录新关注的用户
                    with open(processed_users_file, "a", encoding='utf-8') as f:
                        f.write(f"{username}\n")
                    processed_user_names.add(username)
                    action.Key.back()

        # 增加已处理用户计数
        processed_users += 1

        # 输出进度
        toast(f"已处理用户: {processed_users}/{follow_count}")

        # 等待关注延迟
        time.sleep(follow_delay)  # 使用传输的关注延迟

    toast(f"已达到关注数量 {follow_count}，停止操作")

# 在文件末尾调用这个函数
if config['type'] == "在线榜单":
    process_online_users(config)
if config['type'] == "新加入":
    comment_section_user_follow_handling(config)


