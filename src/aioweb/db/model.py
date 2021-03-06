class ModelMeta(type):
    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        default_views = {
            'all': {
                "map": """
                function(doc){
                if(doc.doc_type == "%s")
                emit(doc._id, doc);
            }
                """ % name
            }
        }
        attrs['default_views'] = default_views
        model_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY[name] = {'class': model_cls, 'synced': False}
        return model_cls

    def get_model_by_name(cls, name):
        return cls.REGISTRY[name]



class Model(metaclass=ModelMeta):
    views = {}
    _fields = []
    _couchdb_fields = ['_id', '_rev']

    def __init__(self, **kwargs):
        super(Model, self).__init__()
        data = {}
        for field in self.fields:
            data[field] = kwargs.get(field)
        for field in self.required_fields:
            assert field in kwargs, "Required field missing: %s" % field
        data['doc_type'] = self.__class__.__name__
        super(Model, self).__setattr__('data', data)

    def save(self, db):
        r = yield from db.put(self.data)
        if 'id' in r.__dict__ and not self._id:
            self._id = r.id
        return r

    @classmethod
    def all(cls, db):
        return cls.view('all', db)

    @classmethod
    def view(cls, view, db, **kwargs):
        view_name = cls.__name__.lower()
        n = yield from db.view(view_name, view, **kwargs)
        return n

    @property
    def fields(self):
        return self.required_fields + self._fields + self._couchdb_fields

    def get_data(self):
        return self.data

    def __setattr__(self, name, value):
        if name in self.required_fields or name in self.fields \
           or name in self._couchdb_fields:
            self.data[name] = value
        else:
            raise AttributeError('Trying to set unknown field: %s' % name)

    def __getattr__(self, name):
        if name in self.required_fields or name in self.fields:
            return self.data[name]
        return getattr(super(Model, self), name)

    def __getitem__(self, name, default=None):
        return getattr(self, name, default)

    def __setitem__(self, name, value):
        setattr(self, name, value)

    @classmethod
    def get(cls, _id, db):
        r = yield from db.get(_id)
        return r

    def update(self, value):
        self.data.update(value)

    def __str__(self):
        return "<%s>%s" % (self.__class__.__name__, self.data)
