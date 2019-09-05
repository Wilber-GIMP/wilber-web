import shutil
import tempfile
import zipfile
import json
import os
from collections import OrderedDict
from os import path


class FileNotFound(Exception):
    pass

class WilberPackage(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def check(self):
        zip = zipfile.ZipFile(self.filepath)
        file_list = zip.namelist()

        self.package_root = 'GIMP'
        self.manifest_filepath = path.join(self.package_root, 'manifest.txt')
        if self.manifest_filepath not in file_list:
            raise FileNotFound(self.manifest_filepath)

        manifest_file = zip.open(self.manifest_filepath)
        manifest_content = manifest_file.read()
        self.check_manifest(manifest_content, file_list)
        return True

    def check_manifest(self, manifest_content, file_list):
        manifest = json.loads(manifest_content)
        file_list = [f for f in file_list if not f.endswith('/')]
        if sorted(manifest['file_list']) != sorted(file_list):
            raise ValueError("The files in manifest doesnt correspond to the zip content")

        self.name = manifest['name']
        self.description = manifest['description']
        self.software = manifest['software']
        self.wilber_package_version = manifest['wilber_package_version']
        self.image = manifest['image']
        self.category = manifest['category']

        return True


    def rename_wilber_files(self, pk):
        package_path = path.join(self.temp_dir, self.package_root)
        wilber_path = path.join(package_path, 'plug-ins/wilber/assets/%s' % self.category)
        os.makedirs(wilber_path)

        image_filepath = path.join(self.temp_dir, self.image)
        manifest_filepath = path.join(self.temp_dir, self.manifest_filepath)
        image_filename = path.basename(image_filepath)

        new_image_path = path.join(wilber_path, "%05d_%s" % (pk, image_filename))
        new_manifest_path = path.join(wilber_path, "%05d_%s" % (pk, 'manifest.txt'))

        shutil.move(image_filepath, new_image_path)
        shutil.move(manifest_filepath, new_manifest_path)

        self.image = path.relpath(new_image_path, path.join(self.temp_dir, self.package_root))

        self.create_manifest(new_manifest_path, package_path)

    def get_file_list(self, folder, base_path=None):
        file_list = []
        if base_path is None:
            base_path = folder

        for root, dirs, files in os.walk(folder):
            for name in files:
                filepath = os.path.join(root, name)
                file_list.append(os.path.relpath(filepath, start=base_path))

        return sorted(file_list)


    def generate_manifest_data(self, file_list):
        data = OrderedDict([
            ('name', self.name),
            ('description', self.description),
            ('software', self.software),
            ('category', self.category),
            ('image', self.image),
            ('wilber_package_version', self.wilber_package_version),
            ('file_list', file_list)]
        )
        return json.dumps(data, indent=4)

    def create_manifest(self, manifest_path, package_path):
        with open(manifest_path, 'w') as f:
            file_list = self.get_file_list(package_path)
            f.write(self.generate_manifest_data(file_list))

    def get_new_asset_name(self, fpath, pk, slug, i):
        basename, ext = path.splitext(fpath)
        new_name = "%05d_%s_%d%s" % (pk, slug, i + 1, ext)
        return new_name

    def rename_asset_files(self, pk, slug):
        asset_path = path.join(self.temp_dir, self.package_root, self.category)
        for i, fname in enumerate(sorted(os.listdir(asset_path))):
            new_name = self.get_new_asset_name(fname, pk, slug, i)
            oldpath = path.join(asset_path, fname)
            newpath = path.join(asset_path, new_name)
            os.rename(oldpath, newpath)



    def unpack(self):
        self.temp_dir = tempfile.mkdtemp(prefix="WilberPackage_")
        shutil.unpack_archive(self.filepath, self.temp_dir)

        self.rename_asset_files(pk=666, slug='night')
        self.rename_wilber_files(pk=666)
        package_name = 'wilber_package'
        package_path = path.join(self.temp_dir, package_name)
        shutil.make_archive(package_path, 'zip', self.temp_dir, self.package_root)
        shutil.rmtree(path.join(self.temp_dir, self.package_root))

        return package_path

    def process(self):
        if self.check():
            return self.unpack()



if __name__ == '__main__':
    #package = WilberPackage("/home/darpan/Dropbox/projects/wilber/wilber-web/wilber/media/assets/2019/09/05/brushes/000258__teste_package/000258__brushes_teste_package.zip")

    package = WilberPackage("/tmp/WilberPackage_L0HUUl/package_file.zip")

    package_path = package.process()
    import subprocess
    subprocess.call(["xdg-open", path.dirname(package_path)])