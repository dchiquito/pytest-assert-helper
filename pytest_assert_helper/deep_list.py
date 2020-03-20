class List(list):
    def __init__(
        self,
        iterable=[],
        allow_extras=False,
        allow_extra_value=None,
        allow_extra_values=[],
        ignore_order=False,
    ):
        super().__init__(iterable)
        if allow_extras and (allow_extra_value or allow_extra_values):
            raise RuntimeError(
                "allow_extras is implicit when specifying allow_extra_value or allow_extra_values"
            )
        if allow_extra_value or allow_extra_values:
            raise RuntimeError(
                "Please use either allow_extra_value or allow_extra_values, not both"
            )
        self.allow_extras = allow_extras or allow_extra_value or allow_extra_values
        self.allow_extra_value = allow_extra_value
        self.allow_extra_values = allow_extra_values
        self.ignore_order = ignore_order

    def _is_valid_extra(self, extra):
        if self.allow_extra_value:
            return self.allow_extra_value == extra
        elif self.allow_extra_values:
            for value in self.allow_extra_values:
                if value == extra:
                    return True
            else:
                return False
        return True

    def __eq__(self, o: object):

        if self.allow_extras and len(o) < len(self):
            # there can be more o than self
            return False
        if (not self.allow_extras) and len(o) != len(self):
            # the lengths must match exactly
            return False

        if not self.ignore_order:
            if not self.allow_extras:
                # exact comparison
                for i in range(0, len(self)):
                    if self[i] != o[i]:
                        return False
                return True
            else:
                # comparison with extras allowed in the other list
                i = 0
                j = 0
                # this won't backtrack if the match doesn't work out, but whatever
                while i < len(self) and j < len(o):
                    if self[i] == o[j]:
                        # they are the same, advance to the next pair
                        i += 1
                        j += 1
                    else:
                        # o[j] is not the same
                        if not self._is_valid_extra(o[j]):
                            # o[j] isn't a valid extra, fail
                            return False
                        j += 1
                # check any values left in o
                for oj in o[j:]:
                    if not self._is_valid_extra(oj):
                        # oj isn't a valid extra, fail
                        return False
                # succeed if all values in self were paired up
                return i == len(self)
        else:
            # comparison with no order enforced
            for e in self:
                for j in range(0, len(o)):
                    if e == o[j]:
                        o = o[:j] + o[j + 1 :]
                        break
                else:
                    return False
            if not self.allow_extras:
                return len(o) == 0
            else:
                for oj in o:
                    if not self._is_valid_extra(oj):
                        # oj isn't a valid extra, fail
                        return False
                return True

    def __ne__(self, o: object):
        return super.__ne__(self, o)
