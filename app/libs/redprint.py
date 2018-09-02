class Redprint:
    def __init__(self, name):
        self.name = name
        self.mound = []
    
    def route(self, rule, **options):
        def deco(f):
            # 注册url, 因为没有蓝图对象, 无法完成注册, 此处只将相关参数保存起来.
            # self.add_url_rule(rule, endpoint, f, **options)
            self.mound.append((f, rule, options))
            # 返回函数
            return f
        return deco

    def register(self, bp, url_prefix=None):
        url_prefix = url_prefix or '/' + self.name
        for f, rule, options in self.mound:
            endpoint = self.name + '+' + options.pop('endpoint', f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)

