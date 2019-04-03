from os.path import join
from os import remove, listdir
from subprocess import call
from random import choice

from django.core.management.base import BaseCommand
from django.utils import timezone

from django.conf import settings
from django.core.files import File

from os.path import join
from django.db import transaction

from users.models import User
from assets.models import Asset


NAMES = ['Kurtis Andrews',
 'Dana Cox',
 'Diane Moore',
 'Dean Carrillo',
 'Jose Meador',
 'Pamela Zordan',
 'Joseph Whitlock',
 'Valerie Zanes',
 'Danny Phelps',
 'Robert Coello',
 'Jeffery Kleven',
 'Kenneth Anderson',
 'Vera Bullock',
 'Tamatha Franklin',
 'Arthur Joseph',
 'Joseph Mogan',
 'Allen Hardman',
 'Adam Schaefer',
 'Timothy Koffman',
 'Kelly Doland',
 'Roderick Hester',
 'Kim Horn',
 'Willie Benjamin',
 'Kevin Diaz',
 'Juanita Mccaughey',
 'Mary Johnson',
 'Barbara Barbour',
 'John Dennis',
 'Ryan Robles',
 'Margaret Chatman',
 'Andrea Sabir',
 'John West',
 'Philip Walter',
 'Ernest Wilson',
 'George Hart',
 'Len Sweet',
 'Ashley Justice',
 'Ronald Durisseau',
 'David Olson',
 'Agnes Brewer',
 'Albert Canty',
 'Carmen Townsend',
 'Clara Ferguson',
 'Douglas Crawford',
 'Sylvia Dickens',
 'Thomas Arrington',
 'Alexander Byers',
 'Daryl Lacoy',
 'Misty Lopez',
 'Theresa Dickert',
 'Tracy Rottenberg',
 'Edward Gibson',
 'Randi Bradburn',
 'Barbara Gibson',
 'Susan Smith',
 'Bradley Prescott',
 'Bret Rose',
 'Everett Ramirez',
 'Edward Peeden',
 'Jonathan Hannah',
 'James Daniel',
 'Rebecca Andreozzi',
 'Dorothy Theiss',
 'Denise Cowman',
 'Jeffery Maddox',
 'Joseph Bryan',
 'Robert Laflamme',
 'Leigh Bilsborough',
 'David Robinson',
 'Veronica Gamblin',
 'Hal Putnam',
 'Charles Foley',
 'Joshua Boykin',
 'Reginald Mackay',
 'Linda Beattie',
 'Gerald Browning',
 'Donald Raybon',
 'Melvin Whitting',
 'Kena Torno',
 'Viola Sherman',
 'Shana Terry',
 'Priscilla Smolka',
 'James Hatcher',
 'Kenneth Mckinney',
 'Sophia Cannon',
 'Carlo Ciotti',
 'Terri Johnson',
 'David Heidelberg',
 'Talisha Brunet',
 'Rebecca Camel',
 'Dana Haney',
 'Steve Goodell',
 'Bruce Figueroa',
 'Ella Kelley',
 'Alexis Hudson',
 'James Rodriguez',
 'Angie Duncan',
 'David Drake',
 'Annie Gentry',
 'Levi Orlando']

lorem =["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus in nisl mollis, bibendum arcu non, fermentum dui. Proin congue sapien ut arcu finibus, nec mollis justo pharetra. Donec eget mauris vel arcu tempus euismod. Duis posuere pharetra massa non sodales. Nam eu tristique ligula. Quisque feugiat elit odio, in dignissim magna lobortis quis. In in rhoncus ligula. Proin vitae ligula non quam pulvinar congue. Nulla facilisi. Aliquam et nibh arcu. In sit amet ligula maximus, iaculis massa volutpat, posuere nulla.",

"Fusce vitae nulla ante. Nam ligula lacus, dignissim feugiat quam non, sollicitudin placerat orci. Nam interdum erat quis pulvinar vehicula. Maecenas quam enim, consectetur posuere lorem quis, molestie cursus orci. Vestibulum porta venenatis nisl sit amet molestie. Praesent ac erat mollis, sagittis tellus a, scelerisque massa. Sed vel ultricies turpis. Nunc vestibulum, odio varius dapibus mollis, lectus elit tincidunt magna, eu feugiat nisi est non dui. Phasellus at turpis quis felis feugiat sagittis ornare a diam. Fusce non eleifend ex. Curabitur cursus orci ac lacus convallis, vitae volutpat mi luctus. Quisque at eleifend lorem. Mauris tincidunt mauris et orci tincidunt auctor. Nullam ex sapien, laoreet vitae gravida eu, tempor vitae purus.",

"Donec semper et nunc a rutrum. Mauris sagittis nulla ut sagittis elementum. Curabitur ut malesuada tellus, sed pellentesque velit. Nullam vitae tincidunt purus. In libero nibh, tristique vel leo eu, malesuada mattis elit. Duis vel tincidunt lacus. Aenean orci nulla, egestas eget sollicitudin ac, rhoncus eu nibh. Pellentesque eu elementum dolor, eleifend aliquet eros. Morbi arcu massa, mattis convallis vehicula ac, egestas ut purus. Nam mi neque, consectetur posuere ligula vel, interdum commodo ipsum.",

"Morbi efficitur diam vel libero consequat, et blandit lacus vestibulum. Etiam finibus tortor ut ipsum faucibus maximus. Nulla dolor elit, convallis et risus in, suscipit suscipit ipsum. Maecenas lacinia nisi libero, et posuere lorem convallis ornare. Aenean vel sapien vitae purus ultricies condimentum id sit amet est. Quisque venenatis, turpis vel tincidunt accumsan, leo erat vehicula mauris, eget pretium odio nunc eu velit. Proin et justo ac dui placerat vehicula. Mauris ac tristique eros. Nam cursus mollis nulla, ut ultrices tellus vehicula vitae. Proin vel hendrerit libero. Proin finibus, odio vitae vehicula fermentum, augue dolor dapibus odio, sed auctor urna ex in purus. Vivamus mauris urna, blandit in hendrerit non, facilisis eget ligula. Phasellus eu diam non tortor laoreet ultrices vulputate eget magna. Nam sit amet varius eros, tempor porttitor magna. Ut sollicitudin ac dui ac semper. Donec quis volutpat purus, iaculis elementum diam.",

"Sed aliquet vulputate magna sit amet porttitor. Vestibulum tincidunt ligula vitae lorem faucibus, id placerat eros facilisis. Nunc consectetur elit eget velit pellentesque commodo. Sed urna ex, aliquam maximus euismod at, laoreet sed ipsum. Nam vitae vehicula felis, in iaculis velit. Proin hendrerit vehicula lacus, quis vehicula leo ultricies et. Quisque convallis tortor at justo euismod, placerat vulputate neque tincidunt. Mauris sit amet ligula eget ante accumsan viverra. Aliquam viverra ex at felis porttitor posuere. Vivamus nec erat feugiat, vulputate erat ut, pretium nibh. Nunc sit amet diam metus. Nullam condimentum purus et odio interdum feugiat. Integer in elit sit amet magna fermentum condimentum.",
]

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
        print(join(settings.BASE_DIR,'data'))
        
        self.restart_db()
        self.populate_admin()
        self.populate_users()
        self.populate_assets()
        
    def restart_db(self):
        db = join(settings.BASE_DIR , 'db.sqlite3')
        remove(db)
        call(['python', 'manage.py', 'migrate'])
        
    def populate_admin(self):
        user = User.objects.create_superuser('admin', 'admin@myproject.com', 'password')
        print("Created superuser", user)
        
    def populate_users(self):
        for name in NAMES[:5]:
            first, last = name.split()
            username = '.'.join(name.lower().split())
            password = 'password'
            email = "%s@email.com" % username
            user = User.objects.create(username=username, email=email, password=password, first_name=first, last_name=last)
            print("Created user", user)
            
            
            
    def populate_assets_type(self, type):
        base_img = join(settings.BASE_DIR, 'data', 'images')
        images = listdir(base_img)
        
        base = join(settings.BASE_DIR, 'data', type)
        for f in listdir(base):
            user = choice(User.objects.all())
            image = choice(images)
            image_path = join(base_img, image)
            
            fpath = join(base, f)
            desc=choice(lorem)
            asset = Asset.objects.create(name=f,  owner=user, type=type, description = desc)
            asset.file.save(f, File(open(fpath, 'rb')))
            asset.image.save(image, File(open(image_path, 'rb')))
            print("created asset", asset)
        
        
    def populate_assets(self):
        
        self.populate_assets_type('brush')
        self.populate_assets_type('gradient')
        
