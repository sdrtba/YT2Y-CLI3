from browser_cookie3 import ChromiumBased
from browser_cookie3 import _genarate_nix_paths_chromium, _genarate_win_paths_chromium

class Yandex(ChromiumBased):
    """Class for Yandex Browser"""

    def __init__(self, cookie_file=None, domain_name="", key_file=None):
        args = {
            'linux_cookies': _genarate_nix_paths_chromium(
                [
                    '~/.config/yandex-browser{channel}/Default/Cookies',
                    '~/.config/yandex-browser{channel}/Profile */Cookies',
                    "~/.var/app/ru.yandex.Browser/config/yandex-browser{channel}/Default/Cookies",
                    "~/.var/app/ru.yandex.Browser/config/yandex-browser{channel}/Profile */Cookies",
                ],
                channel=['', '-beta', '-dev']
            ),
            'windows_cookies': _genarate_win_paths_chromium(
                [
                    'Yandex\\YandexBrowser{channel}\\User Data\\Default\\Cookies',
                    'Yandex\\YandexBrowser{channel}\\User Data\\Default\\Network\\Cookies',
                    'Yandex\\YandexBrowser{channel}\\User Data\\Profile *\\Cookies',
                    'Yandex\\YandexBrowser{channel}\\User Data\\Profile *\\Network\\Cookies'
                ],
                channel=['', ' Beta', ' Dev']
            ),
            'osx_cookies': _genarate_nix_paths_chromium(
                [
                    '~/Library/Application Support/Yandex/YandexBrowser{channel}/Default/Cookies',
                    '~/Library/Application Support/Yandex/YandexBrowser{channel}/Profile */Cookies'
                ],
                channel=['', ' Beta', ' Dev']
            ),
            'windows_keys': _genarate_win_paths_chromium(
                'Yandex\\YandexBrowser{channel}\\User Data\\Local State',
                channel=['', ' Beta', ' Dev']
            ),
            'os_crypt_name': 'chromium',
            'osx_key_service': 'Yandex Safe Storage',
            'osx_key_user': 'Yandex'
        }
        super().__init__(browser='Yandex', cookie_file=cookie_file,
                         domain_name=domain_name, key_file=key_file, **args)

def yandex(cookie_file=None, domain_name="", key_file=None):
    """Returns a cookiejar of the cookies used by Yandex Browser. Optionally pass in a
    domain name to only load cookies from the specified domain
    """
    return Yandex(cookie_file, domain_name, key_file).load()
