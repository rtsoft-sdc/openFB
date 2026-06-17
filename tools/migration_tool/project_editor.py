import xml.etree.ElementTree as ET
from pathlib import Path


class ProjectEditor:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.tree = None
        self.root = None
        self.load_project()

    def load_project(self):
        if not self.project_path.exists():
            raise FileNotFoundError(f".project file {self.project_path} not found")
        self.tree = ET.parse(self.project_path)
        self.root = self.tree.getroot()

    def update_build_spec(self):
        build_spec = self.root.find('buildSpec')
        if build_spec is not None:
            build_spec.clear()
            build_command3 = ET.SubElement(build_spec, 'buildCommand')
            name3 = ET.SubElement(build_command3, 'name')
            name3.text = 'org.eclipse.fordiac.ide.library.builder'
            arguments3 = ET.SubElement(build_command3, 'arguments')
            build_command1 = ET.SubElement(build_spec, 'buildCommand')
            name1 = ET.SubElement(build_command1, 'name')
            name1.text = 'org.eclipse.xtext.ui.shared.xtextBuilder'
            arguments1 = ET.SubElement(build_command1, 'arguments')
            build_command2 = ET.SubElement(build_spec, 'buildCommand')
            name2 = ET.SubElement(build_command2, 'name')
            name2.text = 'org.eclipse.fordiac.ide.export.builder'
            arguments2 = ET.SubElement(build_command2, 'arguments')


    def filter_and_update_library_links(self):

        linked = self.root.find('linkedResources')
        if linked is not None:
            # for link in list(linked):
            #     linked.remove(link)
            linked.clear()

            link1 = ET.SubElement(linked, 'link') 
            name1 = ET.SubElement(link1, 'name')
            type1 = ET.SubElement(link1, 'type')
            locationURI1 = ET.SubElement(link1, 'locationURI')
            name1.text = 'External Libraries'
            type1.text = '2'
            locationURI1.text = 'virtual:/virtual'

            link2 = ET.SubElement(linked, 'link') 
            name2 = ET.SubElement(link2, 'name')
            type2 = ET.SubElement(link2, 'type')
            locationURI2 = ET.SubElement(link2, 'locationURI')
            name2.text = 'Standard Libraries'
            type2.text = '2'
            locationURI2.text = 'virtual:/virtual'

            linked.remove(link1)
            linked.remove(link2)
            linked.insert(0, link2)
            linked.insert(0, link1)
        

    def save_project(self, output_path=None):
        if output_path is None:
            output_path = self.project_path
        else:
            output_path = Path(output_path)
        self.tree.write(output_path, encoding='UTF-8', xml_declaration=True)
