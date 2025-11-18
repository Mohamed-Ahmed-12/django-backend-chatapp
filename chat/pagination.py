from rest_framework.pagination import CursorPagination

class MessagesPagination(CursorPagination):
    page_size = 11
    ordering = '-created_at'   # newest first