from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import  include, url
from django.contrib import admin
from mysite.views import home, portofolio, project_handler, academic_career,\
     contact, professional_career, anything, blog_list, \
    search, about_me, add_testimonial, achievement, blog_post

urlpatterns = [
    # Examples:
    # url(r'^$', 'PersonalWebsite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^portofolio/?$', portofolio),
    url(r'^portfolio/?$', portofolio),
    url(r'^abilities/?$', portofolio),
    url(r'^projects/([a-zA-Z0-9_]+)/?$', project_handler),
    url(r'^project/([a-zA-Z0-9_]+)/?$', project_handler),
    url(r'^career/?$', academic_career),
    url(r'^career/academic/?$', academic_career),
    url(r'^career/professional/?$', professional_career),
    url(r'^life_of_a_debugger/?$', blog_list),
    url(r'^blog/?$', blog_list),
    url(r'^blog/([a-zA-Z0-9_]+)/?$', blog_post),
    url(r'^life_of_a_debugger/([a-zA-Z0-9_]+)/?$', blog_post),
    url(r'^addtestimonial/?$', add_testimonial),
    url(r'^add_testimonial/?$', add_testimonial),
    url(r'^testimonial_add/?$', add_testimonial),
    url(r'^contact/?$', contact),
    url(r'^aboutme/?$', about_me),
    url(r'^about_me/?$', about_me),
    url(r'^achievements/?$', achievement),
    url(r'^search/?', search),
    url(r'^rajababu3_secret/admin/?', include(admin.site.urls)),
    url(r'^(.*)$', anything),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)