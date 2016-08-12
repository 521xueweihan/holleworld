#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 
#   Author  :   XueWeiHan
#   E-mail  :   595666367@qq.com
#   Date    :   16/4/1 下午3:01
#   Desc    :   HTML转义


def code_unescape(s):
    """
    代码块中的内容不转义
    """
    s = s.group(0)
    # 反转义"&amp;"，使得'<','>'是html转义的符号。
    # hightligth.js有个坑，lg和lt会高亮，使得html识别不了"&lt;"和"&gt;"。
    s = s.replace("&amp;", "&")
    return s


def html_escape(s):
    """
    转义特殊符号 "&"， "<"， ">"保证HTML安全
    """
    if s:
        s = s.replace("&", "&amp;") # Must be done first!
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")
        s = s.replace("(", "&#40;")
        s = s.replace(")", "&#41;")
        return s
    else:
        return None


def remove_script(s):
    """
    移除script标签
    """
    s = s.replace("<script>", '')
    s = s.replace('</script>', '')
    return s