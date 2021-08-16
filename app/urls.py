from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='home'),
    path('auth/login/', view=views.customerlogin, name='login'),
    path('auth/logout/', view=views.logOut, name='logout'),
    path('auth/signup/', view=views.signup, name='signup'),
    path('auth/verify-account/', view=views.verify_email_with_otp, name='verifyOtp'),
    path('dashboard/', view=views.dashboard, name='dashboard'),
    path('intents/', view=views.addIntents, name='addIntents'),
    path('train-bot/', view=views.trainBot, name='trainBot'),
    path('chat-bot/', view=views.getMessage, name="chat-bot")
]
