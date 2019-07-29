from django.core.management.base import BaseCommand

import os
from assets.models import Asset
from users.models import User
from django.core.files import File


def listfolders(path):
    return [os.path.join(path, o) for o in os.listdir(path) if os.path.isdir(os.path.join(path,o))]


def get_user():
    u = User.objects.get(username='deviantart')
    if u:
        return u
    u = User.objects.create_user('deviantart', 'deviantart@wilber.social', 'deviant-art')
    return u


def create_asset(name, description, category, image_path, asset_file_path, url):


    u = get_user()

    asset, created = Asset.objects.get_or_create(
        name=name,
        defaults={'source': url, 'description':description, 'owner':u, 'category':category},
    )

    asset.source = url
    asset.description = description
    asset.owner = u
    asset.category = category

    asset_file = open(asset_file_path, 'rb')
    asset.file.save(os.path.basename(asset_file_path), File(asset_file))

    image_file = open(image_path, 'rb')
    asset.image.save(os.path.basename(image_path), File(image_file))


    asset.save()


def parse_asset(asset, category):
    #print(category, asset)
    files = os.listdir(asset)
    try:
        name = os.path.basename(asset)
        url = open(os.path.join(asset, 'url.txt'),'r').read()
        description = open(os.path.join(asset, 'description.txt'),'r').read()
        image = os.path.join(asset, [f for f in files if f.rsplit('.',1)[-1] in ['png', 'jpg']][0])
        asset_file = os.path.join(asset, [f for f in files if 'zip' in f.rsplit('.',1)[-1]][0])

    except:
        print('ERROR',files)
    else:
        create_asset(name, description, category, image, asset_file, url)





def parse_category(folder):
    category = os.path.basename(folder)
    assets = listfolders(folder)
    for asset in assets:
        parse_asset(asset, category)


def parse_folders(path):
    for folder in listfolders(path):
        parse_category(folder)


class Command(BaseCommand):
    help = 'Load assets from folder'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs=1, type=str)

    def handle(self, *args, **kwargs):
        path = kwargs.get('path', None)
        if path:
            path=path[0]
            print('loading', path)
            parse_folders(path)
        else:
            print('Enter path')
