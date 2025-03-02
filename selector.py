from ascript.android.node import Selector
def Online_text_se():
    Online_text = Selector(2).id("com.smile.gifmaker:id/live_audience_count_text").type("TextView").packageName("com.smile.gifmaker").visible(True).find()
    return Online_text
## 直播间主播用户名选择器
def zhubo_name_se():
    zhubo_name = Selector(2).id("com.smile.gifmaker:id/live_name_text").type("TextView").packageName("com.smile.gifmaker").visible(True).find()
    return zhubo_name
def Online_user_se():
    ## 在线观众选择器
    Online_user = Selector(2).type("ScrollView").packageName("com.smile.gifmaker").child().visible(True).find_all()
    return Online_user
## 用户名选择器
def user_name_se():
    user_name = Selector(2).id("com.smile.gifmaker:id/live_profile_nick_name").type("TextView").packageName("com.smile.gifmaker").visible(True).find()
    return user_name
## 关注选择器
def follow_user_se():
    follow_user = Selector(2).id("com.smile.gifmaker:id/live_profile_bottom_bar_follow_container").type("FrameLayout").packageName("com.smile.gifmaker").visible(True).find()
    return follow_user

## 新加入评论区入口
def comment_section_user_se():

    comment_section_user = Selector(2).id("com.smile.gifmaker:id/live_comment_bottom_container").type("FrameLayout").packageName("com.smile.gifmaker").clickable(True).visible(True).find()
    return comment_section_user


## 新加入入口待关注用户用户名
def follow_comment_section_username_se():
    follow_comment_section_username = Selector(2).id("com.smile.gifmaker:id/live_profile_nick_name").type("TextView").packageName("com.smile.gifmaker").visible(True).find()
    return follow_comment_section_username

## 新加入用户关注

def follow_comment_section_user_se():
    follow_comment_section_user = Selector(2).id("com.smile.gifmaker:id/live_profile_bottom_bar_follow_tv").text("关注").type("TextView").packageName("com.smile.gifmaker").visible(True).find()
    return follow_comment_section_user
