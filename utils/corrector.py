
class Dekimashita:

    @staticmethod
    def vname(name: str, separator: str = '_') -> str:
        invalid_chars = ['/', '\\', ':', '*', '?',',', '"', '<', '>', '|', '+', '=', '&', '%', '@', '#', '$', '^', '[', ']', '{', '}', '`', '~', '\n']
        falid = ''.join(char if char not in invalid_chars else '' for char in name)

        return falid.replace(" ", separator)
        ...

    @staticmethod
    def vtext(text: str) -> str:
        try: return text.replace('\u002F', '').replace('\n', '').replace( 'u002F', '')
        except Exception: return None
        ...

    @staticmethod
    def vdict(data, filter_chars):
        """
        Filter dictionary values recursively, ignoring specified characters.

        Args:
        data (dict or list): Data (dictionary or list containing dictionaries) to filter.
        filter_chars (list): List of characters to filter.

        Returns:
        dict or list: Filtered data.
        """
        if isinstance(data, dict):
            filtered_dict = {}
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    
                    filtered_dict[key] = Dekimashita.vdict(value, filter_chars)
                elif isinstance(value, str):
                    
                    filtered_value = ''.join(char for char in value if char not in filter_chars)
                    filtered_dict[key] = filtered_value
                else:
                    
                    filtered_dict[key] = value
            return filtered_dict
        elif isinstance(data, list):
            filtered_list = []
            for item in data:
                if isinstance(item, (dict, list)):
                    
                    filtered_list.append(Dekimashita.vdict(item, filter_chars))
                elif isinstance(item, str):
                    
                    filtered_value = ''.join(char for char in item if char not in filter_chars)
                    filtered_list.append(filtered_value)
                else:
                    
                    filtered_list.append(item)
            return filtered_list
        else:
            
            return data


