from django.db import models

class IDField(models.CharField):
    def __init__(self, *args, id_gen_func=None, **kwargs):
        kwargs['max_length'] = 50
        self.id_gen_func = id_gen_func
        super().__init__(*args, **kwargs)