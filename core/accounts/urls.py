from django.urls import path , include

app_name = "accounts"

urlpatterns = [
    path("api/v1/", include("accounts.api.v1.urls"), name="accounts_api")
]
