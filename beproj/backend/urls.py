from rest_framework import routers
from .views import *
router = routers.DefaultRouter()
router.register('policy', PolicyViewSet)
router.register('elements', ElementViewSet)
router.register('element-flags', ElementFlagViewSet)

urlpatterns =  router.urls