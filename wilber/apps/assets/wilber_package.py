import json
import os
import shutil
import tempfile
import zipfile
from collections import OrderedDict
from os import path


class FileNotFound(Exception):
    pass


class WilberPackage(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.package_root = "GIMP"

    def read_manifest(self, manifest_file, file_list):
        manifest_content = manifest_file.read()
        manifest = json.loads(manifest_content)

        return manifest

    def check_manifest(self, manifest, file_list, pk, slug):
        file_list = sorted([f for f in file_list if not f.endswith("/")])
        if sorted(manifest["file_list"]) != file_list:
            print(file_list)
            print(sorted(manifest["file_list"]))
            return False

        return True

    def check_is_wilber_package(self, file_list, pk, slug):
        """
        Check if it is an already processed Wilber Package
        """
        manifest_path = self.get_path_manifest(pk, slug)

        if path.relpath(manifest_path, self.package_root) not in file_list:
            return False

        manifest = self.read_manifest(
            self.zipfile.open(manifest_path), file_list
        )
        image_path = self.get_path_image(manifest["image"], pk, slug)

        if path.relpath(image_path, self.package_root) not in file_list:
            return False

        return True

    def check_is_plugin_package(self, file_list, pk, slug):
        self.manifest_filepath = path.join(self.package_root, "manifest.txt")

        if self.manifest_filepath not in file_list:
            print("Manifest is not on package!")
            return False

        manifest = self.read_manifest(
            self.zipfile.open(self.manifest_filepath), file_list
        )
        manifest_ok = self.check_manifest(manifest, file_list, pk, slug)

        if not manifest_ok:
            print("Error in manifest")
            return False

        image_path = manifest["image"]
        if image_path not in file_list:
            print("Image file not found")
            return False
        return manifest

    def get_path_wilber(self):
        package_path = self.package_root
        wilber_path = path.join(package_path, "plug-ins/wilber/assets/")

        return wilber_path

    def get_path_manifest(self, pk, slug):
        wilber_path = self.get_path_wilber()
        new_manifest_path = path.join(
            wilber_path, "%05d_%s" % (pk, "manifest.txt")
        )
        return new_manifest_path

    def get_path_image(self, image_path, pk, slug):
        wilber_path = self.get_path_wilber()
        image_filepath = path.join(self.package_root, image_path)
        basename, ext = path.splitext(image_filepath)
        new_image_path = path.join(
            wilber_path, "%05d_%s%s" % (pk, "image", ext)
        )
        return new_image_path

    def rename_wilber_files(self, manifest, pk, slug):
        manifest_filepath = path.join(self.temp_dir, self.manifest_filepath)
        new_manifest_path = path.join(
            self.temp_dir, self.get_path_manifest(pk, slug)
        )

        image_filepath = path.join(self.temp_dir, manifest["image"])
        new_image_path = path.join(
            self.temp_dir, self.get_path_image(manifest["image"], pk, slug)
        )

        os.makedirs(path.join(self.temp_dir, self.get_path_wilber()))

        shutil.move(image_filepath, new_image_path)
        shutil.move(manifest_filepath, new_manifest_path)
        package_path = path.join(self.temp_dir, self.package_root)

        manifest["image"] = path.relpath(new_image_path, package_path)

        self.create_manifest(manifest, new_manifest_path, package_path)

    def get_file_list(self, folder, base_path=None):
        file_list = []
        if base_path is None:
            base_path = folder

        for root, dirs, files in os.walk(folder):
            for name in files:
                filepath = os.path.join(root, name)
                file_list.append(os.path.relpath(filepath, start=base_path))

        return sorted(file_list)

    def generate_manifest_data(self, manifest, file_list):
        data = OrderedDict(
            [
                ("name", manifest["name"]),
                ("description", manifest["description"]),
                ("software", manifest["software"]),
                ("category", manifest["category"]),
                ("image", manifest["image"]),
                ("wilber_package_version", manifest["wilber_package_version"]),
                ("file_list", file_list),
            ]
        )
        return json.dumps(data, indent=4)

    def create_manifest(self, manifest, manifest_path, package_path):
        with open(manifest_path, "w") as f:
            file_list = self.get_file_list(package_path)
            f.write(self.generate_manifest_data(manifest, file_list))

    def get_new_asset_name(self, fpath, pk, slug, i):
        basename, ext = path.splitext(fpath)
        new_name = "%05d_%s_%d%s" % (pk, slug, i + 1, ext)
        return new_name

    def rename_asset_files(self, manifest, pk, slug):
        asset_path = path.join(
            self.temp_dir, self.package_root, manifest["category"]
        )
        for i, fname in enumerate(sorted(os.listdir(asset_path))):
            new_name = self.get_new_asset_name(fname, pk, slug, i)
            oldpath = path.join(asset_path, fname)
            newpath = path.join(asset_path, new_name)
            os.rename(oldpath, newpath)

    def repack(self, manifest, pk, slug):

        shutil.unpack_archive(self.filepath, self.temp_dir)

        self.rename_asset_files(manifest, pk, slug)
        self.rename_wilber_files(manifest, pk, slug)
        package_name = "wilber_package"
        package_path = path.join(self.temp_dir, package_name)
        shutil.make_archive(
            package_path, "zip", self.temp_dir, self.package_root
        )
        shutil.rmtree(path.join(self.temp_dir, self.package_root))
        package_fullpath = path.join(self.temp_dir, package_name + ".zip")
        return package_fullpath

    def process(self, pk, slug):
        self.zipfile = zipfile.ZipFile(self.filepath)
        self.temp_dir = tempfile.mkdtemp(prefix="WilberPackage_")
        file_list_plugin = sorted(
            [f for f in self.zipfile.namelist() if not f.endswith("/")]
        )
        file_list_wilber = sorted(
            [path.relpath(f, self.package_root) for f in file_list_plugin]
        )

        if self.check_is_wilber_package(file_list_wilber, pk, slug):
            return None, "Its already a Wilber package, not processed"
        manifest = self.check_is_plugin_package(file_list_plugin, pk, slug)
        if manifest:
            return (
                self.repack(manifest, pk, slug),
                "Package converted succesfuly",
            )
        return False, "This file looks not as a wilber package! Nothing done"

    def clean(self):
        shutil.rmtree(self.temp_dir)
