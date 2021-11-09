from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Welcome8:
    first_name: str
    last_name: str
    name: str
    locale: str
    picture: str
    email: str

    def __init__(self, first_name: str, last_name: str, name: str, locale: str, picture: str, email: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.name = name
        self.locale = locale
        self.picture = picture
        self.email = email

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome8':
        assert isinstance(obj, dict)
        first_name = from_str(obj.get("first_name"))
        last_name = from_str(obj.get("last_name"))
        name = from_str(obj.get("name"))
        locale = from_str(obj.get("locale"))
        picture = from_str(obj.get("picture"))
        email = from_str(obj.get("email"))
        return Welcome8(first_name, last_name, name, locale, picture, email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["first_name"] = from_str(self.first_name)
        result["last_name"] = from_str(self.last_name)
        result["name"] = from_str(self.name)
        result["locale"] = from_str(self.locale)
        result["picture"] = from_str(self.picture)
        result["email"] = from_str(self.email)
        return result


def welcome8_from_dict(s: Any) -> Welcome8:
    return Welcome8.from_dict(s)


def welcome8_to_dict(x: Welcome8) -> Any:
    return to_class(Welcome8, x)