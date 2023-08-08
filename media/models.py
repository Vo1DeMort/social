from django.db import models
from django.conf import settings

'''
if someone is mentioned in a post (@exampleuser) ,use django signal to notify the user being mentioined
'''

'''
i am gonna migrate the db to psql to unlock the full text search feature later
'''



'''
maintain flexibility to swap out the default user model provided by Django with a custom user model that you have defined.
'''
# extending the User model
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/ < get_user_model >
class Profile(models.Model):
    # not the same with build-in User model
    # custom user_model
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    page_link = models.CharField(null=True, blank=True, max_length=100)
    # logical grouping for all user related file
    # users is an arbitary folder name
    profile_image= models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)
    # this shoud be auto_now_add
    # this is working like an 'last time update time'
    joined = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

'''
this project is the Frankenstein's moneter ,lol
'''
class Post(models.Model):
    post_creator= models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='user_post')
    story = models.TextField(max_length=300)
    #images = models.ImageField(upload_to='post_photos/')
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='post_likes',blank=True)
    
    def num_of_likes(self):
        return self.likes.count()

    '''
    class Meta:
        # Limit each user profile to have a maximum of 5 photos
        constraints = [
            models.CheckConstraint(check=models.Q(image__count__lte=5), name='max_five_photos')
        ]

    '''
    def __str__(self):
        return(
            f'{self.post_creator}'
            f'{self.story}'
            f'{self.created}'
        )


'''haven"t register the models in the admin.py yet'''
class Comments(models.Model):
    pass

class Followers(models.Model):
    pass

class Likes(models.Model):
    pass
