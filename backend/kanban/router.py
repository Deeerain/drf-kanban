from rest_framework import routers

from kanban import viewsets


router = routers.SimpleRouter()

router.register('boards', viewsets.BoardViewset, 'boards')
router.register('columns', viewsets.ColumnViewset, 'boards')

urlpatterns = router.urls
