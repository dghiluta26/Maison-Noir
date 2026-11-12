from rest_framework.pagination import PageNumberPagination


class CataloguePagination(PageNumberPagination):
    """
    DRF page-number envelope: {count, next, previous, results}.

    The default page size fits the whole P2 catalogue (32 products) on one page;
    clients can request smaller pages with ?page_size=.
    """

    page_size = 48
    page_size_query_param = "page_size"
    max_page_size = 100
