from rest_framework import routers

from kanban import viewsets


router = routers.SimpleRouter()

router.register('boards', viewsets.BoardViewset, 'boards')
router.register('columns', viewsets.ColumnViewset, 'boards')
router.register('tasks', viewsets.TaskViewset, 'tasks')
router.register('users', viewsets.UserViewset, 'users')

urlpatterns = router.urls
