from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination

class StandardResultsSetPagination(LimitOffsetPagination):
    max_limit = 20


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 20
