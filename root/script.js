function setCookie(name, value, daysToExpire) {
    let expires = "";
    if (daysToExpire) {
        const date = new Date();
        date.setTime(date.getTime() + (daysToExpire * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(nameEQ) === 0) {
            return cookie.substring(nameEQ.length, cookie.length);
        }
    }
    return null;
}

function deleteCookie(name) {
    document.cookie = name + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function checkCookie(name) {
    return getCookie(name) !== null;
}

const LANG_COOKIE_NAME = 'lang';
function getCurLang() {
    return window.location.pathname.startsWith('/en') ? 'en' : 'ar';
}
function switchLanguage(newlang) {
    setCookie('lang', newlang);
    const curpath = window.location.pathname;
    window.location.href = (newlang == 'ar' ? ('/en' + curpath) : curpath.slice(3));
}

function checkRedirection() {
    const curlang = window.location.pathname.startsWith('/en') ? 'en' : 'ar';
    if (!checkCookie('lang')) {
        setCookie('lang', curlang);
    } else {
        if (getCookie('lang') == 'en' && )
    }
}