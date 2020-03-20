class Dict(dict):
    def __init__(self, source={}, allow_extra=False):
        super().__init__(source)
        self.allow_extra = allow_extra

    def __eq__(self, o: object):

        more = False
        more_value = None
        for flag in self.flags:
            if isinstance(flag, More):
                more = True
                more_value = self.flags[flag]

        if (not more) and len(self) != len(o):
            return False

        for key in self:
            if not key in o:
                return False
            if self[key] != o[key]:
                return False

        if more:
            for key in o:
                if not key in self:
                    if more_value != o[key]:
                        return False
        return True

    def __ne__(self, o: object):
        return super.__ne__(self, o)
