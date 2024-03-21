from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login_request, name="login"),
    path('payorder/', views.payorder, name="Payorder"),
    path('receiveit/', views.ReceiveIt, name="Receive It"),
    path('package/<int:package_id>/', views.PackageDetails, name="package_details"),
    path('ShowAllpackages/', views.AllPackages, name="All Packages"),
    path('ShowAllProducts/', views.AllProducts, name="All Products"),
    path('ShowAllLogistics/', views.AllLogistics, name="All Logistics"),
    path('DispatchPack/<int:package_id>/', views.DispatchPack , name='Dispatch Package'),
    path('EditProduct/<int:product_id>/', views.EditProduct , name='Edit Product'),
    path('EditLogistics/<int:logistic_id>/', views.EditLogistics , name='Edit Logistics'),
    path('AddProduct/', views.AddProduct , name='Add Product'),
    path('AddLogistics/', views.AddLogistics, name="Add Logistics"),

    path('Dashboard/', views.RenderDashboard, name="Show Dashboard"),
    path('logout/', views.logout_request, name="Logout"),
]
