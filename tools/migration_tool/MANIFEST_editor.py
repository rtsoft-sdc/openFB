import xml.etree.ElementTree as ET
from pathlib import Path


class ManifestEditor:
    def __init__(self, manifest_path):
        self.manifest_path = Path(manifest_path)
        self.tree = None
        self.root = None
        self.load_manifest()

    def load_manifest(self):
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"MANIFEST.MF file {self.manifest_path} not found")
        self.tree = ET.parse(self.manifest_path)
        self.root = self.tree.getroot()

    def update_versions_with_check(self, typelibrary_path, target_version="3.0.0"):
        typelib_path = Path(typelibrary_path)
        dependencies = self.root.find('Dependencies')
        if dependencies is not None:
            for required in dependencies.findall('Required'):
                symbolic_name = required.get('SymbolicName')
                if symbolic_name:
                    lib_dir = typelib_path / f"{symbolic_name}-{target_version}"
                    if lib_dir.exists() and lib_dir.is_dir():
                        required.set('Version', target_version)

        product = self.root.find('Product')
        if product is not None:
            version_info = product.find('VersionInfo')
            if version_info is not None:
                version_info.set('Version', target_version)

    def save_manifest(self, output_path=None):
        if output_path is None:
            output_path = self.manifest_path
        else:
            output_path = Path(output_path)
        self.tree.write(output_path, encoding='UTF-8', xml_declaration=True)

    def filter_and_update_dependencies(self, typelibrary_path, target_version="3.0.0"):
        # Libraries to remove (no version 3.0.0)
        remove_libs = {'math', 'devices', 'segments', 'resources', 'storage'}
        # Libraries to add (available in version 3.0.0)
        add_libs = {'powerlink', 'system'}
        
        typelib_path = Path(typelibrary_path)
        dependencies = self.root.find('Dependencies')
        if dependencies is not None:
            # Remove old libraries
            for required in dependencies.findall('Required'):
                symbolic_name = required.get('SymbolicName')
                if symbolic_name in remove_libs:
                    dependencies.remove(required)
            
            # Update versions for remaining libraries
            for required in dependencies.findall('Required'):
                symbolic_name = required.get('SymbolicName')
                if symbolic_name and symbolic_name not in remove_libs:
                    lib_dir = typelib_path / f"{symbolic_name}-{target_version}"
                    if lib_dir.exists() and lib_dir.is_dir():
                        required.set('Version', target_version)
            
            # Add new libraries if they exist
            for lib_name in add_libs:
                lib_dir = typelib_path / f"{lib_name}-{target_version}"
                if lib_dir.exists() and lib_dir.is_dir():
                    # Check if not already present
                    exists = any(req.get('SymbolicName') == lib_name for req in dependencies.findall('Required'))
                    if not exists:
                        new_required = ET.SubElement(dependencies, 'Required')
                        new_required.set('SymbolicName', lib_name)
                        new_required.set('Version', target_version)
        
        # Update product version
        product = self.root.find('Product')
        if product is not None:
            version_info = product.find('VersionInfo')
            if version_info is not None:
                version_info.set('Version', target_version)

    def get_current_version(self):
        product = self.root.find('Product')
        if product is not None:
            version_info = product.find('VersionInfo')
            if version_info is not None:
                return version_info.get('Version')
        return None
