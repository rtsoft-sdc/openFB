class GetInstancePath:
    def __init__(self):
        self.instance_path = "openfb.default.path"
    
    def schedule(self, event_name, event_value, Sep):
        if event_name == 'REQ':
            # Формируем путь экземпляра с указанным разделителем
            if Sep and isinstance(Sep, str):
                path = self.instance_path.replace('.', Sep)
            else:
                path = self.instance_path.replace('.', '/')
            return event_value, path
        
        return event_value, ""
