from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.conf import settings
from mysite.models import project, message,\
  error_404_visit, testimonial, blog
import os

#Function to get IP Address of the request
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def record_visit(request, page):
#     normal_visit.new_visit(get_client_ip(request), page, request.META.get('HTTP_USER_AGENT'))
#     return normal_visit.unique_visit(page)


def search(request) :
    return render(request, 'search.html', {})
#Function to handle the home-page
def home(request):

    context = {
        'page' : 'home',
        'testimonial_list' : testimonial.objects.filter(approved=True),
    }

    return render(request, 'index.html', context)

#Function to handle past-project page
def portofolio(request):

    #Fetch all projects from database and load in context
    context = {
        'page' : 'portofolio',
        'project_list' : project.objects.filter(display_rank__gt=0).order_by('display_rank'),
    }

    return render(request, 'portofolio.html', context)

#Function to display project details
def project_handler(request, name):

    #Fetch project details from database
    try:
        proj = project.objects.get(folder = name, display_rank__gt=0)
        temp = os.path.join(os.path.join(settings.STATICFILES_DIRS[0], 'images'), 'projects')
        images_folder = os.path.join(temp, name)

        images = []

        for image in os.listdir(images_folder):
            images.append('images/projects/' + name + '/' + image)



        context = {
            'page' : 'portofolio',
            'project' : proj,
            'images' : images,

        }

        return render(request, name + '.html', context)

    except ObjectDoesNotExist:

        error_404_visit.record_error(get_client_ip(request),
            request.META.get('HTTP_USER_AGENT'),'project/' + name)

        context = {
            'message' : '''<h1>I have no knowledge about this project ! </h1>
                <h3 class="subheader"> <a href="/portofolio">Click here</a>
                to view all my projects ! </h3>''',
            'visitors' : 'Error'
        }

        return render(request, 'error.html', context)

    except OSError:

      error_404_visit.record_error(get_client_ip(request),
            request.META.get('HTTP_USER_AGENT'),'project/' + name)

      context = {
            'message' : '''<h1>Page Currently Unavailable! </h1>
                <h3 class="subheader">The page is being updated ! Check back later !</h3>
                <h3 class="subheader"> <a href="/portofolio">Click here</a>
                to view all my projects ! </h3>''',
            'visitors' : 'Error'
        }

      return render(request, 'error.html', context)

#View to handle Academic Career Page
def academic_career(request):

    sgpa = [73.16, 74.45, 74.77, 71.12]


    semwise = []
    for i in range(len(sgpa)):
        temp = []
        temp.append(sgpa[i])
        semwise.append(temp)

    course_left = [
        'Data Structures and Algorithms',
        'Unix System Programming*',
        'Data Structures and Algorithms Lab',
        'Graph Theory, Probability and Statistics',
        'Operating Systems',
        'Computer Networks 1 and 2*',
        'Design and Analysis of Algorithms',
        'Machine Learning and Data Science * (Learning from Udemy)'
    ]

    course_right = [
        'Database Management Systems',
        'Web Technologies and Applications**',
        'Finite Automata ',
        'Software Engineering',
        'Management and Entrepreneurship',
        'Linear Algebra and Matrices',
        'File Structure*',
        'Operational Research*'

    ]

    context = {
        'page' : 'career',
        'semwise' : semwise,
        'cgpa' : 73.37,
        'course_left' : course_left,
        'course_right' : course_right,
    }

    return render(request, 'academic_career.html', context)

def professional_career(request):

    context = {
        'page' : 'career',
    }

    return render(request, 'professional_career.html', context)

#View To Handle 404 Errors
def anything(request, path):

    error_404_visit.record_error(get_client_ip(request), request.META.get('HTTP_USER_AGENT'), path)

    context = {
        'message' : '<h1>The page doesn\'t seem to exist !</h1>',
        'visitors' : 'Error'
    }
    return render(request, 'error.html', context)


#View to Render the Blog
def blog_list(request):

    context = {
        'page' : 'blog',
        'post_list' : blog.objects.order_by('-time_added'),
    }
    return render(request, 'blog.html', context)

#View to handle the contact page
def contact(request):

    context = {
        'page' : 'contact'
    }

    if 'submit' in request.POST:
        msg = message(name=request.POST['name'], email=request.POST['email'],
            message=request.POST['message'], ip=get_client_ip(request))
        msg.save()
        context.update({'message' : 'Your message was recorded ! You will hear from me ASAP :)', 'messagetype' : 'success'})

    context.update(csrf(request))
    return render(request, 'contact.html', context)

def about_me(request):

    return render(request, 'aboutme.html', {
        'page' : 'aboutme'
    })

def achievement(request):

    return render(request, 'achievements.html', {

        'page' : 'achievements'
    })

def add_testimonial(request):

    context = {

    }
    context.update(csrf(request))

    if 'submit' in request.POST:
        test = testimonial(
            author = request.POST['author'],
            email = request.POST['email'],
            conection = request.POST['connection'],
            ip = get_client_ip(request),
            content = request.POST['content']
        )

        test.save()
        context.update({'message' : 'Your Testmonial has been successfully submitted for Approval !'})

    return render(request, 'add_testimonial.html', context)

def blog_post(request, post_name):

    try:
        post = blog.objects.get(template_file=post_name)

        context = {
            'page' : 'blog',
            'post' : post,

        }

        return render(request, os.path.join('blog', post_name) + '.html', context)

    except ObjectDoesNotExist:

        error_404_visit.record_error(get_client_ip(request),
            request.META.get('HTTP_USER_AGENT'),'project/' + post_name)

        context = {
            'message' : '''<h1>I have not posted any such article ! </h1>
                <h3 class="subheader"> <a href="/blog">Click here</a>
                to view all my post ! </h3>''',
            'visitors' : 'Error'
        }

        return render(request, 'error.html', context)

    except OSError:

      error_404_visit.record_error(get_client_ip(request),
            request.META.get('HTTP_USER_AGENT'),'project/' + post_name)

      context = {
            'message' : '''<h1>Page Currently Unavailable! </h1>
                <h3 class="subheader">The page is being updated ! Check back later !</h3>
                <h3 class="subheader"> <a href="/blog">Click here</a>
                to view my blog ! </h3>''',
            'visitors' : 'Error'
        }

      return render(request, 'error.html', context)

def add_stuff(request):

    project.objects.all().remove()

    p = project(name = '')
    p.tag = ""
    p.folder = ""
    p.main_image = ""
    p.style = project.COURSE
    p.alt_text = ""
    return HttpResponse("Added Stuff To Database Successfully")
