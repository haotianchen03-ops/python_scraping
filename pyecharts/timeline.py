from pyecharts.charts import Bar, Timeline
from pyecharts import options as opts
from pyecharts.faker import Faker
import random


def creat_bar():
    bar = (
        Bar()
        .add_xaxis(Faker.choose()[:3])
        .add_yaxis('', [50+random.randint(1, 10), 88+random.randint(1, 10), 180+random.randint(1, 10)], label_opts=opts.LabelOpts(position='right'))
        .reversal_axis()
        )
    return bar


bar1 = creat_bar()
bar2 = creat_bar()
bar3 = creat_bar()

timeline = (
    Timeline()
    .add(bar1, str(2021+random.randint(1, 5)))
    .add(bar2, str(2021+random.randint(1, 5)))
    .add(bar3, str(2021+random.randint(1, 5)))
    .add_schema(is_auto_play=True)
)
timeline.render('timeline.html')
