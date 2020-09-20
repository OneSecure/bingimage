[必应美图](http://weibo.com/bingphoto) 机器人
==========

开发过程的艰难困苦，记述下来。


用 [Python](https://www.python.org) 语言编写, 托管在 [GAE](https://appengine.google.com) 上面。

功能只有一个：抓取壁纸网站 [必应(Bing)](http://www.bing.com) 上的图片，并自动发送到 [微博](http://www.weibo.com) 上。



抓取网页
--------------------
这部分相对简单。取得网页纯文本，用 `正则表达式` 提取需要的信息，包括图片的说明和图片的网址。



发微博
--------------------
这部分周折很多，首先使用的 SDK 是渣浪推荐的个人代码 [微博 Python SDK](https://github.com/michaelliao/sinaweibopy) ，使用以后发现自动提取 Code 相当费劲，用了好几个第三方库，包括 [requests](https://github.com/kennethreitz/requests) 才搞定，然后就可以 登录、认证、取码、发博。一气呵成。



集成到 [GAE](https://appengine.google.com)
--------------------
这部分搞得老子差点崩溃。虽然只是很简单几句 Python 代码，数行配置语句。

开发倒是很顺利，就是测试时，每次程序都是崩溃在 `requests` 库的 [某个地方](https://github.com/kennethreitz/requests/issues/3018) 。

开始怀疑是 [微博 Python SDK](https://github.com/michaelliao/sinaweibopy) 的问题，找了一个更简洁的 [微博SDK](https://github.com/lxyu/weibo) ，当然它同样也使用了 `requests` 库。满怀希望地重试以后，在本地毫无问题，集成到 `GAE` 崩溃依旧。

于是到官方网站上提 [issue](https://github.com/kennethreitz/requests/issues/3018) ；作者很快回复，他表示他不带 `GAE` 玩。

这是老子人生中少有的绝望时刻。Google 了很久以后，终于找到了 [解决方案](http://stackoverflow.com/questions/27974128/how-do-i-resolve-django-allauth-connection-aborted-error13-permission-d) ：将 `requests` 库的版本降级到 2.3.0 版。死马当作活马医之后，怀着前途未卜的忐忑，按下了调试按钮。运行成功了！！！什么叫 `飞一般的感觉`？这他妈就是！



翻越 `GFW`，部署 `GAE`
--------------------
然后，我们走到了最后一道难关：翻越 `GFW`，部署 `GAE`，我们平时翻墙翻惯了，从来没想过翻不过去的问题，这回是结结实实地踢到铁板了。

我们平时的翻墙走的是 `http`／`https` 端口代理，其他端口根本从不关心，而 [GAE](https://appengine.google.com) 的发布客户端可能使用了其它端口，导致发布程序在运行后即假死，半个小时以后报告主人：发布失败。

其实我们有没有注意过？我们翻着墙，却从来没有 ping 通过 Google 的 IP，就是这个道理。

于是发了疯似的找 `真正` 的 `VPN`，于是找到了这个：[FlyVPN](https://www.flyvpn.com) 。 `FlyVPN` 果然不是吹牛逼，绝逼是 `飞一般的感觉`。—— 这里替 `FlyVPN` 打个小广告。—— 不过有个限制，免费用户每天只能用 3 次，每次只能用 20 分钟。不过对于我目下的场景，就是绝处逢生。于是一行命令将应用上传、部署、启动完毕。夜野耶叶✌️。



最后
--------------------
罗列出 GAE 的本机调试命令

        dev_appserver.py 应用所处文件夹/

和应用上传命令

        gcloud app deploy

终于，打完收工。



文末废话
==========
我们伟光正的政府为啥要千方百计地阻断我们与全球互联网的连接，你们在怕什么？咹？！
