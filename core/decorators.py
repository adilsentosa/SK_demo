
import re
from xml.etree import ElementInclude
from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('you are not authorized to view this page')
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
                
        if group == 'pegawai':
            return redirect('userpage_pegawai')
        
        if group == 'walisiswa':
            return redirect('userpage_walisiswa')
        
        if group == 'siswa':
            return redirect('userpage_walisiswa')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
            
       
    return wrapper_function



