import cohere
from cohere.client import ClassifyExample

co = cohere.Client('yyY3fuwyrGeoSLdlcUHTNblXSW8A07zNtEuDmlde')


examples = [ClassifyExample('go to hell', 'offensive'),
            ClassifyExample('are you this stupid', 'offensive'),
            ClassifyExample('would not recommend', 'negative review'),
            ClassifyExample('i loved it!!', 'positive review'),
            ClassifyExample('you should try it', 'positive review'),
            ClassifyExample('bad customer service', 'negative review'),
            ClassifyExample("best food i've tried!", 'positive review'),
            ClassifyExample('i felt so at home.', 'positive review'),
            ClassifyExample('the food was so nasty ugh', 'negative review'),
            ClassifyExample('disgusting food', 'negative review')]


class Comments:
    """Comments customers leave for businesses they patronise."""
    # Attribute type
    content: str

    def __init__(self, comment: str) -> None:
        self.content = comment

    def __str__(self) -> str:
        return self.content


