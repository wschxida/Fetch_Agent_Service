#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : clean_html_attr.py
# @Author: Cedar
# @Date  : 2020/5/6
# @Desc  :


import lxml.html.clean as clean


safe_attrs = set(['src', 'alt', 'href', 'title', 'style'])  # 正文非剔除标签列表，在减少正文体积时，除此列表外其他的标签一律剔除


def clean_html_attr(input_html_str=''):
    cleaner = clean.Cleaner(safe_attrs=safe_attrs, page_structure=False)
    cleaned_html = cleaner.clean_html(input_html_str)
    cleaned_html = cleaned_html.replace('style="visibility: hidden;"', '')  # 此项会影响到正文显示，剔除
    return cleaned_html


def main():
    aa = '<div class="js-tweet-text-container"><p class="TweetTextSize  js-tweet-text tweet-text" lang="zh" data-aria-label-part="0">达赖喇嘛要<strong>中国</strong>信众唱诵度母心咒抵御新冠病毒 <a href="https://t.co/nUOzXmD90Q" rel="nofollow noopener" dir="ltr" data-expanded-url="http://dlvr.it/RP0z8G" class="twitter-timeline-link u-hidden" target="_blank" title="http://dlvr.it/RP0z8G"><span class="tco-ellipsis"/><span class="invisible">http://</span><span class="js-display-url">dlvr.it/RP0z8G</span><span class="invisible"/><span class="tco-ellipsis"><span class="invisible"> </span></span></a></p></div>'
    result = clean_html_attr(aa)
    print(aa)
    print(result)


if __name__ == '__main__':
    main()
