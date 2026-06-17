import argparse
import shutil
import json
from pathlib import Path
from project_editor import ProjectEditor
from sys_editor import SysEditor
from MANIFEST_editor import ManifestEditor


def copy_project_tree(src_project, dest_root):
    src = Path(src_project)
    if src.is_file() and src.name == '.project':
        src = src.parent
    if not src.exists() or not src.is_dir():
        raise FileNotFoundError(f"Source project folder not found: {src}")
    dest = Path(dest_root) / src.name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    return dest

def convert_project(project_root, typelibrary_path):
    src = Path(project_root)
    project_file = src / '.project'
    if project_file.exists():
        editor = ProjectEditor(project_file)
        editor.load_project()
        editor.update_build_spec()
        editor.filter_and_update_library_links()
        editor.save_project(project_file)
        print('.project converted')
    manifest_file = src / 'MANIFEST.MF'
    if manifest_file.exists():
        manifest_editor = ManifestEditor(manifest_file)
        manifest_editor.filter_and_update_dependencies(typelibrary_path)
        manifest_editor.save_manifest(manifest_file)
        print('MANIFEST.MF converted')
    sys_file = next(src.glob('*.sys'), None)
    if sys_file is not None:
        sys_editor = SysEditor(sys_file, typelibrary_path)
        sys_editor.convert_fb_types()
        sys_editor.save_sys(sys_file)
        print(f'{sys_file.name} converted')


def main():
    parser = argparse.ArgumentParser(description='PROJECT_CONVERTER v2 to v3')
    parser.add_argument('--project', help='path to v2 project folder or .project file')
    parser.add_argument('--typelibrary', help='path to typelibrary folder')
    parser.add_argument('--config', help='path to JSON config file with typelibrary and projects list')
    parser.add_argument('--out', default='./converted_projects', help='output base directory')
    args = parser.parse_args()

    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        typelibrary_path = Path(config['typelibrary'])
        projects = config['projects']
        out_root = Path(args.out)
        out_root.mkdir(parents=True, exist_ok=True)
        for project_path in projects:
            dest_project = copy_project_tree(project_path, out_root)
            convert_project(dest_project, typelibrary_path)
            print(f'Converted: {dest_project}')
    else:
        if not args.project or not args.typelibrary:
            parser.error('--project and --typelibrary are required when --config is not used')
        out_root = Path(args.out)
        out_root.mkdir(parents=True, exist_ok=True)
        dest_project = copy_project_tree(args.project, out_root)
        convert_project(dest_project, Path(args.typelibrary))
        print('Conversion complete:', dest_project)


if __name__ == '__main__':
    main()
