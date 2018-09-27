from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]')
class UserManager(models.Manager):

# ========== Validation and Register ================================
   def validate_and_create_user(self, form):
       errors = []
       if len(form['name']) < 3:
           errors.append("Name must be at least 3 characters long.")

       if len(form['username']) < 3:
           errors.append("Username must be at least 3 characters long.")

       if len(form['password']) < 8:
           errors.append("Password must be at least 8 characters.")

       if not form['password'] == form['re-password']:
           errors.append("Password and Confirmation doesn't match. ")



       users_list = users.objects.filter(username=form['username'])
       # if len(users_list) > 0:
       #     errors.append('Username already in use')

       try:
           user = self.get(username=form['username'])
           errors.append("Username already in use")
           return (False, errors)
       except:
           if len(errors) > 0:
               return (False, errors)
           else:
               pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
               user = self.create(name=form['name'], username=form['username'], dateHired=form['dateHired'], password=pw_hash)
               return (True, user)

   # ========== Validation and Login ================================
   def validate_and_login(self, form):
       errors = []
       try:

           user = self.get(username = form['username'])

           if bcrypt.checkpw(form['password'].encode(), user.password.encode()):
               return (True, user)
           else:
               errors.append('Incorrect username or password')
               return (False, errors)
       except:
           errors.append('Incorrect username or password')
           return (False, errors)



# ========== Validation and AddItem ================================
   def validate_and_add_item(self, request):
       errors = []
       if len(request.POST['item']) < 1:
           errors.append("ERROR : Item/Product is empty.")

       if len(request.POST['item']) < 3:
           errors.append("Item/Product must be at least 3 characters long.")
       if len(errors) > 0:
           return (False, errors)
       else:
           this_user=users.objects.get(id=request.session['id'])
           wishlist=this_user.wishitem.create(item=request.POST['item'])
           this_user.all_items.add(wishlist)
           # wishlist = self.create(item=request.POST['item'])
           # wishlist.all_items.add(this_user)
           return (True, wishlist)

# ======  Create your models here.=========================
class users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=500)
    dateHired = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class wishlist(models.Model):
    curr_user = models.ForeignKey(users, related_name="wishitem")
    all_users = models.ManyToManyField(users, related_name="all_items")
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
