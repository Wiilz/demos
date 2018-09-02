# flask-restful-api

返回信息格式: 


 ```
{
    "error_code": 999,
    "msg": "sorry, we make a mistake",
    "request": "POST /v1/client/register"
 }
```

部分error_code:
```
-1 删除成功
0 获取成功
999  未知错误
1006  客户端错误
1007  服务器错误
1000 参数错误
1001 notfound
1004 Forbidden
1005 授权失败
```
