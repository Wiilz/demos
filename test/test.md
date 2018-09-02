#### 一. 方便但不完美的\__dict__
对象对字典用到的方法为\__dict__.  比如对象对象a的属性`a.name='wk', a.age=18`, 那么如果直接将使用a.\__dict__获得对应的字典的值为: `{name: 'wk', aget:18}`, 很方便, 但是也存在一些限制. 其不完美之处在于: 

比如: 

```python
class A(object):
    name = 'wukt'
    age = 18

    def __init__(self):
        self.gender = 'male'
a = A()
print(a.__dict__)
```
此时的打印结果是: 
{gender: 'male'}
但是不会name和age一同转换. 


#### 二. 使用dict


```python
a = A()
dict(a)
```
1. 使用dict之时, 将自动调用类中的keys方法, keys中定义了字典的键, 调用keys方法后, 程序将依照字典取值的方式尝试获得这些键对应的值. 
2. 当对对象使用形如字典的取值方式时: 比如`a['name']`, 将会调用类中的\__getitem__方法, \__getitem__方法决定了这个值是多少. 

因此只需要在一例中添加两个方法就可以使对象可以通过dict转字典

```python
def keys(self):
    return ('name', 'age' )

def __getitem__(self, item):
    return getattr(self, item)

```

完整代码: 

```python
class A(object):
    name = 'wukt'
    age = 18

    def __init__(self):
        self.gender = 'male'

    def keys(self):
        '''当对实例化对象使用dict(obj)的时候, 会调用这个方法,这里定义了字典的键, 其对应的值将以obj['name']的形式取,
        但是对象是不可以以这种方式取值的, 为了支持这种取值, 可以为类增加一个方法'''
        return ('name', 'age', 'gender')
    
    def __getitem__(self, item):
        '''内置方法, 当使用obj['name']的形式的时候, 将调用这个方法, 这里返回的结果就是值'''
        return getattr(self, item)

a = A()
r = dict(a)
print(r)

```


