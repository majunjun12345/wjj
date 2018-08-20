import requests
from pyquery import PyQuery as pq
import re

def get(u):
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

    r = requests.get(u, headers=headers)
    page = r.content
    return page


def obtain(i):
    e = pq(i)
    url = e("tr th a.s").attr("href")
    return "http://web699250.com/" + url


def main():
    url = "http://web699250.com/forum.php?mod=forumdisplay&fid=56&page=1"
    page = get(url)
    e = pq(page)
    p = e("#fd_page_top .last").text()
    match_re = r"...(?P<page_num>\d+)"
    page_num = int(re.search(match_re, p).group(1))
    while (page_num > 0):
        url = "http://web699250.com/forum.php?mod=forumdisplay&fid=56&page={}".format(page_num)
        r = get(url)
        e = pq(r)
        items = e("tbody")
        del items[0]
        item_urls = [ obtain(i) for i in items]
        for url in item_urls:
            item = get(url)
            e = pq(item)
            title = e("#thread_subject").text()
            print(title)
            front_image_url = e("#aimg_JCgWG")
            if front_image_url:
                print("ok")
        page_num = page_num - 1


if __name__ == "__main__":
    main()