class Datafinder:

    def __init__(self, soup):
        self._soup = soup

    def get_authors(self):
        authors = set()
        searches = [
                {'itemprop': 'author'}
                ]

        author_elements = []
        for s in searches:
            author_elements += self._soup.find_all(attrs=s)

        for el in author_elements:
            author = self._get_data_from_element(el)
            if (len(author.split()) > 1):
                authors.add(author)
        
        authors_list = list(authors)
        return authors_list

    def get_title(self):
        searches = [
                {'class': 'report-title'}
                ]

        for s in searches:
            el = self._soup.find(attrs=s)
            if (el is not None and self._get_data_from_element(el) is not ''):
                return self._get_data_from_element(el)
            titleStr = self._soup.title.string
            if(titleStr is not None):
                return titleStr
        return 'TITLE'

    def get_publication_date(self):
        searches = [
                {'itemprop': 'datePublished'}
                ]
        for s in searches:
            el = self._soup.find(attrs=s)
            if (el is not None):
                return self._get_data_from_element(el)

        return '[[[PUBLICATION DATE]]]'

    def get_content(self):
        matches = self._soup.findAll('p')
        body = []
        if (matches is not None):
            for match in matches:
                body.append(match.text)
            return body
        return 'BODY'

    def _get_data_from_element(self, el):
        try:
            return el['content']
        except KeyError:
            return el.text

