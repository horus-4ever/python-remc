class Type:
    def __init__(self, name):
        self.name = name
        self.is_aligned = False


class Struct(Type):
    def __init__(self, name, fields, auto_align=False):
        super().__init__(name)
        self.fields = fields
        self.must_auto_align = auto_align
        self.size = None
        self.max_element_size = None

    def auto_align_fields(self):
        result = {name: value for name, value in sorted(self.fields.items(), key=lambda f: f[1].size)}
        self.fields = result

    def align(self, max_alignement=0):
        if self.must_auto_align:
            self.auto_align_fields()
        self.is_aligned = True
        last_field = None
        total_length = 0
        for name, field in self.fields.items():
            if last_field is None:
                total_length += field.length
                max_alignement = field.length if not max_alignement else max_alignement
                last_field = field
                continue
            if field.length > max_alignement:
                max_alignement = field.length
            if total_length % field.length == 0:
                required_padding = 0
            else:
                required_padding = field.length - (total_length % field.length)
            last_field.padding = required_padding
            total_length += field.length + required_padding
            last_field = field
        if total_length % max_alignement == 0:
            required_padding = 0
        else:
            required_padding = max_alignement - total_length % max_alignement
        last_field.padding = required_padding
        total_length += required_padding
        self.max_element_size = max_alignement
        self.size = total_length

    def align_to(self, max_alignement):
        self.align(max_alignement)

    @property
    def alignement(self):
        return self.max_element_size

    def recursive_align(self):
        for field in self.fields.values():
            if not field.type_ref.is_aligned:
                field.type_ref.recursive_align()
        self.align()


class BuiltinType(Type):
    def __init__(self, name, size):
        super().__init__(name)
        self.is_aligned = True
        self.size = size

    @property
    def alignement(self):
        return self.size



class NormalType:
    def __init__(self, name):
        self.name = name
        self.type_ref = None

    def get_size(self, config):
        return self.type_ref.size


class PointerType:
    def __init__(self, name, is_immut=False):
        self.name = name
        self.is_immut = is_immut
        self.type_ref = None

    def get_size(self, config):
        return config["size_t"]