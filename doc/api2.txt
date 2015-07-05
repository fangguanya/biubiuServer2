
<h1 id="0"> API 手册 </h1>

## 目录

>[1.0 用户登陆（v2）](#1.0)

>[1.1 获取区县信息](#1.1)

>[1.2 获取学校信息](#1.2)

>[2.0 资格验证](#2.0)

>[2.1 创建学团](#2.1)

>[2.2 查找学团](#2.2)

>[2.3 加入学团](#2.3)

>[2.4 创建学团](#2.4)

>[2.5 学团副团长设置（暂时不用）](#2.5)

>[2.6 获取学团信息（返回学团详细信息）](#2.6)

>[2.7 学团解散（可暂不开放）](#2.7)

>[2.8 加入学团审核（会长专用，暂不使用，加满为止）](#2.8)

>[2.9 学团信息设置](#2.9)

>[2.10 获取普通学团头像列表](#2.10)

>[2.11 获取普通学团头像列表](#2.11)

>[3.1 经济物品修改](#3.1)

>[4.1 获取排行榜](#4.1)

>[4.2 获取排行榜(v2)](#4.2)

>[5.0 获取用户信息](#5.0)

>[5.1 获取用户信息(v2)](#5.1)

>[5.2 更改用户信息(v2)](#5.2)

>[5.3 邀请人认证 ](#5.3)

>[5.4 查询邀请情况 ](#5.4)

>[附录](#0.1)

>[1 行政区划代码简介](#0.1)






>说明：

>该文档是对之前API多了大部分的整理和修改，故称为API2，即第二版API。

>但为了与现有已实现的API兼容，故老的API暂时是兼容的，待前端修改后，再进行老代码删除。

>为了区分新API，在文档中API的url中包含api2的为新API，说明中也用(v2)标识。
 
 
 
---
## **用户登陆**


<h4 id="1.0">  0. 用户登陆（v2）(目前仅在启动时调用，用来获取id和token, 登录系统仍用老的socket模式) </h4>

<pre><code>
[POST] http://ip/api2/qq/login
{
    "openid"   : "OPENID",
    "openkey"  : "OPEN_KEY",
    "name"     : "The player name(nickname)",
    "head_url" : "http://ip/the_player_head_url"
}
返回值：
{
    "result" : "success", 
    "code"   : 0,
    "id"     : 123456,
    "token"  : "ABCDEFabcdef"
}

字段说明：
"code"  : 返回码，表征操作正确与否及错误原因
"id"    : 用户ID，用户的唯一标识
"token" : 用户令牌， 标识用户登陆的有效性
</code></pre>


<h4 id="1.1">  1. 获取区县信息 </h4>

<pre><code>
[GET] http://ip/api/get/{province}/{city}/county
返回值：
{
    "result" : "success", 
    "county": [
            {
                "name": "东城区",
                "id": "110101"
            },
            {
                "name": "西城区",
                "id": "110102"
            },
            {
                "name": "崇文区",
                "id": "110103"
            }
    ]
}

字段说明：
{province}  : 行政区划代码省、直辖市字段（两位数字）
{city}      ：行政区划代码市级字段（两位数字）
"id"        : 区县ID，即区县的行政区划代码
"name"      : 区县名称
</code></pre>
>注：行政区划代码,可参见[行政区划代码简介](#0.1)

**举例说明：**
<pre><code>
获取北京市的区县级信息（北京的行政区划代码为110100）
[GET] http://ip/api/get/11/01/county

获取长沙市的区县级信息（长沙的行政区划代码为430100）
[GET] http://ip/api/get/43/01/county
</code></pre>


<h4 id="1.2">  2. 获取学校信息 </h4>

<pre><code>
[GET] http://ip/api/get/schools/{number}
返回值：
{
    "result": "success",
    "schools": [
        {
            "name": "北京八十五中",
            "id": "110101001"
        },
        {
            "name": "北京一六六中",
            "id": "110101002"
        }
    ]
}

字段说明：
{number}   : 行政区划代码
"schools"  : 学校列表
"id"       : 学校ID
"name"     : 学校名称
</code></pre>
>注：行政区划代码,可参见[行政区划代码简介](#0.1)

**举例说明：**
<pre><code>
获取北京市海淀区的区级范围的学校信息（北京市海淀区的行政区划代码为110108）
[GET] http://ip/api/get/schools/110108

获取湖南省长沙市的市级范围的学校信息（长沙的行政区划代码为430100）
[GET] http://ip/api/get/schools/4301

获取湖南省的省级范围的学校信息（湖南省的行政区划代码为430000）
[GET] http://ip/api/get/schools/43

</code></pre>






---
## **学团相关API**


<h4 id="2.0">  0. 资格验证(v1) </h4>

>该API作用是验证用户是否有创建学团资格

<pre><code>
[POST] http://ip/api/verify/license
{
    "license" : "LICENSE_CODE"
}
返回值：
{
    "result" : "success", 
    "logo_url" : "http://xxx.xxx.com/xxx/xx.jpg"
}
说明：
"result"描述操作结果，"success"表示成功，"error"表示失败。
"logo_url"表示授权对象的logo路径。
</code></pre>



<h4 id="2.1">  1. 创建学团（v2）</h4>
<pre><code>
[POST] http://ip/api2/create/guild
{
    "player" : 123456,              #必选，用户ID
    "token"  : "xxxxxxxxx",         #必选，用户令牌， 标识用户登陆的有效性
    "license": "LICENSE_CODE",      #必选，授权码
    "name" : "NAME"                 #必选，学团名称         
}
返回值：
{
    "result" : "success", 
    "code"   : 0,
    "id"     : 100，                #学团ID
    "logo_url" : "xxxx"             #学团头像路径
}
说明：
"player"为用户ID,可以登陆（login）时系统返回
</code></pre>

> 
> 

<h4 id="2.2"> 2. 查找学团（附简单信息）</h4>

>通过位置或ID等查找
>查找类型： 全部，城市，附近，指定名称，指定ID
<pre><code>
[POST] http://ip/api/search/guild
{
    
    "mode" : "all",                   #必选，选择范围"all","city", "nearby" (注:目前只支持"all")
    "range_min" : 1,                  #可选，期望获取学团信息的数量范围
    "range_max" : 20,                 #可选，期望获取学团信息的数量范围
    "sort_type" : "exp",              #可选，默认"exp", 支持类型"id"(按学团id号), "level"(按学团等级),"exp"(按学团经验), "duration_exp"(按学团近期一段时间经验)  (注：目前只支持"exp","duration_exp")
    "player" : "PLAYER_OPENID",       #可选，若设置，则返回的学团列表中若有该用户所在学团，将被标识出来

    #其它可选参数
    "city_id": "1101",                #城市ID， "mode"为"city"时的必要参数  (注：暂不支持)
    "longitude"：122.39592,           #经度， "mode"为"nearby"时的必要参数  (注：暂不支持)
    "latitude" ： 32.44345            #纬度， "mode"为"nearby"时的必要参数  (注：暂不支持) 

}


返回值：
{
    "result" : "success", 
    "guilds" : [
        {
            "guild_id" : 92,  
            "guild_name" : "xxxx",
            "head" : "xxx",                  #学团头像
            "people_number" : 12,
            "people_limits": 25,
            "if_in_guild" : "yes" ,          # 返回值"yes"或"no"，表示是否在该学团中
            "level" : 22,                    # 学团等级
        },
        {}
    ]
}
</code></pre>


<h4 id="2.3">  3. 加入学团（先不限制，学团加满为止） </h4>
<pre><code>
[POST] http://ip/api/add/guildmember
{
    "player" : "PLAYER_ID",          #必选
    "guild_id" : 92                  #学团ID
}
返回值：
{
    "result": "success"
}
</code></pre>

<h4 id="2.4"> 4. 退出学团 </h4>

<pre><code>
[POST] http://ip/api/quit/guild
{
    "player": "xxxxx"    #player的openid
}
返回值：
{
    "result" : "success"
}
</code></pre>

<h4 id="2.5"> 5. 学团副团长设置（暂时不用）</h4>
>限制： 学团有副团长人数限制



<h4 id="2.6"> 6. 获取学团信息（返回学团详细信息）</h4>
<pre><code>
[POST] http://ip/api/get/guild
{
    "mode" : "guild",        #必选， 根据什么方式获取学团信息，目前支持"guild"（根据学团ID）,"player"（根据用户openid）
    "guild_id" : 21,         #当"mode"为"guild"时为必选， 学团ID
    "player" : "xxxx"        #当"mode"为"player"时为必选，用户openid
}

返回值：
{
    "result": "success",
    "guild_info": {
        # 详细信息
        "head": "xxx",                       #学团头像URL
        "headID" : 23,                       #学团头像ID
        "level" : 10,                        #学团等级
        "createTime":"xxxx"                  #学团创建时间
        "createrID":12,                      #学团创建者ID
        "createrOpenID":"xxx",               #学团创建者OpenID
        "limit":100,                         #学团成员限制
        "number":89,                         #学团现有成员
        "province" : 8,                      #省行政区域码
        "city": 23,                          #市行政区域码
        "county" : 11,                       #县行政区域码
        "longitude" : 23.456,                #经度（浮点数）
        "latitude" : 33.456,                 #纬度（浮点数）
    
        #经济道具类信息
        "exp" : 100,                         #经验
        "gold": -200,                        #金币
        "gem": 1000,                         #宝石
        "prop": {},                          #道具
    },

    "members" : [
        {   
            "openid" : "xxxx",
            "name": "xxx",
            "head": "xxx",
            "level": 3,
            "guild_exp" : 123,
            "iscreater" : 0                #是否是团长（创建者），0:不是（普通学员）， 1:是（团长）
        },
        {}
    ]
}
</code></pre>

<h4 id="2.7"> 7. 学团解散（可暂不开放）</h4>
<pre><code>
[POST] http://ip/api/delete/guild
{
    "player": "xxxxx"   #player的openid(会长才能解散学团)
}
返回值：
{
    "result" : "success"
}
</code></pre>

<h4 id="2.8"> 8. 加入学团审核（会长专用，暂不使用，加满为止）</h4>



<h4 id="2.9">  9. 学团信息设置 </h4>
<pre><code>
[POST] http://ip/api/update/guild
{
    "player" : "PLAYER_ID",             #必选  用户openid(会长才有修改权限)
    "guild_id" : 92 ,                   #必选, 学团ID
    
    #以下是学团可设置的参数，均为可选，使用时可以为一个或多个
    "headID" : 23,                      #学团头像ID  
    "province" : 8,                     #省行政区域码
    "city": 23,                         #市行政区域码
    "county" : 11,                      #县行政区域码
    "longitude" : 23.456,               #经度（浮点数）
    "latitude" : 33.456,                #纬度（浮点数）
    "address" : "xxxxxx"                #学团地理位置（例如：北京市海淀区中关村1号）
    

}
返回值：
{
    "result": "success"
}
</code></pre>

<h4 id="2.10"> 10. 获取普通学团头像列表(v2) </h4>
<pre><code>
[GET] http://ip/api2/guild/heads
返回值：
{
    "result": "success",
    "code"   : 0,
    "heads" : [
        {
            "head": "xxx",                      #学团头像URL
            "id" : 1                            #学团头像ID 
        },
        ...
        {
            "head": "xxx",
            "id" : 10
        }
    ]

}
</code></pre>

<h4 id="2.11"> 11. 从学团中移除某个学员[未完成] </h4>
<pre><code>
[POST] http://ip/api2/guild/remove/member
返回值：
{
    "player" : 012345,                  #必选，会长ID(会长才有修改权限)
    "guild_id" : 92 ,                   #必选, 学团ID
    "member" : 123456                   #必须，学员ID
}
返回值：
{
    "result": "success",
    "code"   : 0
}
</code></pre>


---
## **经济相关API**

<h4 id="3.1"> 1. 经济物品修改API </h4>
<pre><code>
[POST] http://ip/api/update/props
{
    "who" : "player",                   #必选， 需要修改的对象，"player","guild"
    "openid" : "xxx",                   #"who" 为 "player"时为必选，用户的openid
    "guildid" : 23,                     #"who" 为 "guild"时为必选，guild的id

    #经济道具类参数
    "exp" : 100,                        #可选， "who" 为 "player"时有效，经验增加，例如，经验增加100
    "gold": -200,                       #可选， 金币的变化，例如，金币减少200
    "gem": 1000,                        #可选， 宝石的变化，例如，宝石增加1000,普通学员暂不支持宝石
    "prop": {
            "bomb" : 20,                #可选， 道具炸弹的变化
            "glass": 30,                #可选， 道具放大镜的变化
            "delay": 10,                #可选， 道具延时的变化
            "point": 100                #可选， 道具提示的变化
    }                                   #可选， 道具的变化    
}
注意：
1. 对于经验的增加，学团目前不支持经验增加的方法，学团的经验是随学团成员的经验增加而增加
2. exp表示经验值，理论上只能增加
</code></pre>


---
## **排行榜API**

<h4 id="4.1"> 1. 获取排行榜 </h4>
<pre><code>
[GET] http://ip/api/ranklist/{openid}/{index}

字段说明：
openid：用户的openid
index: 赛事ID

返回值：
{
    "result": "success",                    #操作是否成功，"success" or "error"
    "index": 99999,                         #赛事索引

    "first":[                               #前三名信息
        {
            "name":"xxx",                   #player名称
            "head":"xxx",                   #player头像路径
            "guild_id": 20,                 #player所属学团，0表示没有学团
            "guild_name": "xxx",            #学团名称
            "guild_head": "xxx",            #学团头像路径
            "ranking":1,                    #排名
            "count": 23,                    #积分（名牌数）
            "isplayer":0                    #是否是当前调用者
        },{}   
    ],

    "ranklist": [                           #排行榜信息，返回调用者周围11人信息
        {
            "name":"xxx",
            "head":"xxx",
            "guild_id": 20,
            "guild_name": "xxx",
            "guild_head": "xxx",
            "ranking":1,
            "count":22,
            "isplayer":0 
        },{}
    ]

}
</code></pre>


<h4 id="4.2"> 2. 获取排行榜(v2) </h4>
<pre><code>
[GET] http://ip/api2/ranklist/{openid}/{index}/{range_min}/{range_max}

字段说明：
openid：用户的openid
index: 赛事ID
range_min : 自定义排行范围查询，下限范围
range_max : 自定义排行范围查询，上限范围

返回值：
{
    "result": "success",                    #操作是否成功，"success" or "error"
    "index": 99999,                         #赛事索引

    "first":[                               #前三名信息
        {
            "name":"xxx",                   #player名称
            "head":"xxx",                   #player头像路径
            "guild_id": 20,                 #player所属学团，0表示没有学团
            "guild_name": "xxx",            #学团名称
            "guild_head": "xxx",            #学团头像路径
            "ranking":1,                    #排名
            "count": 23,                    #积分（名牌数）
            "isplayer":0                    #是否是当前调用者
        },{}   
    ],

    "ranklist": [                           #排行榜信息，返回调用者周围11人信息
        {
            "name":"xxx",
            "head":"xxx",
            "guild_id": 20,
            "guild_name": "xxx",
            "guild_head": "xxx",
            "ranking":1,
            "count":22,
            "isplayer":0 
        },{}
    ],
    

    "search_range": [                        #自定义排行范围查询信息，返回调用者设定范围的用户排行信息
        {
            "name":"xxx",
            "head":"xxx",
            "guild_id": 20,
            "guild_name": "xxx",
            "guild_head": "xxx",
            "ranking":1,
            "count":22,
            "isplayer":0 
        },{}
    ]



}
</code></pre>



---
## **用户信息API**

<h4 id="5.0"> 0. 获取用户信息 </h4>
<pre><code>
[GET] http://ip/api/info/player/{openid} 

字段说明：
openid：用户的openid

返回值：
{
    "result" : "success",
    "player": {
        "name":"xxx",                   #player名称
        "head":"xxx",                   #player头像路径
        "guildID": 20,                  #player所属学团，0表示没有学团
 

        "gold": 94,                     #金币数
        "level": 0,                     #等级

        "exp": 358,                     #经验
        "prop": {                       #道具信息
            "delay": 0,                 #延时道具数量
            "glass": 0,                 #放大镜数量
            "bomb": 0,                  #炸弹数量
            "point": 0                  #提示道具数量
        },
        "id": 158,                      #用户ID(BiuBiu ID)
        "gem": 0,                       #宝石数量
        "inviter": 121003,              #邀请人ID
        "modify_cnt": 2345              #用户信息修改次数
    }   
}
</code></pre>

<h4 id="5.1"> 1. 获取用户信息(v2) </h4>
<pre><code>
[GET] http://ip/api2/info/player/{id} 

字段说明：
id：用户的id(登陆时返回id值)

返回值：
{
    "result" : "success",
    "code"   : 0,
    "player": {
        "name":"xxx",                   #player名称
        "head":"xxx",                   #player头像路径
        "guildID": 20,                  #player所属学团，0表示没有学团
 

        "gold": 94,                     #金币数
        "level": 0,                     #等级

        "exp": 358,                     #经验
        "prop": {                       #道具信息
            "delay": 0,                 #延时道具数量
            "glass": 0,                 #放大镜数量
            "bomb": 0,                  #炸弹数量
            "point": 0                  #提示道具数量
        },
        "id": 158,                      #用户ID(BiuBiu ID)
        "gem": 0,                       #宝石数量
        "inviter": 121003               #邀请人ID
    }   
}
</code></pre>

<h4 id="5.2"> 2. 更改用户信息(v2) </h4>
<pre><code>
[POST] http://ip/api2/update/player
{
    "id": 123456,                     #用户的ID
    "token" : "xxxxx",
    
    # 基本信息
    "name":"xxx",                     #player名称
    "head":"xxx",                     #player头像路径
    
    # 位置信息

}
返回值：
{
    "result":"success"
}
</code></pre>

<h4 id="5.3"> 3. 邀请人认证 </h4>
>说明：用户使用其他用户分享的邀请码（即其他用户的ID），可以获得一次经济奖励。
>在player表中增加字段"inviter"，用来表示该用户的邀请人（该字段用ID表示）
<pre><code>
[POST] http://ip/api/add/inviter
{
    "inviter": 123456,                 #邀请人的ID
    "player" : "xxx",                  #被邀请人的openid
}
返回值：
{
    "result":"success"
}
</code></pre>

<h4 id="5.4"> 4. 查询邀请情况 </h4>
>说明：该API用来获取用户本人已邀请的用户数量
<pre><code>
[GET] http://ip/api/number/inviter/{playerid}
说明：playerid为用户的biubiu ID，非openid
返回值：
{
    "result":"success",
    "number":20
}
</code></pre>







---
## **附录**

<h4 id="0.1"> 1.行政区划代码简介 </h4>

>行政区划代码，也称行政代码，它是国家行政机关的识别符号，一般由6位阿拉伯数字组成，相当于机关单位的身份号码。
>中华人民共和国县及县以上行政区划代码，由中华人民共和国国家质量监督检验检疫总局和中国国家标准化管理委员会发布。

**代码含义**

>代码从左至右的含义是：
>第一、二位表示省（自治区、直辖市、特别行政区）。
>第三、四位表示市（地区、自治州、盟及国家直辖市所属市辖区和县的汇总码）。其中，01-20，51-70表示省直辖市；21-50表示地区（自治州、盟）。
>第五、六位表示县（市辖区、县级市、旗）。01-18表示市辖区或地区（自治州、盟）辖县级市；21-80表示县（旗）；81-99表示省直辖县级市。

**例如**
<pre><code>
110000  　　  北京市
110100  　　  市辖区
110101  　　　东城区
110102  　　　西城区
110105  　　　朝阳区
110106  　　　丰台区
</code></pre>
>注：详细代码参见[官方统计数据](http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/)
