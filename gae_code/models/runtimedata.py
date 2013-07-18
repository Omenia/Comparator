class Filter(object):
    def __init__(self, name, selected, selected_value, options):
        self.name = name
        self.selected = selected
        self.selected_value = selected_value
        self.options = options


class Opt(object):
    def __init__(self, value, name):
        self.value = value
        self.name = name
