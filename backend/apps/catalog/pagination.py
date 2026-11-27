from rest_framework.pagination import PageNumberPagination


class CataloguePagination(PageNumberPagination):
    """
    Public catalogue pages. DRF page-number envelope: {count, next, previous, results}.

    Spec A1: at most 24 products per page. Clients may ask for smaller pages with
    ?page_size=, but never larger ones (?page_size=100 still returns 24).
    """

    page_size = 24
    page_size_query_param = "page_size"
    max_page_size = 24


class AdminPagination(PageNumberPagination):
    """Admin lists: larger pages, so the whole catalogue fits in one admin table."""

    page_size = 48
    page_size_query_param = "page_size"
    max_page_size = 100
