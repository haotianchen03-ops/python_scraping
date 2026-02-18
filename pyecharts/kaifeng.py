# 需要引用的库
from pyecharts import options as opts
from pyecharts.charts import Map

# 设置不同的系列，和系列中区域对应的数量值
pair_data1 = [
    ['龙亭区', 100],
    ['顺河回族区', 200],
    ['鼓楼区', 300],
    ['禹王台区', 400],
    ['祥符区', 500]
]

pair_data2 = [
    ['杞县', 100],
    ['兰考县', 200],
    ['尉氏县', 300],
    ['通许县', 400]
]


def create_map():
    '''
     作用：生成地图
    '''
    (  # 大小设置
        Map()
        .add(
            series_name="开封市市区",
            data_pair=pair_data1,
            maptype="开封"
        )
        .add(
            series_name="开封市县区",
            data_pair=pair_data2,
            maptype="开封"
        )

        # 全局配置项
        .set_global_opts(
            # 设置标题
            title_opts=opts.TitleOpts(title="开封地图"),
            # 设置标准显示
            visualmap_opts=opts.VisualMapOpts(max_=500, is_piecewise=False)
        )
        # 系列配置项
        .set_series_opts(
            # 标签名称显示，默认为True
            label_opts=opts.LabelOpts(is_show=True, color="blue")
        )
        # 生成本地html文件
        .render("省份地图.html")
    )


create_map()
