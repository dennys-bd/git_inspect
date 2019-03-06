from django.db.models import QuerySet

class CommitQuerySet(QuerySet):
    def order_by_date(self):
        return self.order_by("-created_at")
