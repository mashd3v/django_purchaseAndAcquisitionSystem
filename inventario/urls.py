from django.urls import path
from .views import CategoryView, NewCategory,UpdateCategory, DeleteCategory, \
    SubcategoryView, NewSubcategory, UpdateSubcategory, DeleteSubcategory, \
    BrandView, NewBrand, UpdateBrand, activateBrand,deactivateBrand, \
    MeasurementUnitsView, NewMeasurementUnits, UpdateMeasurementUnits, activateMeasurementUnits,deactivateMeasurementUnits, \
    ProductView, NewProduct, UpdateProduct, activateProduct, deactivateProduct

urlpatterns = [
    path('categories/', CategoryView.as_view(), name='categoryList'),
    path('categories/new', NewCategory.as_view(), name='newCategory'),
    path('categories/edit/<int:pk>', UpdateCategory.as_view(), name='updateCategory'),
    path('categories/delete/<int:pk>', DeleteCategory.as_view(), name='deleteCategory'),

    path('subcategories/', SubcategoryView.as_view(), name='subcategoryList'),
    path('subcategories/new', NewSubcategory.as_view(), name='newSubcategory'),
    path('subcategories/edit/<int:pk>', UpdateSubcategory.as_view(), name='updateSubcategory'),
    path('subcategories/delete/<int:pk>', DeleteSubcategory.as_view(), name='deleteSubcategory'),

    path('brand/', BrandView.as_view(), name='brandList'),
    path('brand/new', NewBrand.as_view(), name='newBrand'),
    path('brand/edit/<int:pk>', UpdateBrand.as_view(), name='updateBrand'),
    path('brand/activate/<int:id>', activateBrand, name='activateBrand'),
    path('brand/deactivate/<int:id>', deactivateBrand, name='deactivateBrand'),

    path('measurementUnits/', MeasurementUnitsView.as_view(), name='measurementUnitsList'),
    path('measurementUnits/new', NewMeasurementUnits.as_view(), name='newMeasurementUnits'),
    path('measurementUnits/edit/<int:pk>', UpdateMeasurementUnits.as_view(), name='updateMeasurementUnits'),
    path('measurementUnits/activate/<int:id>', activateMeasurementUnits, name='activateMeasurementUnits'),
    path('measurementUnits/deactivate/<int:id>', deactivateMeasurementUnits, name='deactivateMeasurementUnits'),

    path('product/', ProductView.as_view(), name='productList'),
    path('product/new', NewProduct.as_view(), name='newProduct'),
    path('product/edit/<int:pk>', UpdateProduct.as_view(), name='updateProduct'),
    path('product/activate/<int:id>', activateProduct, name='activateProduct'),
    path('product/deactivate/<int:id>', deactivateProduct, name='deactivateProduct'),
]