from store.models import Category,Profile
from django.conf import settings

def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}


def user_profile_image(request):
    if request.user.is_anonymous:
        return {'user_profile_image':f"{settings.MEDIA_URL}uploads/profiles/avatar1.png"}
    else:
        try:
            user_profile_image = Profile.objects.get(user=request.user).image.url
            return {'user_profile_image': user_profile_image}
        except Exception:
            return {'user_profile_image':  f"{settings.MEDIA_URL}uploads/profiles/avatar1.png"}
