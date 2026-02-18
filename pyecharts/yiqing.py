import json
from pyecharts.charts import Map
from pyecharts.options import VisualMapOpts

f = open('疫情.txt', 'r', encoding='utf-8')
data = f.read()
f.close()

data = json.loads(data)
data = data['areaTree'][0]['children']

province_list = list()
for i in data: #列表的遍历
    province_name = i['name'] #列表里的元素为字典
    total_num = i['total']['confirm']
    if len(province_name) == 2:
        province_list.extend([[province_name + "省", total_num]])
    else:
        province_list.extend([[province_name, total_num]])
# province_list.sort(key = lambda x: x[1], reverse = True)
# province_list = sorted(province_list, key=lambda x: x[1], reverse=True)
print(province_list)

c = (
    Map()
    .add("全国疫情", province_list,"china")
    .set_global_opts(
        visualmap_opts=VisualMapOpts(
            is_show=True,
            is_piecewise=True,
            pieces=[
                {"min": 1, "max": 99, "label": "1-99人", "color": "#F0FFF0"},
                {"min": 100, "max": 4999, "label": "100-4999人", "color": "#FFDEAD"},
                {"min": 5000, "max": 9999, "label": "5000-9999人", "color": "#CDAA7D"},
                {"min": 10000, "label": "10000+人", "color": "#B22222"},
            ]
        )
    )
    .render("全国疫情.html")
)

