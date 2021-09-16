from flask import render_template, request, render_template_string
from flask_login import login_required
from app.main import main

def waf(str):
    waf_list = ['__builtins__', '{{', '}}']
    for word in waf_list:
        if word in str:
            return True
    return False


@main.route('/yxh')
def yxh():
    result = '全国高校不开学了是怎么回事呢？全国高校相信大家都很熟悉，但是全国高校不开学了是怎么回事呢，下面就让小编带大家一起了解吧。\r\n' \
             '全国高校不开学了，大家可能会很惊讶全国高校怎么会不开学了呢？但事实就是这样，小编也感到非常惊讶。\r\n' \
             '这就是关于全国高校不开学了的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！'
    return render_template('main/yxh.html', txt=result)


@main.route('/result/', methods=['POST'])
@login_required
def result():
    e = request.form.get('event')
    n = request.form.get('name')
    str = '{{subject}}{{event}}是怎么回事呢？{{subject}}相信大家都很熟悉，但是{{subject}}{{event}}是怎么回事呢，下面就让小编带大家一起了解吧。\r\n' \
          '{{subject}}{{event}}，大家可能会很惊讶，{{subject}}怎么会{{event}}呢？但事实就是这样，小编也感到非常惊讶。\r\n' \
          '这就是关于{{subject}}{{event}}的事情了，大家有什么想法呢，欢迎在评论区告诉小编一起讨论哦！'
    if e and n:
        if waf(e) or waf(n):
            return error('No hacker!')
        else:
            content = render_template_string(str, subject=n, event=e)
            return render_template('main/yxh.html', txt=content)
    else:
        return error('Parameters illegal:' + request.form['event'] + ',' + request.form['name'])


# there is a SSTI vulnerability
@main.route('/error/')
def error(str):
    if waf(str):
        str = 'No hacker!'
    html = '''
    <h3> Error:</h3>
    %s
    <!-- That's close -->
    ''' % (str)
    result = render_template_string(html)

    return result
