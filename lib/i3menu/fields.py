from zope.schema import Choice as BaseChoice
from zope.schema import Int as BaseInt
from zope.schema import TextLine as BaseTextLine


class RequiredCondition(object):
    _required = True
    required_condition = None

    def get_required(self):
        required = self._required
        if self.required_condition and not self.context:
            raise Exception('Cannot validate unbound field')
        elif self.required_condition:
            required = required or self.required_condition(self.context)
        return required

    def set_required(self, value):
        self._required = value
    required = property(get_required, set_required)

    def __init__(self, *args, **kwargs):
        if 'required_condition' in kwargs:
            self._required = False
            self.required_condition = kwargs.pop('required_condition')
        super(RequiredCondition, self).__init__(**kwargs)


class VisibleCondition(object):
    _visible = True
    visible_condition = None

    def get_visible(self):
        visible = self._visible
        if self.visible_condition and not self.context:
            raise Exception('Cannot validate unbound field')
        elif self.visible_condition:
            visible = visible or self.visible_condition(self.context)
        return visible

    def set_visible(self, value):
        self._visible = value
    visible = property(get_visible, set_visible)

    def __init__(self, *args, **kwargs):
        if 'visible_condition' in kwargs:
            self._visible = False
            self.visible_condition = kwargs.pop('visible_condition')
        super(VisibleCondition, self).__init__(**kwargs)


class Int(RequiredCondition, VisibleCondition, BaseInt):
    pass


class Choice(RequiredCondition, VisibleCondition, BaseChoice):
    pass


class TextLine(RequiredCondition, VisibleCondition, BaseTextLine):
    pass
