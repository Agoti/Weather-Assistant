
# 天气助手

作者: Monster Kid(刘鸣霄, 2021010584)  
邮箱: mx-liu21@mails.tsinghua.edu.cn

- src: 源代码
  - Interface.py: 图形界面. **从这里运行**
  - WeatherAssistant.py: 天气助手类, 控制器
  - GetWeather.py: 从API获取天气数据
  - utils: 
    - predict_city.py: 从输入的城市名预测城市
    - SerialPages.py: 图形界面中的多页面控件
    - TimerThread.py: 定时器线程
    - get_all_cities: 获取所有城市名(程序运行时不会用到)
  - misc: 这里面的东西不重要
  - data: 城市列表文件, 设置文件, 所有城市文件
  - assets: 多语言字典
- report.pdf: 实验报告
- demo.mp4: 演示视频

备注: 程序在运行的时候可能会显示:   
libpng warning: iCCP: known incorrect sRGB profile  
忽略即可  
