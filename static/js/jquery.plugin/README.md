#jQuery cascade select——casmenu

casmenu 是基于 jQuery 的多级联动菜单插件，使用方便。


##使用方法
###载入 JavaScript 文件
```html
  <script src="../js/jquery.min.js" type="text/javascript"></script>
  <script src="../js/jquery.plugin.casmenu.js" type="text/javascript"></script>
  <script src="../js/data.js" type="text/javascript"></script>  
```

###DOM 结构
```html
<div id="yrt"></div>
```

###菜单文件格式
```javascript
var levels={
    //内容中有引号，必须使用单引号，外引号必须用双引号
    //name => value
    1:{
        退出应用: "code1003",
        登录界面:"code1004",
        跳转至个人资料界面:"code1005",
    },
    2:{
        退出应用:{
            应用1:"gameid1",
            应用2:"gameid2",
            应用3:"gameid3",
            应用4:"gameid4",
            应用5:"gameid5",            
        },
        跳转至个人资料界面:{
            主界面:"main interface",
        }
    },
    3:{
        应用1:{
            中级场:"12",
            高级场:"13",
            职业场:"14",
            比赛场:"15",
        }
    }
}
```

###调用 cxSelect
``` javascript
// selects 为数组形式，请注意顺序
$("#yrt").casmenu({
	levels:levels,
	...... //还可以设置其他配置项
});
```
