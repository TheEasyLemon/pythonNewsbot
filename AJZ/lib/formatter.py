import re

class CitationFormatter(object):

    def format(citation):
        raise NotImplementedError("Citation format not implemeted")

class PolicyFormatter(CitationFormatter):
    def format(self, citation):
        format = self._get_format()

        return format % (
            self._assemble_tag_authors(citation.authors),
            self._format_year(citation.publication_date, citation),
            self._assemble_authors(citation.authors),
            self._format_pubdate(citation.publication_date, citation),
            citation.title,
            citation.url,
            self._format_accessdate(citation.access_date)
            )

    def _get_format(self):
        #return "%s (%s). %s. Retrieved %s, from %s"
        return '%s %s [%s; %s; "%s"; %s; %s; --RB and DR]'
        # lastname year [full name; title; date; url; access date; --RB]

    def _get_author_format(self, authors):
        if (len(authors) == 0):
            return "AUTHORS"
        elif (len(authors) == 1):
            return "%s"
        elif (len(authors) == 2):
            return "%s, & %s"
        else:
            format_string = "%s, " * (len(authors)-1)
            return format_string + "& %s"

    def _assemble_authors(self, authors):

        formatted_names = set()

        for a in authors:
            first_last = a.split()
            if (len(first_last) > 1):
                # This pulls the first and last name
                formatted_names.add(first_last[0] + ' ' + first_last[1])

        authors = list(formatted_names)
        if (len(authors) < 1):
            string = "AUTHORS"
            print('Enter author')
            string = input()
            return string

        authors.sort()

        formatted_authors = self._get_author_format(authors) % tuple(authors)
        return formatted_authors

    def _assemble_tag_authors(self, authors):
        names = self._assemble_authors(authors)
        if names is "AUTHORS":
            return names
        names = names.split()
        lastnames = ""
        for x in range(int(len(names)/2)):
            lastnames+=names[2*x+1] + " "
        return lastnames
           
    def _regex_date(self, citation):
         dateRegex = re.compile(r'(\d\d)?\d\d((/|-)\d\d){1,2}(\d\d)?')
         mo = dateRegex.search(citation.url)
         if mo is not None:
             return mo.group()
         return "ND"

    def _format_pubdate(self, date, citation):
        if (date is not None):
            return date.strftime("%Y, %B %d")
        else:
            return self._regex_date(citation)
    
        
    def _format_year(self, date, citation):
        if(date is not None):
            return date.strftime("%y")
        else:
            dateStr = self._regex_date(citation)
            if dateStr is not "ND":
                yearStr = re.compile(r'(\d){4}').search(dateStr).group()
                return yearStr[2:]
            return "ND"

    def _format_accessdate(self, date):
        if (date is not None):
            return date.strftime("%B %d, %Y")
        else:
            return "[[[ACCESS DATE]]]"

class ExtempFormatter(CitationFormatter):
    def format(self, citation):
        format = self._get_format()

        return format % (
            self._assemble_authors(citation.authors),
            self._format_pubdate(citation.publication_date),
            citation.title,
            self._format_accessdate(citation.access_date),
            citation.url, self._get_data_from_element
            )

    def _get_format(self):
        return "%s (%s). %s. Retrieved %s, from %s. %s"

    def _get_author_format(self, authors):
        if (len(authors) == 0):
            return "[[[AUTHORS]]]"
        elif (len(authors) == 1):
            return "%s"
        elif (len(authors) == 2):
            return "%s, & %s"
        else:
            format_string = "%s, " * (len(authors)-1)
            return format_string + "& %s"

    def _assemble_authors(self, authors):

        formatted_names = set()

        for a in authors:
            first_last = a.split()
            if (len(first_last) > 1):
                # This pulls the last name and first initial
                formatted_names.add(first_last[1] + ", " + first_last[0][0] + ".")

        authors = list(formatted_names)
        if (len(authors) < 1):
            return "[[[AUTHORS]]]"

        authors.sort()

        formatted_authors = self._get_author_format(authors) % tuple(authors)
        return formatted_authors

    def _format_pubdate(self, date):
        if (date is not None):
            return date.strftime("%Y, %B %d")
        else:
            return "[[[PUBLICATION DATE]]]"

    def _format_accessdate(self, date):
        if (date is not None):
            return date.strftime("%B %d, %Y")
        else:
            return "[[[ACCESS DATE]]]"


class APAFormatter(CitationFormatter):

    def format(self, citation):
        format = self._get_format()

        return format % (
            self._assemble_authors(citation.authors),
            self._format_pubdate(citation.publication_date),
            citation.title,
            self._format_accessdate(citation.access_date),
            citation.url
            )

    def _get_format(self):
        return "%s (%s). %s. Retrieved %s, from %s"

    def _get_author_format(self, authors):
        if (len(authors) == 0):
            return "[[[AUTHORS]]]"
        elif (len(authors) == 1):
            return "%s"
        elif (len(authors) == 2):
            return "%s, & %s"
        else:
            format_string = "%s, " * (len(authors)-1)
            return format_string + "& %s"

    def _assemble_authors(self, authors):

        formatted_names = set()

        for a in authors:
            first_last = a.split()
            if (len(first_last) > 1):
                # This pulls the last name and first initial
                formatted_names.add(first_last[1] + ", " + first_last[0][0] + ".")

        authors = list(formatted_names)
        if (len(authors) < 1):
            return "[[[AUTHORS]]]"

        authors.sort()

        formatted_authors = self._get_author_format(authors) % tuple(authors)
        return formatted_authors

    def _format_pubdate(self, date):
        if (date is not None):
            return date.strftime("%Y, %B %d")
        else:
            return "[[[PUBLICATION DATE]]]"

    def _format_accessdate(self, date):
        if (date is not None):
            return date.strftime("%B %d, %Y")
        else:
            return "[[[ACCESS DATE]]]"
