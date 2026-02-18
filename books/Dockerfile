FROM python

# 可选：换国内源
# RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 工作目录
WORKDIR /app

# 先装依赖（利用缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium
RUN playwright install-deps

# 再拷贝你的 Scrapy 项目代码（包含 scrapy.cfg 与 books/ 包）
COPY . .

# 默认列出爬虫，方便检查
CMD ["scrapy","list"]
#运行scrapy list，CMD[‘python’，‘main.py’]则是python main.py，可在后面docker run中覆盖
