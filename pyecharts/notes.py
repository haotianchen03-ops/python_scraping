from pyecharts.charts import Line
from pyecharts.options import TitleOpts,VisualMapOpts,ToolboxOpts,LegendOpts
line = Line()

line.add_xaxis(['jason','Yoco','Enzo'])
line.add_yaxis('marks',[15,60,92])
line.set_global_opts(
    title_opts=TitleOpts(title="notes",pos_right="center",pos_bottom="1%"),
    visualmap_opts=VisualMapOpts(is_show=True,type_="red"),
    toolbox_opts=ToolboxOpts(is_show=True,orient='horizontal'),
    legend_opts=LegendOpts(is_show=True,pos_right="center"),
)
line.render('notes.html')

