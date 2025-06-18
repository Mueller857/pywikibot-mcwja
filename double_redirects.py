import pywikibot
from pywikibot import pagegenerators

def main():
    site = pywikibot.Site()
    redirects = pagegenerators.RedirectFilterPageGenerator(
        pagegenerators.AllpagesPageGenerator(),
        no_redirects=False
        )
    for page in redirects:
        if page.isRedirectPage():
            target = page.getRedirectTarget()
            if target.isRedirectPage():
                double_target = target.getRedirectTarget()
                page.set_redirect_target(double_target, keep_section=True, save=True, summary='二重リダイレクト')


if __name__ == '__main__':
    main()