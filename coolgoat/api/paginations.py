from rest_framework.pagination import PageNumberPagination

class FixturesPageNumberPagination(PageNumberPagination):
    page_size = 25  
    page_size_query_param = 'count'  
