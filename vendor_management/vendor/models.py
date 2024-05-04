from django.db import models
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.name
    
    def update_performance_metrics(self):
        # On-Time Delivery Rate
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        self.on_time_delivery_rate = (on_time_delivered_pos / total_completed_pos) * 100 if total_completed_pos > 0 else 0.0

        # Quality Rating Average
        completed_pos_with_ratings = completed_pos.exclude(quality_rating__isnull=True)
        self.quality_rating_avg = completed_pos_with_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0.0
        
        # Average Response Time
        acknowledged_pos = completed_pos.exclude(acknowledgment_date__isnull=True)
        response_times = [(pos.acknowledgment_date - pos.issue_date).total_seconds() for pos in acknowledged_pos]
        average_response_time_seconds = sum(response_times) / len(response_times) if response_times else 0.0
        self.average_response_time = average_response_time_seconds

        # Fulfilment Rate
        total_pos = self.purchaseorder_set.count()
        successfully_fulfilled_pos = completed_pos.filter(quality_rating__isnull=False).count()
        self.fulfillment_rate = (successfully_fulfilled_pos / total_pos) * 100 if total_pos > 0 else 0.0

        self.save()



class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
