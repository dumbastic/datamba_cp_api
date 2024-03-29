from django.urls import include, path
from rest_framework import routers
from goers import views

router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'training', views.TrainingViewSet)
router.register(r'recommendation', views.RecommendationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
