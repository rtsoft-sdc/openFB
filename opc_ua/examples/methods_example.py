from opcua import ua


def hello_word(parent, *args):
    return [ua.Variant(True, ua.VariantType.Boolean)]
