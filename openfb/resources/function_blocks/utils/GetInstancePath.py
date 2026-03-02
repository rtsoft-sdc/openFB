class GetInstancePath:
    def __init__(self):
        self.instance_path = "openfb.default.path"
    
    def schedule(self, event_name, event_value, Sep):
        if event_name == 'REQ':
            if Sep and isinstance(Sep, str):
                path = self.instance_path.replace('.', Sep)
            else:
                path = self.instance_path.replace('.', '/')
            return event_value, path
        

    def __del__(self):
        print('class destroyed')
