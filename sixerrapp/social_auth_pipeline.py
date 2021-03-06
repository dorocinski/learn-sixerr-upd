from .models import Profile

def save_avatar(backend, user, response, *args, **kwargs):
    try:
        profile = Profile.objects.get(user_id=user.id)
    except Profile.DoesNotExist:
        profile = Profile(user_id=user.id)

    if backend.name == 'facebook':
        profile.avatar = response['picture']['data']['url']
        #profile.avatar = 'http://graph.facebook.com/%s/picture?type=large' %  response['id']
    profile.save()

#Tutorial bom aqui: https://www.digitalocean.com/community/tutorials/django-authentication-with-facebook-instagram-and-linkedin
