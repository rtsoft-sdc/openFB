import logging


class GetInstancePathAndName:
    def __init__(self):
        self.instance_path = "openfb.default"
        self.instance_name = "FB_Instance"
    
    def schedule(self, event_name, event_value, Sep):
        if event_name == 'REQ':
            if Sep and isinstance(Sep, str):
                path = self.instance_path.replace('.', Sep)
            else:
                path = self.instance_path.replace('.', '/')
            
            return event_value, path, self.instance_name
        
        return event_value, "", ""

    def __del__(self):
        logging.info('class destroyed')
