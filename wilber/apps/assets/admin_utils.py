class field(object):
    def __init__(self, short_description, admin_order_field):
        self.short_description = short_description
        self.admin_order_field = admin_order_field

    def __call__(self, original_func):
        def wrappee(*args, **kwargs):
            return original_func(*args, **kwargs)

        wrappee.short_description = self.short_description
        wrappee.admin_order_field = self.admin_order_field
        return wrappee
