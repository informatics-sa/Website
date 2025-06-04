// -- Cookie Utils --
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

function checkValidLangCookie(name) {
    const cookieValue = getCookie(name);
    return (cookieValue !== null) && (cookieValue === 'ar' || cookieValue === 'en');
}
// -- End of Cookie Utils --


const LANG_COOKIE_NAME = 'lang';

const notMultiLingualPrefixes = [
    '/debug',
    '/data',
];

function redirectToLang(lang) {
    var curpath = window.location.pathname;
    if (lang === 'ar') {
        while (curpath.startsWith('/en')) {
            curpath = curpath.slice(3);
        }
        window.location.href = curpath;
    } else if (lang === 'en') {
        var noEnglish = false;
        notMultiLingualPrefixes.forEach(pref => {
            noEnglish |= curpath.startsWith(pref);
        });
        if (!noEnglish && !curpath.startsWith('/en')) {
            window.location.href = '/en' + curpath;
        }
    }
}

function switchLanguage(newlang) {
    setCookie(LANG_COOKIE_NAME, newlang);
    redirectToLang(newlang);
}

function getCurLang() {
    return window.location.pathname.startsWith('/en') ? 'en' : 'ar';
}

// main
if (!checkValidLangCookie(LANG_COOKIE_NAME)) {
    setCookie(LANG_COOKIE_NAME, getCurLang(), 71);
}

const cookieLang = getCookie(LANG_COOKIE_NAME);
if (cookieLang !== getCurLang()) {
    redirectToLang(cookieLang)
}

