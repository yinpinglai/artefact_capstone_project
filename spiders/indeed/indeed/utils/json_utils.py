import json

class JSONUtils:

    _KEYWORDS_JSON_FILE = 'indeed/resources/keywords.json'

    @classmethod
    def load_keywords_json(cls) -> list[list[str]]:
        '''
        Load the keywords combination list from the keywords.json file.
        
        Returns:
        List<List<str>>: The predefined combination of keywords list 
        '''
        combination_of_keywords_list = []

        with open(cls._KEYWORDS_JSON_FILE) as json_file:
            combination_of_keywords_list = json.load(json_file)
        
        return combination_of_keywords_list
    
    @staticmethod
    def get_dict_from(json_string: str) -> dict:
        '''
        Load the JSON object from the given JSON string and convert to Python dictionary object.

        Parameters:
        json_string: str - The JSON string to be converted to Python dictionary object.

        Returns:
        result: dict - The dictionary instance 
        '''
        if json_string is None or len(json_string) == 0:
            return dict({})
        
        return json.loads(json_string)
