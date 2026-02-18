from pyecharts.charts import Map
from pyecharts.options import TitleOpts, VisualMapOpts

data = [
    ['上海市', 99],
    ['广东省', 166],
    ['河南省', 2000]
]

c = (
    Map()
    .add('中国地图', data, 'china')
    .set_global_opts(
        title_opts=TitleOpts(title="CNMap"),
        visualmap_opts=VisualMapOpts(
            is_show=True,
            is_piecewise=True,
            pieces=[
                    {'min': 1, 'max': 99}, {'min': 100, 'max': 1000}, {'min': 1001, 'max': 2000}])
    )
    .render('CNmap.html')
)
