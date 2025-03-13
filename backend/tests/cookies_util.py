import http.cookies

def get_all_cookies(response):
    all_cookies = {}
    for cookies in response.headers.getlist("Set-Cookie"):
        cookie = http.cookies.SimpleCookie()
        cookie.load(cookies)
        for key, morsel in cookie.items():
            all_cookies[key] = morsel.value

    if len(all_cookies) == 0:
        return None
    
    return all_cookies
