class UaObserver:
    def __init__(self):
        self.class_instance = None

    def set_class_instance(self, class_instance):
        self.class_instance = class_instance

    def is_class_instance_set(self):
        return self.class_instance

    def split_node(self, n):
        node = str(n)
        node = node.split("FunctionBlocks:")[-1]
        node = node.split(":")
        return node[0] + "." + node[2]

    def datachange_notification(self, node, val, data):
        if self.is_class_instance_set():
            for _, conf in self.class_instance.items():
                if conf.fb_dictionary.get(self.split_node(node)) is None:
                    continue
                else:
                    conf.write_connection(val, self.split_node(node))