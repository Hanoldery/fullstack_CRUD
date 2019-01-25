
# To get the models I need to CRUD

def get_class_by_tablename(tablename):
  for c in Base._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
      return c


# Just in case

exec(mycode)


# To convert JS into my model

user = User(**{k:v for k, v in obj.items() if k in {'id', 'name'}})
