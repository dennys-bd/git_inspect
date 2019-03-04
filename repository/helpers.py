"""
create_from_dict recieves a dictionary
and creates a model from it, ignoring
fields that are not in the model.
"""
def create_from_dict(dct, model):
    fields = set(f.name for f in model._meta.get_fields())
    dct = {k: v for k, v in dct.items() if k in fields}
    return model(**dct)
