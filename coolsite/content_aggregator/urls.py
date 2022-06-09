from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView, TokenObtainPairView
from .views import *


urlpatterns = [
    path('home/', ContentHome.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    # path('api/', APIView.as_view(), name='api'),
    path('contacts/', show_contacts, name='contacts'),

    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    
    path('profile/create', UserCategoriesCreateView.as_view(), name='create_user_categories'),
    path('profile/<slug:slug>/categories', UserCategoriesUpdateView.as_view(), name='edit_user_categories'),
    path('profile/<slug:slug>/', UserProfileView.as_view(), name='user_profile'),
    path('profile/<slug:slug>/edit/', UserProfileUpdateView.as_view(), name='edit_user_profile'),

    # path('add_article/', ArticleAdding.as_view(), name='add_article'),
    path('article/<slug:article_slug>/', ArticleDetail.as_view(), name='article'),
    path('category/<slug:category_slug>', ContentCategory.as_view(), name='category'),
    
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
