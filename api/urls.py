from .views import MovieViewSet, ActorViewSet, CustomerViewSet, AddressViewSet, CountryViewSet, RentalViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('actors', ActorViewSet)
router.register('addresses', AddressViewSet)
router.register('countries', CountryViewSet)
router.register('customers', CustomerViewSet)
router.register('rentals', RentalViewSet)

urlpatterns = router.get_urls()
