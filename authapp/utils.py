
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_request_info(request):
    device = ''
    ip = get_client_ip(request)

    if request.user_agent.is_mobile:
        device = 'Mobile'
    elif request.user_agent.is_tablet:
        device = 'Tablet'
    elif request.user_agent.is_pc:
        device = 'PC'
    elif request.user_agent.is_bot:
        device = "Bot"

    if request.user_agent.is_touch_capable:
        device += '-Touch'
    if request.user.is_anonymous:
        current_user = None
    else:
        current_user = request.user
    device_family = request.user_agent.device.family  # returns 'iPhone'
    browser = request.user_agent.browser.family  # returns 'Mobile Safari'
    operating_system = f'{request.user_agent.os.family}({request.user_agent.os.version_string})'
    return f'device: {device}, device_family: {device_family}, browser: {browser}, os: {operating_system}, user: {current_user}, ip: {ip}'


def request_from_pc(request):
    """Check if request is coming from pc or not"""
    os_version = request.user_agent.os.version_string
    os_version = int(os_version) if os_version.isdigit() else 0
    
    browser = request.user_agent.browser.family
    print(browser)
    if 'Chrome' not in browser:
        return {
            'success': False,
            'reason': 'Please use Chrome browser!',
        }
    
    if not request.user_agent.is_pc or request.user_agent.os.family != 'Windows' or os_version < 7:
        return {
            'success': False,
            'reason': 'Please use your computer!',
        }
    return {
        'success': True,
        'reason': '',
    }