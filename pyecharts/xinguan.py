import json
from pyecharts.charts import Line
from pyecharts.options import TitleOpts, LabelOpts, VisualMapOpts

f_us = open("美国.txt", 'r', encoding='utf-8')
us_data = f_us.read()
us_data = us_data.replace('jsonp_1629344292311_69436(', '')
us_data = us_data[:-2]
us_data = json.loads(us_data)
x_axis = us_data['data'][0]['trend']['updateDate'][:314]
us_yaxis = us_data['data'][0]['trend']['list'][0]['data'][:314]

f_jp = open("日本.txt", 'r', encoding='utf-8')
jp_data = f_jp.read()
jp_data = jp_data.replace('jsonp_1629350871167_29498(', '')
jp_data = jp_data[:-2]
jp_data = json.loads(jp_data)
jp_yaxis = jp_data['data'][0]['trend']['list'][0]['data'][:314]

f_in = open("印度.txt", 'r', encoding='utf-8')
in_data = f_in.read()
in_data = in_data.replace('jsonp_1629350745930_63180(', '')
in_data = in_data[:-2]
in_data = json.loads(in_data)
in_yaxis = in_data['data'][0]['trend']['list'][0]['data'][:314]

line = (
    Line()
    .add_xaxis(x_axis)
    .add_yaxis('美国新冠确诊人数', us_yaxis, label_opts=LabelOpts(is_show=False))
    .add_yaxis('日本新冠确诊人数', jp_yaxis, label_opts=LabelOpts(is_show=False))
    .add_yaxis('印度新冠确诊人数', in_yaxis, label_opts=LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=TitleOpts(title='全球新冠疫情确诊人数', pos_bottom='1%', pos_right='center'),
        visualmap_opts=VisualMapOpts(is_show=True, pos_right='1%', max_=19000000, min_=0),
    )
)

line.render('新冠疫情确诊人数.html')

f_us.close()
f_jp.close()
f_in.close()
