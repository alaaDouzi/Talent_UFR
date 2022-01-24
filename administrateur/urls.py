from django.urls import path
from administrateur import views
# Create your tests here.

urlpatterns = [
    path('filiere', views.get_add_filiere),
    path('filiere/<slug:id>', views.update_filiere),
    path('tuteur', views.get_add_tuteur),
    path('tuteur/<int:id>', views.update_tuteur),
    path('motCle', views.get_add_mot_cle),
    path('motCle/<int:id>', views.update_mot_cle),
]


# re_path(r"^blog/(?P<year>[0-9]{4})/(?P<slug>[\w-]+)/$"
