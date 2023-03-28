from urllib.parse import unquote

class URLInterpreter:

    @classmethod
    def parse_url(cls, url: str) -> str:
        '''
        Get the purified URL from response

        Parameters:
        url: str - The URL from response

        Returns:
        url: str - The purified URL string
        '''
        if url is None or len(url) == 0 or 'url=' not in url:
            return url
        
        index = url.index('url=')
        indeed_url = url[index + 4:]
        return unquote(indeed_url)
