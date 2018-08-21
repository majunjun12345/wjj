import requests
from pyquery import PyQuery as pq
import re
import os

def get(u, filename=None, dir_name=None, static_file=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        "Cookie": "safedog-flow-item=; 8VUp_2132_saltkey=XO31hxEp; 8VUp_2132_lastvisit=1534770467; "
                  "8VUp_2132_seccode=196.c01068342bfd11e144; 8VUp_2132_sid=K9Qz0t; "
                  "8VUp_2132_ulastactivity=6ca6WfuKINfeINVYurg0YAwlAI3A6b%2BxDatiq9rtzKksSKdUzHlU; "
                  "8VUp_2132_auth=ed29Ue3kj4WwLrTs4kVAyVlX0Q3jb%2BLB4Aw%2FfpwEwyyTkgn68s0it15mwmVaJ55ZDBST9TMSPY0a6Bph34Gf1sM; "
                  "8VUp_2132_lastcheckfeed=194%7C1534774626; 8VUp_2132_checkfollow=1; "
                  "8VUp_2132_lip=119.96.206.10%2C1534773764; 8VUp_2132_lastact=1534774630%09forum.php%09forumdisplay; "
                  "8VUp_2132_st_t=194%7C1534774630%7Cc39db9016875ea110904404d193c7ef0; "
                  "8VUp_2132_forum_lastvisit=D_56_1534774630; 8VUp_2132_visitedfid=56"
    }
    if not static_file:
        r = requests.get(u, headers=headers)
        content = r.content
    else:
        content = requests.get(u).content
    if filename and dir_name:
        filename = str(filename)
        dirs = os.path.join(dir_name, filename)
        if not os.path.exists(dirs):
            os.makedirs(dirs)

        file_path = os.path.join(dirs, filename)
        if static_file:
            file_path = file_path + static_file
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(content)
        else:
            if not static_file:
                with open(file_path, "rb") as f:
                    content = f.read()
    return content


def obtain(i, selector=None, attr=None):
    e = pq(i)
    if attr:
        content = e(selector).attr(attr)
    else:
        content = e(selector).text()
    return content


def main():
    url = "http://web699250.com/forum.php?mod=forumdisplay&fid=56&page=1"
    page = get(url)
    e = pq(page)
    p = e("#fd_page_top .last").text()
    match_re = r"...(?P<page_num>\d+)"
    page_num = int(re.search(match_re, p).group(1))
    while (page_num > 0):
        url = "http://web699250.com/forum.php?mod=forumdisplay&fid=56&page={}".format(page_num)
        r = get(url, filename=page_num, dir_name="page_list")
        e = pq(r)
        items = e("tbody")
        del items[0]
        item_urls = [ "http://web699250.com/" + obtain(i, selector="tr th a.s", attr="href") for i in items]
        title_list = [obtain(i, selector=".s.xst") for i in items]
        i = 0
        while (i < len(item_urls)):
            url = item_urls[i]
            title = title_list[i]
            item = get(url, filename=title, dir_name="video_list")
            e = pq(item)
            front_image_url = e(".zoom").attr("src")
            if front_image_url:
                get(front_image_url, filename=title, dir_name="video_list", static_file=".jpg")

            video_url = e("#audio1").attr("src")
            if video_url:
                print(video_url)
                get(front_image_url, filename=title, dir_name="video_list", static_file=".m4a")

            i += 1
        page_num = page_num - 1


if __name__ == "__main__":
    main()