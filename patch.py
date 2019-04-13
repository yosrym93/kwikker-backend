import flask_restplus


def patch_flask_restplus_fields():
    old_init = flask_restplus.fields.Raw.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        if self.required is None:
            self.required = True

    flask_restplus.fields.Raw.__init__ = new_init
