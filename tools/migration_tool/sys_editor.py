import xml.etree.ElementTree as ET
from pathlib import Path


class SysEditor:
    def __init__(self, sys_path, typelibrary_root):
        self.sys_path = Path(sys_path)
        self.typelibrary_root = Path(typelibrary_root)
        self.tree = None
        self.root = None
        self.package_map = None
        self.load_sys()
        self.build_typelib_map()

    def load_sys(self):
        if not self.sys_path.exists():
            raise FileNotFoundError(f"SYS file {self.sys_path} not found")
        self.tree = ET.parse(self.sys_path)
        self.root = self.tree.getroot()

    def build_typelib_map(self):
        self.package_map = {}
        for ext in ('*.fbt', '*.dev', '*.res', '*.seg'):
            for f in self.typelibrary_root.rglob(ext):
                try:
                    t = ET.parse(f)
                except ET.ParseError:
                    continue
                r = t.getroot()
                ci = r.find('CompilerInfo')
                if ci is None:
                    continue
                pkg = ci.get('packageName')
                if not pkg:
                    continue
                name = r.get('Name')
                if not name:
                    continue
                self.package_map[name] = pkg

    def convert_fb_types(self):
        elements = []
        elements.extend(self.root.findall('.//FB'))
        elements.extend(self.root.findall('.//Device'))
        elements.extend(self.root.findall('.//Resource'))
        elements.extend(self.root.findall('.//Segment'))
        for el in elements:
            t = el.get('Type')
            if not t or '::' in t:
                continue
            if "F_SEL_E" in t:
                print("WARNING: in new TypeLibrary F_SEL_E FBs input/output names changed. You hve to fix this in IDE.")
            pkg = self.package_map.get(t)
            if pkg:
                el.set('Type', f"{pkg}::{t}")

    def save_sys(self, output_path=None):
        if output_path is None:
            output_path = self.sys_path
        else:
            output_path = Path(output_path)
        self.tree.write(output_path, encoding='UTF-8', xml_declaration=True)
