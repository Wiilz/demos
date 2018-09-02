class Scope:
    allow_api = []  # 允许
    allow_module = []
    forbidden = []  # 禁止

    def __add__(self, other):
        self.allow_api.extend(other.allow_api)
        self.allow_api = list(set(self.allow_api))  # 去重

        self.allow_module.extend(other.allow_module)
        self.allow_module = list(set(self.allow_module))

        self.forbidden.extend(other.forbidden)
        self.forbidden = list(set(self.forbidden))
        return self


class UserScope(Scope):
    """普通用户的权限"""
    # allow_api = ['v1.user+get_user', 'v1.user+delete_user']
    forbidden = ['v1.user+super_get_user', 'v1.user+super_delete_user']
    allow_module = ['gift']

    def __init__(self):
        self + AdminScope()  # 可以访问Admin可以访问的视图, 但是不包括forbidden的部分


class AdminScope(Scope):
    """管理员权限"""
    allow_module = ['user']


class SuperScope(Scope):
    """超级管理员的权限"""
    allow_api = []

    def __init__(self):
        self + UserScope + AdminScope


def is_in_scope(scope, endpoint):
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    module_name = red_name.split('.')[-1]
    return endpoint not in scope.forbidden and \
           (endpoint in scope.allow_api or
            module_name in scope.allow_module)
