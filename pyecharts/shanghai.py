from pyecharts.charts import Map
import json

f = open('疫情.txt','r',encoding='utf-8')
data = f.read()
f.close()

data = json.loads(data)
data = data['areaTree'][0]['children'][4]['children']
data_pair = list()
for item in data:
    district_name = item['name']
    total_num = item['total']['confirm']
    data_pair.extend([[district_name + "区",total_num]])
    
c = (
    Map()
    .add("上海疫情", data_pair,'上海')
    .render("上海.html")
)