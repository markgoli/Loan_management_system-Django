from loans import views
from django.urls import path

urlpatterns = [
    path('', views.all_loans, name='all_loans'),
    path('apply/', views.apply_for_loan, name='apply_for_loan'),
    path('<int:loan_id>/', views.loan_detail, name='loan_detail'),
    path('<int:loan_id>/approval/', views.loan_approval, name='loan_approval'),
    path('<int:loan_id>/repayment/', views.create_loan_repayment, name='create_loan_repayment'),
    path('<int:loan_id>/repayments/<int:repayment_id>/delete/', views.delete_repayment, name='delete_repayment'),
]