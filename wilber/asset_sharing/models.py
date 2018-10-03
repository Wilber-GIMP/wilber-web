from django.db import models

# Create your models here.


from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Brush(Asset):
    pass

class Pattern(Asset):
    pass
