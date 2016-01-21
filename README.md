# python_web_ide
##说明
实现的一个简单Python Web IDE，提供了简单的Python代码编辑，代码提示等功能，后续会加入包管理等进一步功能。

* IDE主要注重前端，所以框架没有特别需求，项目中使用的是Flask，实际使用Django、WebPy都可以。
* 主要使用了ace.js和jedi. ace.js是一个支持多语言代码高亮的js库，jedi是一个提供Python静态分析和代码提示的第三方库。

##使用
直接
    git clone 

##代码执行
从IDE扩展成为一个OJ系统, 对应idev2项目

采用 Django + Mysql + Docker

Django, Mysql构建系统，用户注册后创建一个Docker容器，对应该用户

登录后启动容器，登录期间根据心跳保持容器运行

用户提交代码，创建一个 Submission记录， 提交任务到消息队列中，

从队列中取出任务，对应的容器启动判题流程，运行测试用例，输出结果

运行虚机中使用lrun来控制资源，根据传入的mem、cpu等参数限制运行时间

用户如果留在提交页面，会有轮询查询提交状态，等运行结束更新提交状态后会反映在提交界面

