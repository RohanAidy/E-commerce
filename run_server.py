#!/usr/bin/env python
"""
Custom run server script to avoid port conflicts
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Import settings to get the port
django.setup()
from django.conf import settings

def main():
    """Run the development server on a custom port"""
    port = getattr(settings, 'RUNSERVER_PORT', 8001)
    print(f"🚀 Starting Books Store on port {port}")
    print(f"📚 Visit: http://127.0.0.1:{port}/")
    
    # Run the server with custom port
    execute_from_command_line(['manage.py', 'runserver', f'127.0.0.1:{port}'])

if __name__ == '__main__':
    main()
