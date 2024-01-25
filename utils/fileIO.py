import json

class File:

    @staticmethod
    def write_json(path: str, content: any) -> None:
        with open(path, 'w', encoding= "utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=2, default=str)

    @staticmethod
    def write_str(path: str, content: any) -> None:
        with open(path, 'w', encoding="utf-8") as file:
            file.writelines(content)

    @staticmethod
    def write(path: str, content: any) -> None:
        with open(path, 'a', encoding="utf-8") as file:
            file.write(content)

    @staticmethod
    def write_byte(path: str, media: any) -> None:
        with open(path, 'wb') as file:
            file.write(media.content)

    @staticmethod
    def read_json(path: str):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data