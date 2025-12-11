import os
import argparse
from pathlib import Path
from xml.etree import ElementTree as ETree

HEAD_LINE = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str, help="Path to fbt file")
    parser.add_argument("--opc", "-o", type=bool, default=False,
                        help="Modify block for usage under OPC UA.")
    args = parser.parse_args()
    return args


def get_vars(xml_data):
    events = ["EventInputs", "EventOutputs"]
    vars = ["InputVars", "OutputVars"]
    output = {"input_vars": [], "output_vars": [],
              "input_events": [], "output_events": []}

    for e in events:
        selection_io = ""
        if e == "EventInputs":
            selection_io = "input"
        else:
            selection_io = "output"
        for i in xml_data.findall(".//%s" % e):
            for item in i.findall("./Event"):
                output[f"{selection_io}_events"].append(item.get("Name"))

    # Double run to be sure that we have all IO variables
    for v in vars:
        if v == "InputVars":
            dtype = "input_vars"
        else:
            dtype = "output_vars"
        defenition = xml_data.findall(".//%s" % v)
        if len(defenition) == 1:
            for item in defenition[0].findall("./VarDeclaration"):
                output[dtype].append(item.get("Name"))

    output["input_vars"] = list(dict.fromkeys(output["input_vars"]))
    output["output_vars"] = list(dict.fromkeys(output["output_vars"]))

    return output


def generate_script(path, name, input, outputs_v, input_e, output_e):
    name = name.split('.')
    class_def = "class %s:\n" % name[0]
    input_args = ', '.join(input)
    schedule_def = " "*4 + \
        "def schedule(self, event_input_name, event_input_value, % s ):\n" % input_args
    dummy_block = class_def + schedule_def + " "*8 + "'Write your code here.'\n"
    output_line = " "*12 + "return " + \
        ', '.join(output_e) + ', ' + ', '.join(outputs_v) + '\n'
    for event in input_e:
        handler = ""
        handler += " "*8 + "if event_input_name == '%s':\n" % event
        handler += " "*12 + '"Write your handler for current event here."\n'
        handler += output_line
        dummy_block += handler
    script_path = os.path.join(path, name[0]+'.py')
    with open(script_path, 'w') as dummy_writer:
        dummy_writer.write(dummy_block)
    print("Dummy block was generated")


if __name__ == "__main__":
    args = get_args()
    filepath = Path(args.file)
    file_parent_dir = filepath.parent

    xml_data = ETree.parse(filepath)
    xml_root = xml_data.getroot()
    vars = get_vars(xml_data)
    print(vars)
    blocks4remove = ['Identification', 'VersionInfo', 'BasicFB', 'SimpleFB']
    for block in blocks4remove:
        remb = xml_root.find(block)
        if remb != None:
            print("Removed %s " % block)
            xml_root.remove(remb)
    xml2str = ETree.tostring(xml_root).decode('utf-8').split('\n')
    xml2str[-1] = xml2str[-1].replace('\t', '')
    xml2str = HEAD_LINE + '\n'.join(xml2str)
    with open(filepath, 'w') as output:
        output.writelines(xml2str)
    generate_script(file_parent_dir, filepath.name,
                    vars["input_vars"], vars["output_vars"], vars["input_events"], vars["output_events"])

    print("Conversion finished")
