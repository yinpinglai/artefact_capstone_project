import re

class HTMLUtils:

    HTML_TAG_REGEX = re.compile('<.*?>')

    @classmethod
    def remove_html_tags(cls, html:str) -> str:
        '''
        Remove HTML tags from the given HTML string

        Parameters:
        html: str - The HTML string

        Returns:
        text: str - The plain text without containing any HTML tag 
        '''
        if html is None or len(html) == 0:
            return html
        
        return re.sub(HTMLUtils.HTML_TAG_REGEX, '', html).strip()
