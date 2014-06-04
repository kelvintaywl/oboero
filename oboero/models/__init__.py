#!/usr/bin/python
# -*- coding: utf-8 -*-

class JsonableMixin(object):
    def to_jsonable(self, exclude=None):
        """Returns dict for JSON API response."""
        json_keys = self.json_keys
        checkable = isinstance(json_keys, dict)
        to_expand = set(json_keys)
        if exclude is not None:
            to_expand.difference_update(exclude)

        jsonable = {k: getattr(self, k) for k in to_expand}
        try:
            for k, v in jsonable.iteritems():
                if checkable:
                    typecheck(k, json_keys[k], v)
                jsonable[k] = to_jsonable(v)
        except TypeError as e:
            logging.error("json_keys error on %s: %s", type(self), str(e))
            raise
        return jsonable
