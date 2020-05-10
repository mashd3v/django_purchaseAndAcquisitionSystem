from django.urls import path
from compras.views import SupplierView, NewSupplier, UpdateSupplier, deactivateSuppliers, \
    AcquisitionView, acquisition, AcquisitionDetailDelete
from .reports import acquisitionsReport, printAcquisition

urlpatterns = [
    path('supplier/', SupplierView.as_view(), name="supplierList"),
    path('supplier/new', NewSupplier.as_view(), name="newSupplier"),
    path('supplier/edit/<int:pk>', UpdateSupplier.as_view(), name="updateSupplier"),
    path('supplier/deactivate/<int:id>', deactivateSuppliers, name="deactivateSuppliers"),

    path('acquisition/', AcquisitionView.as_view(), name="acquisitionList"),
    path('acquisition/new', acquisition, name="acquisitionNew"),
    path('acquisition/edit/<int:acquisition_id>', acquisition, name="updateAcquisition"),
    path('acquisition/<int:acquisition_id>/delete/<int:pk>', AcquisitionDetailDelete.as_view(), name="deleteAcquisition"),

    path('acquisition/list', acquisitionsReport, name='printAllAcquisitions'),
    path('acquisition/<int:acquisition_id>/print', printAcquisition, name='printOneAcquisition'),
]