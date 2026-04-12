from HclsWebApi.models import CheckLogin

def admin_context(request):
    """Adds `admin_name`, `admin_username`, and `admin_email` to template context when logged in via session."""
    admin_id = request.session.get('admin_id')
    if not admin_id:
        return {}

    try:
        admin = CheckLogin.objects.get(id=admin_id)
        return {
            'admin_name': getattr(admin, 'username', '') or getattr(admin, 'email', ''),
            'admin_username': getattr(admin, 'username', ''),
            'admin_email': getattr(admin, 'email', ''),
        }
    except CheckLogin.DoesNotExist:
        return {}
