from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, render_to_response

from website.forms import HelpRequestForm
from customers.models import *


