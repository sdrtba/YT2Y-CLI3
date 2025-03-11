import os
import sys

from cookies import check_cookies, save_cookies
from download import download
from transfer import set_kind, set_token, check_kind, check_token

def main() -> None:
    os.makedirs('etc', exist_ok=True)

    save_cookies() if '--set-cookies' in sys.argv else check_cookies()

    set_token() if '--set-token' in sys.argv else check_token()

    set_kind() if '--set-kind' in sys.argv else check_kind()

    download()

if __name__ == '__main__':
    main()
