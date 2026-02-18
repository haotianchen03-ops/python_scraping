from pyecharts.charts import Bar, Timeline
from pyecharts.options import LabelOpts, VisualMapOpts, TitleOpts
from pyecharts.globals import ThemeType
from pyecharts.components import Video

f = open("1960-2019全球GDP数据.csv", "r", encoding="ANSI")
data = f.readlines()
f.close()

data = data[1:]  # 将第一行去除
year_list = list()
country_list = list()
GDP_list = list()
data_dict = {}
for i in range(len(data)):
    data[i] = data[i].strip()
    data[i] = data[i].split(',')
    year_list.append(data[i][0])  # 获得年份
    country_list.append(data[i][1])  # 获得国家
    GDP_list.append(float(data[i][2]))  # 将（如5.433E+11）科学计数法变为浮点

    if year_list[i] in data_dict.keys():
        data_dict[year_list[i]].extend([[country_list[i], GDP_list[i]]])
    else:
        data_dict[year_list[i]] = []
        data_dict[year_list[i]].extend([[country_list[i], GDP_list[i]]])

year_list = sorted(data_dict.keys())  # 去重
timeline = Timeline({'theme': ThemeType.LIGHT})
for year in year_list:
    data_dict[year].sort(key=lambda x: x[1], reverse=True)
    year_data = data_dict[year][:8]  # 取前8位

    x_data = []
    y_data = []
    for country in year_data:
        x_data.append(country[0])
        y_data.append(country[1] / 100000000)
    x_data.reverse()
    y_data.reverse()
    bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis('GDP(亿)', y_data, label_opts=LabelOpts(position="right"))  # 要求高的在上面，所以添加数据的时候反转

        .reversal_axis()
        .set_global_opts(
            visualmap_opts=VisualMapOpts(
                is_show=True,
                is_piecewise=True,
                pieces=[
                    {'min': 0, 'max': 1.5, 'color': '#FFDEAD'},
                    {'min': 1.6, 'max': 2, 'color': '#EECFA1'},
                    {'min': 2.1, 'max': 3, 'color': '#CDB38B'},
                    {'min': 3, 'color': '#8B795E'},
                ]
            ),
            title_opts=TitleOpts(title=f"{year}年全球前八GDP", pos_top='3.9%', pos_right='center')
        )
    )
    timeline.add(bar, str(year))
timeline.add_schema(
     is_auto_play=True,
     play_interval=800  # 800ms播放下一个
    )
timeline.render("GDP.html")
