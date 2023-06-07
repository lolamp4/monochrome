from __future__ import annotations
import cohere


from typing import List, TYPE_CHECKING
from cohere.client import ClassifyExample

if TYPE_CHECKING:
    from comments import Comments, examples

co = cohere.Client('rYFZf3Cna0haQpn87w85IoUwARMWcb17DqF0ZU08')



class User:
    """A customer."""
    name: str
    comments: List[Comments]

    def __init__(self, name: str) -> None:
        self.name = name
        self.comments = []

    def add_comment(self, business: Business, comment: Comments) -> None:
        """If comment already in self.comments, do nothing and return False.
        If comment is offensive, return 'You cannot say that'
        If comment is valid, add to self.comments and return True.
        """
        if (co.classify([comment.content], examples=examples).classifications[0].prediction != 'offensive') and (comment not in self.comments):
            self.comments.append(comment)
            business.reviews.append((comment, self))
            examples.append(ClassifyExample(comment.content, co.classify([comment.content], examples=examples).classifications[0].prediction))
            print(f"You just commented '{comment}'")
        elif comment in self.comments:
            print('You have already said that.')
        else:
            examples.append(ClassifyExample(comment.content, co.classify([comment.content], examples=examples).classifications[0].prediction))
            # Train AI model by adding it to examples
            print('This is potentially offensive, you cannot say that.')

    def __str__(self) -> str:
        return self.name


class Business:
    """A business brand."""

    # Attribute type
    name: str
    services: list[str]
    reviews: list[tuple[Comments, User]]

    def __init__(self, name: str, services: list) -> None:
        self.name = name
        self.reviews = []
        self.services = services

    def __str__(self) -> str:
        final_str = f'{self.name} is a black owned business.\n'
        if self.reviews == []:
            return final_str + f'{self.name} has no reviews yet! sorry :/'
        else:
            final_str += self.review_type() + '\n'
            for review in self.reviews:
                final_str += f'{review[1]} said: {review[0]}\n'
        return final_str

    def review_type(self) -> str:
        """ Summarize the types of reviews for <business>. """
        positive = 0
        negative = 0
        for review in self.reviews:
            if co.classify([review[0].content], examples=examples).classifications[0].prediction == 'positive review':
                positive += 1
            if co.classify([review[0].content], examples=examples).classifications[0].prediction == 'negative review':
                negative += 1
        return f'{self.name} has {positive} positive review(s) and {negative} negative review(s).'


class MadeForBlack:
    """A website where black people meet black businesses."""
    # Attribute types
    _businesses: dict[Business, list[Business.name, Business.services]]
    _users: dict[User.name, str]

    def __init__(self) -> None:
        self._businesses = {}
        self._users = {}

    def add_business(self, businesses: list) -> None:
        lst = []
        for business in businesses:
            b = Business(business["name"], business["services"])
            self._businesses[b] = [b.name, b.services]
            lst.append(self._businesses[b])
        print(lst)

    def register_user(self, user: str, email: str) -> None:
        u = User(user)
        self._users[u.name] = email

     
    def search_for_business(self, service: str) -> None:
        lst = []
        for business in self._businesses:
            if service in business.services:
                lst.append(business.name)
        print(lst)

    def __str__(self) -> str:
        remark = 'Made for Black is a marketplace where black owners can meet black customers'+ '\n' + 'Businesses listed:' + '\n' * 2
        for business in self._businesses:
            remark += str(business) + '\n' * 2
        return remark


if __name__ == '__main__':
    from comments import Comments, examples
    from mockdata import visitors_data, businesses_data, reviews_data
    angry = Comments('waste of money, never buying that again')
    happy = Comments('i am buying two more!')
    offensive = Comments('go back to your country')
    happy2 = Comments('i am buying two more!')
    chris = User('Chris')
    salon = Business("Enny's Salon", ['hair', 'self-care'])
    chris.add_comment(salon, angry)
    chris.add_comment(salon, happy)
    chris.add_comment(salon, offensive)
    chris.add_comment(salon, happy)
    print('Business example')
    print(salon)
    s = MadeForBlack()
    for i in visitors_data:
        s.register_user(i['name'], "johndoe@gmail.com")
    print('List of Users ' + '\n')
    print(s._users)
    print('List of Businesses' + '\n')
    s.add_business(businesses_data)
    print('List of businesses that provide food services')
    s.search_for_business('food')
    print(s)


