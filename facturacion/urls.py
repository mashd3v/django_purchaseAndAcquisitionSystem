from django.urls import path, include
from .views import CustomerView, NewCustomer, UpdateCustomer, deactivateCustomer, \
    BillingView, billings, \
    ProductView, \
    deleteBillingDetail
from .reports import printBillingReceipt, printBillingList

urlpatterns = [
    path('customer/', CustomerView.as_view(), name="customerList"),
    path('customer/new', NewCustomer.as_view(), name="newCustomer"),
    path('customer/<int:pk>', UpdateCustomer.as_view(), name="updateCustomer"),
    path('customer/status/<int:id>', deactivateCustomer, name="deactivateCustomer"),

    path('billing/', BillingView.as_view(), name="billingList"),
    path('billing/new', billings, name="newBilling"),
    path('billing/edit/<int:id>', billings, name="updateBilling"),

    path('billing/searchProduct', ProductView.as_view(), name="productBilling"),

    path('billing/deleteDetail/<int:id>', deleteBillingDetail, name="deleteBillingDetail"),

    path('billing/print/<int:id>', printBillingReceipt, name="printOneBilling"),
    path('billing/printAll/<str:date1>/<str:date2>', printBillingList, name="printBillingList"),
]