CONFIGURATION

- Install requirements.txt

- Add "social_core" to INSTALLED_APPS django settings

- Add "social_django" to INSTALLED APPS django_settings

- Add "social_app_django_multitenant" to INSTALLED_APPS django settings

- Add SOCIAL_AUTH_STRATEGY = 'social_app_django_multitenant.strategy.DjangoMultiTenantStrategy' to django settings

- Add social auth backends to  django settings
  
  AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
  )

- Add social_auth_settings = JsonField() to your Tenant model

- Include this url to your main urls.py
  url('', include('social_app_django_multitenant.urls', namespace='social'))

- Add social auth settings with this format
  {
  	"linkedin-oauth2": {
  		"SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY": "",
  		"SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET": ""
  	},
  	"twitter": {
  		"SOCIAL_AUTH_TWITTER_KEY": "",
  		"SOCIAL_AUTH_TWITTER_SECRET": ""
  	},
    "SOCIAL_AUTH_PIPELINE": [
    	"social_core.pipeline.social_auth.social_details",
    	"social_core.pipeline.social_auth.social_uid",
    	"social_core.pipeline.social_auth.social_user",
    	"social_core.pipeline.user.get_username",
    	"social_core.pipeline.user.create_user",
    	"social_core.pipeline.social_auth.associate_user",
    	"social_core.pipeline.social_auth.load_extra_data",
    	"social_core.pipeline.user.user_details",
    	"social_core.pipeline.social_auth.associate_by_email"
    ],
    "SOCIAL_AUTH_LOGIN_REDIRECT_URL": "profile"
  }