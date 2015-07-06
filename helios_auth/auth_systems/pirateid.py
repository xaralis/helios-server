"""
Yahoo Authentication

"""

from django.http import *
from django.core.mail import send_mail
from django.conf import settings

import sys, os, cgi, urllib, urllib2, re
from xml.etree import ElementTree

from openid import view_helpers
import json
import urllib2
import logging


# some parameters to indicate that status updating is not possible
STATUS_UPDATES = False

# display tweaks
LOGIN_MESSAGE = "Log in with my PirateID"
OPENID_ENDPOINT = 'https://openid.pirati.cz'

AX_REQUIRED_FIELDS = {
    'firstname' : 'http://axschema.org/namePerson/first',
    'lastname' : 'http://axschema.org/namePerson/last',
    'fullname' : 'http://axschema.org/namePerson',
    'email' : 'http://axschema.org/contact/email',
    'nickname' : 'http://axschema.org/namePerson/friendly'
}


def get_auth_url(request, redirect_url):
  request.session['pirateid_redirect_url'] = redirect_url
  url = view_helpers.start_openid(request.session, OPENID_ENDPOINT, redirect_url, redirect_url, ax_required_fields = AX_REQUIRED_FIELDS)
  return url

def get_user_info_after_auth(request):
  data = view_helpers.finish_openid(request.session, request.GET, request.session['pirateid_redirect_url'], ax_required_fields = AX_REQUIRED_FIELDS)

  return {'type' : 'pirateid', 'user_id': data['ax']['nickname'][0], 'name': data['ax']['fullname'][0], 'info': {'email': data['ax']['email'][0]}, 'token':{}}
    
def do_logout(user):
  """
  logout of Yahoo
  """
  return None
  
def update_status(token, message):
  """
  simple update
  """
  pass

def send_message(user_id, user_name, user_info, subject, body):
  """
  send email to yahoo user, user_id is email for yahoo and other openID logins.
  """
  send_mail(subject, body, settings.SERVER_EMAIL, ["%s <%s@pirati.cz>" % (user_name, user_id)], fail_silently=False)
  
def generate_constraint(category_id, user):
  return category_id

def eligibility_category_id(constraint):
  return constraint
import pprint
pp = pprint.PrettyPrinter(indent=4)
def check_constraint(constraint, user):
  """
  for eligibility
  """
  userinfo = json.load(urllib2.urlopen("https://graph.pirati.cz/user/" + user.user_id))
  id = userinfo[u'id']
  usergroups = json.load(urllib2.urlopen("https://graph.pirati.cz/" + id + "/groups"))
  for usergroup in usergroups:
    if usergroup[u'id'] == constraint:
      return True
  return False

def can_list_categories():
  """
  we will use phpbb groups
  """
  return True

def list_categories(user):
  """
  returns [{id,name},...]
  """
  categories = []
  groups = json.load(urllib2.urlopen("https://graph.pirati.cz/groups"))
  for group in groups:
    categories.append({'id': group[u'id'], 'name': group[u'username']})
  
  return categories
