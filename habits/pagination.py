from rest_framework.pagination import PageNumberPagination


class HabitPagination(PageNumberPagination):
    """
    Paginare pentru habits: 5 items per pagină.
    Conform cerințelor proiectului.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100