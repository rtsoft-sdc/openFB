import argparse
import xml.etree.ElementTree as ET  # 1.1.2, 1.1.7
import pathlib
import os

class FBDataModel:
    def __init__(self, name, comment=""):
        self.name = name
        self.comment = comment
        self.event_inputs = []
        self.event_outputs = []
        self.input_vars = []
        self.output_vars = []

def parse_fbt_xml(xml_content_or_path):
    # Check if input is file path or direct string
    if os.path.exists(xml_content_or_path):
        tree = ET.parse(xml_content_or_path) 
        root = tree.getroot() 
    else:
        root = ET.fromstring(xml_content_or_path) 

    fb_name = root.attrib.get('Name', 'UnnamedFB')
    fb_comment = root.attrib.get('Comment', '')
    
    fb_model = FBDataModel(fb_name, fb_comment)
    
    # Locate InterfaceList block
    interface = root.find('InterfaceList') 
    if interface is None:
        return fb_model

    # Locate and parse Event Inputs
    event_in = interface.find('EventInputs')
    if event_in is not None:
        fb_model.event_inputs = [ev.attrib.get('Name') for ev in event_in.findall('Event')]

    # Locate and parse Event Outputs
    event_out = interface.find('EventOutputs')
    if event_out is not None:
        fb_model.event_outputs = [ev.attrib.get('Name') for ev in event_out.findall('Event')]

    # Locate and parse Input Variables
    input_vars = interface.find('InputVars')
    if input_vars is not None:
        fb_model.input_vars = [
            {"name": var.attrib.get('Name'), "type": var.attrib.get('Type')}
            for var in input_vars.findall('VarDeclaration')
        ]

    # Locate and parse Output Variables
    output_vars = interface.find('OutputVars')
    if output_vars is not None:
        fb_model.output_vars = [
            {"name": var.attrib.get('Name'), "type": var.attrib.get('Type')}
            for var in output_vars.findall('VarDeclaration')
        ]

    return fb_model

def generate_python_class(fb_model):
    """Generates an openFb Python class string from parsed data model."""
    class_src = f'import logging\n\n'
    class_src += f'class {fb_model.name}:\n'
    class_src += f'    """ {fb_model.comment} """\n\n'
    
    # Generate __init__ constructor
    class_src += '    def __init__(self):\n'
    class_src += '        # Input Variables\n'
    for var in fb_model.input_vars:
        default_val = "False" if var['type'] == "BOOL" else "0"
        if var['type'] == "STRING":
           default_val = "''"          
        class_src += f"        self.{var['name']} = {default_val}  # Type: {var['type']}\n"

        
    class_src += '\n        # Output Variables\n'
    for var in fb_model.output_vars:
        default_val = "False" if var['type'] == "BOOL" else "0"
        class_src += f"        self.{var['name']} = {default_val}  # Type: {var['type']}\n"

    class_src += '\n    def __del__(self):\n'
    class_src += '        # TODO Insert your code here \n'
    class_src += '        pass \n'

        
    # Generate Input Event Triggers
    for event in fb_model.event_inputs:
        class_src += f'\n    def service_{event}(self):\n'
        class_src += f'        """ Event Handler for {event} """\n'
        class_src += f'        logging.info("Execution logic for {event} triggered")\n'
        class_src += f'        # Implement internal algorithms here\n'
        
            
    # Generate schedule function
    class_src += f'\n    def schedule(self,'
#    for event in fb_model.event_inputs:
    class_src += f'IN_EVENT_NAME,'    
    class_src += f'EVNT_CNTR,'

    for var in fb_model.input_vars:
        class_src += f"{var['name']},"
         
    idx = len(class_src)-1    
    class_src = class_src[:idx] + class_src[idx+1:]    
    class_src += f'): \n'    

    for var in fb_model.input_vars:
        class_src += f"\n        self.{var['name']}= {var['name']}"

    class_src += '\n' * 2    

    # Generate Input Event Triggers
    for event in fb_model.event_inputs:
        class_src += f'\n        if IN_EVENT_NAME == \"{event}\":'
        class_src += f'\n            # TODO Insert your code here'
        class_src += f'\n            self.service_{event}()'
        class_src += f'\n            return '
        for ev in fb_model.event_inputs:
            if (ev == event):
               class_src += f'EVNT_CNTR,'
            else:
               class_src += f'None,'    
        for var in fb_model.output_vars:
            class_src += f"self.{var['name']},"
        # remove last ,    
        idx = len(class_src)-1    
        class_src = class_src[:idx] + class_src[idx+1:]    
   
        
    return class_src

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert fbt to py file.")
    parser.add_argument("filename", type=str, help="The name of the fbt file to open")

    args = parser.parse_args()

    with open(args.filename, 'r') as file:
      file_content = file.read()

    parsed_fb = parse_fbt_xml(file_content)
    generated_code = generate_python_class(parsed_fb)
    
    fbtname = pathlib.Path(args.filename).stem

    with open(fbtname+".py", "w", encoding="utf-8") as file:
       file.write(generated_code)
    
    

