from django.urls import path
from .views import WebhookView, OrganizationBalanceView


urlpatterns = [
    path('webhook/bank/', WebhookView.as_view(), name='webhook_view'),
    path('organizations/<str:inn>/balance/', OrganizationBalanceView.as_view(), name='get_balance_view'),
]
