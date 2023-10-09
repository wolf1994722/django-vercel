

# Django-Authentication-Login-Logout-Signup-Custom-User
Django Authentication – How to build Login/Logout/Signup for custom User

<strong>Database name</strong> : <i>atikgohel</i>
<p> you can change database name : DjangoAuth\settings.py line number 85 </p>

<p>Building user <a href="https://docs.djangoproject.com/en/2.1/topics/auth/">User authentication</a> is not easy, in almost case, it’s complicated. Fortunately, Django has a powerful built-in User authentication that helps us create our Authentication system fast. By default, the User model in Django <code>auth</code> app contains fields: username, password, email, first_name, last_name… However, using our own custom user model allows us deal with user profile more comfortably. For example, what if we want to add more fields: full_name or age?</p>

<p>In this tutorial, we’re gonna look at way to customize authentication in Django (version 3.1.7) using subclass of <code>AbstractBaseUser</code>: <code>AbstractUser</code>. All User authentication data will be stored in <strong>MySQL</strong> database that we’ll show you how to config the datasource.<p>

<h2  padding-bottom: .3em><span id="Django_Custom_Authentication_Project_overview" >Django Custom Authentication Project overview</span></h2>

We will build a Dajngo Project with Authentication app that has login/logout/signup with custom fields such as <strong>full name</strong> and <strong>age</strong>:

<img src="https://user-images.githubusercontent.com/65019876/113774104-787d9b00-9744-11eb-8db9-0b4dcaec4c72.png" width="930px" >

<p>We will code our custom <code>signup()</code> function, <code>login()</code> and <code>logout()</code> is automatically implemented by Django <code>auth</code>.</p>

All User data will be saved in MySQL/PostgreSQL database.

<h2><span id="Project_Structure">Project Structure</span></h2>

<p>Here is the folders and files structure that we will create in the next steps.</p>

<img src="https://user-images.githubusercontent.com/65019876/113776945-1888f380-9748-11eb-986f-d50a06be4d74.png" width="300" >

<p>
  Create a manually highlighted folder and file <br>
    1. authen\apps.py <br>
    2. authen\forms.py <br>
    3. static folder <br>
    4. static\css folder -> bootstrap.css  <br>
    5. static\js folder -> bootstrap.js <br>
    6. templates floder <br>
    7. templates\auth folder <br>
    8. templates\auth\base.html <br>
    9. templates\auth\index.html <br>
    10.templates\auth\login.html <br>
    11.templates\auth\signup.html <br> 
    
  <strong>! Go to the following link and copy and paste it It's just a bootstrap file !</strong>
  <br> – <a href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"><strong>bootstrap.css</strong></a>
  <br> – <a href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js"><strong>bootstrap.js</strong></a></p>

<h2><span id="Setup_Django_Custom_Authentication_Project">Setup Django Custom Authentication Project</span></h2>

<p>Create Django project named <strong>DjangoAuth</strong> with command:<br> <code>django-admin startproject DjangoAuth</code></p>

<p>
  Run following commands to create new Django App named <strong>authen</strong> inside the project:
  <br> – <code>cd DjangoAuth</code>
  <br> – <code>python manage.py startapp authen</code>
</p>

<p>Open <strong><em>authen\apps.py</em></strong>, we can see <code>AuthenConfig</code> class (subclass of the <code>django.apps.AppConfig</code>) that represents our Django app and its configuration:</p>
<pre> 
from django.apps import AppConfig
  
class AuthenConfig(AppConfig):
name; = 'authen'
</pre>

<p>Open <strong><em>settings.py</em></strong>, find <code>INSTALLED_APPS</code>, then add:</p>
<pre>
  INSTALLED_APPS = [
      ...
      'authen.apps.AuthenConfig',
  ]
</pre>

<h2><span id="Specify_Derectory" >Specify Derectory</span></h2>
<p><li><b>Specify template directory</b> </li></p>
<pre>
  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [os.path.join(BASE_DIR, 'templates')],
          'APP_DIRS': True,
          ...
      },
  ]
</pre>
  
<p><li><b>Specify static directory</b> </li></p>
<pre>
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]
</pre>

<h2><span id="Config_Django_project_to_work_with_database">Config Django project to work with database</span></h2>
<b id="MySQL_Database">• MySQL Database</b>
  <br><br>
<p id="Install_Import_Python_MySQL_Client">Install &amp; Import Python MySQL Client</p>

<p>We have to install Python MySQL Client to work with MySQL database.<br> In this tutorial, we use <strong>pymysql</strong>: <code>pip install pymysql</code>.</p>

<p>Once the installation is successful, import this module in <strong><em>DjangoAuth/__init__.py</em></strong>:</p>  

<pre>
import pymysql

pymysql.install_as_MySQLdb()
</pre>
  <br>
<b id="Setup_MySQL_Database_engine">• Setup MySQL Database engine</b>    <br><br>
<p>Open <strong><em>settings.py</em></strong> and change declaration of <code>DATABASES</code>:</p>
<pre>
  DATABASES = {
       'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'atikGohel',
          'USER' : 'root',
          'PASSWORD' : '',
          'HOST': 'localhost',
          'PORT' : '3306',
      }
  }
</pre>

<h2><span id="Create_Custom_User_Model">Create Custom User Model</span></h2>
<b><span id="Create_a_new_Custom_User_Model">• Create a new Custom User Model</span></b><br><br>
<p>
  In <em>authen/models.py</em>, create a new User model called <code>CustomUser</code> that extends <code>AbstractUser</code> (a subclass of <a href="https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser">AbstractBaseUser</a>), then add two custom fields: <code>full_name</code> and <code>age</code>:</p>
  
<pre>
  from django.db import models
  from django.contrib.auth.models import AbstractUser

  class CustomUser(AbstractUser):
      full_name = models.CharField(max_length=100, blank=False)
      age = models.PositiveIntegerField(null=True, blank=True)
</pre>

<p>
  <code>age</code> field uses both <code>null</code> and <code>blank</code>:<br> 
  – <code>null</code> is for database. <code>null=True</code> indicates that we can store it in database entry as <strong>NULL</strong> (no value).<br> 
  – <code>blank</code> is for validation. <code>blank=True</code> accepts empty value for the form field, so <code>blank=False</code> indicates that the value is required.
</p>
<br>

<b><span id="Specify_Custom_User_Model_in_settingpy">• Specify Custom User Model in setting.py</span></b><br>
<p>
  In <Strong>setting.py</strong>, we add <code>AUTH_USER_MODEL</code> config to specify our custom user model instead of Django built-in <code>User</code> model. The model is named <code>CustomUser</code> and exists within <code>authen</code> app, so we refer to it as <code>authen.CustomUser</code>:
</p>
  
<pre>
  AUTH_USER_MODEL = 'authen.CustomUser'
</pre>

<h2><span id="Create_a_new_form_for_UserCreationForm">Create a new form for UserCreationForm</span></h2>
<p>Now we create a new file in the authen app called forms.py:</p>
<pre>
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, help_text='Required. 100 charaters of fewer.')
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('full_name', 'age',)
</pre>

<p>Our <code>SignUpForm</code> extends the <code><a href="https://docs.djangoproject.com/en/2.1/topics/auth/default/#django.contrib.auth.forms.UserCreationForm"> UserCreationForm</a></code>.</p>

<p>We set <code>model</code> to <code>CustomUser</code> and use default fields by <code>Meta.fields</code> which includes all default fields (including username, first_name, last_name, email, password, groups…). We simply plus our custom fields (<code>full_name</code>, <code>age</code>) at the end and it will display automatically on signup page.</p>

<p>When a user signs up for a new account, the default form only asks for a <code>username</code>, <code>email</code>, and <code>password</code>. Now, it also requires <code>full_name</code> and <code>age</code>.</p>

<h2><span id="Activate_the_User_Model">Activate the User Model</span></h2>

<p>Now our new database model is created, we need to update Django in 2 steps:</p> 

<b><span id="Create_migration_file">• Create migration file</span></b><br>
<p>Run the command:<br> <code>python manage.py makemigrations authen</code></p>

<p>We can see output text:</p>
<pre>
  Migrations for 'authen':
  authen\migrations\0001_initial.py
    - Create model CustomUser
</pre>

<p>It indicates that the <strong>authen/migrations/0001_initial.py</strong> file includes code to create CustomUser data model:</p>

<pre>
# Generated by Django 3.1.7 on 2021-04-06 18:05

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

  initial = True

  dependencies = [
    ('auth', '0012_alter_user_first_name_max_length'),
    ]

  operations = [
      migrations.CreateModel(
          name='CustomUser',
          fields=[
              ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
              ('password', models.CharField(max_length=128, verbose_name='password')),
              ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
              ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
              ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
              ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
              ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
              ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
              ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
              ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
              ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
              ('full_name', models.CharField(max_length=100)),
              ('age', models.PositiveIntegerField(blank=True, null=True)),
              ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
              ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
          ],
          options={
              'verbose_name': 'user',
              'verbose_name_plural': 'users',
              'abstract': False,
          },
          managers=[
              ('objects', django.contrib.auth.models.UserManager()),
          ],
      ),
    ]

 </pre>
 
<p>The generated code defines a subclass of the <code>django.db.migrations.Migration</code>. It has an operation for creating <code>CustomUser</code> model table. Call to <code>migrations.CreateModel()</code> method will create a table that allows the underlying database to persist the model.</p>

<p>You can see that we have not only user default fields but also custom fields (<code>full_name</code>, <code>age</code>).</p>

<b><span id="Generate_database_table">• Generate database table</span></b><br>

<p>Run the following Python script to apply the generated migration:<br> <code>python manage.py migrate</code></p>
<p>The output text:</p>
<pre> 
Operations to perform:
  Apply all migrations: admin, auth, authen, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK        
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK

</pre>
<p>
  A warning may come to you, ignore it 👇👇
</p>
<pre>
System check identified some issues:

WARNINGS:
?: (mysql.W002) MariaDB Strict Mode is not set for database connection 'default'
        HINT: MariaDB's Strict Mode fixes many data integrity problems in MariaDB, such as data truncation upon insertion, by escalating warnings into errors. It is strongly recommended you activate it. See: https://docs.djangoproject.com/en/3.1/ref/databases/#mysql-sql-mode     
Operations to perform:
  Apply all migrations: admin, auth, authen, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK        
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
</pre>

<p>Check MySQL Database, for example, now we can see that a table for CustomUser model was generated and it’s named <code>authen_customuser</code>:</p>

<img src="https://user-images.githubusercontent.com/65019876/113788162-0fa11d80-975a-11eb-85af-3813d52ad199.png" width="308"> <span>
<img src="https://user-images.githubusercontent.com/65019876/113788325-4e36d800-975a-11eb-9cdf-6a750943a9b3.png" width="620"> </span>
  
<h2><span id="Set_urlpatterns_038_handle_signuploginlogout_requests">Set urlpatterns &amp; handle signup/login/logout requests</span></h2>

<b><span id="Set_url_patterns">• Set url patterns</span></b><br>
<p>Open the project-level <em>DjangoAuth\urls.py</em> file</p>

<pre>
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authen.urls')),
]
</pre>

<p>Open the app-level <em>authen\urls.py</em> file, we’re gonna use built-in <code>django.contrib.auth</code> module to handle login/logout requests:</p>

<pre>
from django.urls import path
from django.contrib.auth import views as auth_views
from authen import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name="signup")
]
</pre>

<p> Using <code>auth_views.LogoutView</code> helps us handle logout request automatically, we only need to call <code>{% url 'logout' %}</code> where we want to make logout event in the HTML template. </p>

<p>The next step is to specify where to redirect the user upon a successful login/logout.<br> Open project <strong><em>setting.py</em></strong>, then set values for <code>LOGIN_REDIRECT_URL</code> and <code>LOGOUT_REDIRECT_URL</code>:</p>

<pre> 
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
</pre>

<p>Now, after login/logout, if we don’t indicate where to come, the user will be redirected to the <code>'home'</code> template which is our homepage.</p>

<b><span id="Custom_signup_request">• Custom signup request</span></b><br>

<p>Inside <strong><em>authen/views.py</em></strong>, define functions for handling signup request and homepage:</p>

<pre>
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def home(request):
    return render(request, 'auth/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', { 'form' : form })
</pre>

<p>Now we dive into <code>signup()</code> function. It gets user data from HTTP <strong>POST</strong> request which is handled by <code>SignUpForm</code>, save user to database.</p>

<p>Then we use <code>authenticate()</code> function and <code>login()</code> function from <code>django.contrib.auth</code> to log the user in.</p>

<p>If the process is successful, redirect to homepage, otherwise, return to <code>signup.html</code> template.</p>


<h2><span id="Edit_or_Create_Django_template_for_User_Authentication"\>Edit or Create Django template for User Authentication</span></h2>

<b><span id="Edite_or_Create_Homepage_template">• Edit or Create base.html</span></b><br>

<p>In <strong>templates\auth</strong> folder, edit or  create new HTML file named <strong><em>base.html</em></strong>:</p>

<p>The most powerful – and thus the most complex – part of Django’s template engine is template inheritance. Template inheritance allows you to build a base “skeleton” template that contains all the common elements of your site and defines blocks that child templates can override.</p>

<p>it's  template inheritance</p>

<pre> <code>
  &lt;!DOCTYPE html&gt; {% load static %}
  &lt;html lang="en"&gt;
  &lt;head&gt;
      &lt;meta charset="UTF-8"&gt;
      &lt;meta http-equiv="X-UA-Compatible" content="IE=edge"&gt;
      &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
      &lt;title&gt; {% block title %}{% endblock title %} | Atik Gohel &lt;/title&gt;
      &lt;link rel="stylesheet" href="{% static 'css/bootstrap.css'%}"&gt;
  &lt;/head&gt;
  &lt;body&gt;
      &lt;div class="container mt-5"&gt;
          &lt;h3 class="text-center alert alert-danger"&gt; Login and Singup Example &lt;/h3&gt;
      &lt;/div&gt;
      {% block body %}{% endblock body %}
      &lt;script src=" {% static 'js/bootstrap.js' %}"&gt; &lt;/script&gt;
  &lt;/body&gt;
  &lt;/html&gt;
  </code>
</pre>

<b><span id="Edite_or_Create_Homepage_template">• Edit or Create home.html</span></b><br>

<p>We’re gonna use Django built-in <a href="https://docs.djangoproject.com/en/2.1/ref/templates/builtins/#url" target="_blank" rel="nofollow noopener noreferrer">url templatetag</a> to create links for login/logout/signup requests.</p>

<p>In <strong>templates\auth</strong> folder, edit or  create new HTML file named <strong><em>home.html</em></strong>:</p>

<pre> <code>
  {% extends 'auth/base.html' %}
  {% block title %}Home{% endblock title %}

  {% block body %}

    &lt;div class="container"&gt;
      &lt;div class="row"&gt;
          &lt;div class="clo-12"&gt;
              &lt;div class="alert alert-info"&gt;this is home page&lt;/div&gt;

              {% if user.is_authenticated %} 

                  Hi {{ user.full_name }}, Welcome to My site!
                  &lt;a href="logout/" class="btn btn-danger"&gt;Logout&lt;/a&gt; 

              {% else %}

                  You are not logged in!
                  &lt;br&gt;
                  &lt;a href="{% url 'login' %}" class="btn btn-primary mt-3"&gt;
                      Log In
                  &lt;/a&gt;
                  &lt;a href="{% url 'signup' %}" class="btn btn-primary mt-3"&gt;
                      SignUp
                  &lt;/a&gt;

              {% endif %}
          &lt;/div&gt;
      &lt;/div&gt;
  &lt;/div&gt;

  {% endblock body %}
  </code>
</pre>

<p>If you use <code> {% extends %} </code>in a template, it must be the first template tag in that template. Template inheritance won’t work, otherwise.
<br><strong>{% block title %}{% endblock title %}</strong> it is title block
<br><strong>{% block body %}{% endblock body %}</strong> it is title block</p>

<p>We can use <code>is_authenticated</code> attribute to specify whether the user is logged in or not, then show his full name for a website greeting.</p>

<p>So, when user aren’t logged in, it looks like:</p>
<img src="https://user-images.githubusercontent.com/65019876/113792927-b7bbe400-9764-11eb-91ef-ab6c26166250.png" > 

<b><span id="Edit_or_Create_Django_custom_Signup_template">• Edit or Create Django custom Signup.html</span></b><br>

<p>
  – We’re gonna use HTML <code>&lt;form&gt;</code> tag with HTTP POST method.<br>
  – We add <code>{% csrf_token %}</code>to protect our form from cross-site scripting attacks.
</p>

<p>In <strong>templates\auth</strong> folder, edit or  create new HTML file named <strong><em>signup.html</em></strong>:</p>

<pre>
  {% extends 'auth/base.html' %}
  {% block title %}Singup{% endblock title %} 
  {% block body %}
  &lt;div class="container"&gt;
      &lt;div class="row"&gt;
          &lt;div class="clo-12"&gt;
              &lt;div class="alert alert-info"&gt;this is Singup page&lt;/div&gt;
              &lt;a href="{% url 'home' %}" class="btn btn-primary mt-3"&gt;Home&lt;/a&gt;
              &lt;a href="{% url 'login' %}" class="btn btn-primary mt-3"&gt;Login&lt;/a&gt;
              &lt;br&gt;
              &lt;form method="post"&gt;
                  {% csrf_token %}
                  {% for field in form %}
                  &lt;p&gt;
                      {{ field.label_tag }}&lt;br&gt;
                      {{ field }}
                      {% if field.help_text %}
                          &lt;small style="color: green"&gt;{{ field.help_text }}&lt;/small&gt;
                      {% endif %}
                      {% for error in field.errors %}
                          &lt;/p&gt;&lt;p style="color: red"&gt;{{ error }}&lt;/p&gt;
                      {% endfor %}
                  &lt;p&gt;&lt;/p&gt;
                  {% endfor %}
                  &lt;button type="submit" class="btn btn-primary mt-3"&gt;Sign up &lt;/button&gt;
              &lt;/form&gt;
          &lt;/div&gt;
      &lt;/div&gt;
  &lt;/div&gt;

  {% endblock body %}
</pre>

<p>it looks like:</p>

<img src="https://user-images.githubusercontent.com/65019876/113793196-56484500-9765-11eb-8b1b-8b037a328fad.png" > 

<b><span id="Edite_or_Create_Django_custom_Login_template">• Create Django custom login.html</span></b><br>

<p>In <strong>templates\auth</strong> folder, edit or  create new HTML file named <strong><em>login.html</em></strong>:</p>

<pre>
{% extends 'auth/base.html' %} 
{% block title %}Login{% endblock title %} 

{% block body %}

&lt;div class="container"&gt;
    &lt;div class="row"&gt;
        &lt;div class="clo-12"&gt;

            &lt;div class="alert alert-info"&gt;this is Login page&lt;/div&gt;
            
            &lt;a href="{% url 'home' %}" class="btn btn-primary mt-3"&gt;Home&lt;/a&gt;
            &lt;a href="{% url 'signup' %}" class="btn btn-primary mt-3"&gt;SignUp&lt;/a&gt;
            &lt;br&gt;&lt;br&gt;&lt;br&gt;
            &lt;form method="post"&gt;
                {% csrf_token %}
                {{ form.as_p }}
                &lt;button type="submit" class="btn btn-primary mt-3"&gt;Login&lt;/button&gt;
            &lt;/form&gt;
            
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/div&gt;

{% endblock body %}

</pre>

<p>We use <code>{{ form.as_p }}</code> to render it within paragraph <code>&lt;p&gt;</code> tags.<br> It looks like:</p>

<img src="https://user-images.githubusercontent.com/65019876/113795530-c4dbd180-976a-11eb-9714-503b2b37f1c2.png">

<h2><span id="Run_038_Check_results">Congratulations &amp; Now Run Progrma</span></h2>

<p>– Run Django project with command:<br> <code>python manage.py runserver</code></p>

<p>– Open browser with url <code>http://localhost:8000/</code>, then go to <code>/signup</code> page and fill your information:</p>

<img src="https://user-images.githubusercontent.com/65019876/113795942-a75b3780-976b-11eb-91a7-494d3c6d0d3f.png">

<p>Click on <strong>Sign up</strong> Button, if the process is sucessful, the browser will turn into <code>/home</code> page with your information:</p>

<img src="https://user-images.githubusercontent.com/65019876/113796043-ea1d0f80-976b-11eb-83a2-0b87caebf60c.png">

<p>Click on <strong>Log out</strong> and see the result:</p>

<img src="https://user-images.githubusercontent.com/65019876/113796108-159ffa00-976c-11eb-9749-d123eaf0163f.png">

<p>Go to <code>/login</code> page and fill <em>Username</em> and <em>Password</em>:</p>

<img src="https://user-images.githubusercontent.com/65019876/113796198-4b44e300-976c-11eb-9efb-03a2f40db6ce.png">

<p>Click on <strong>Login</strong> to check authentication.</p>

<p>Now check MySQL database:</p>

<img src="https://user-images.githubusercontent.com/65019876/113796430-d9b96480-976c-11eb-8a3c-e81a62b69854.png">


<h2><span id="Source_Code">Source Code</span></h2>

<p>🙌 you can Download Source code 🙌</p>
<br>
<span >By <a class="url fn n" href="github.com/atik-gohel">Atik Gohel</a> | April 7, 2021.</span>




    
    
    
