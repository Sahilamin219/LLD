"""
Decorator Pattern is about adding behavior. Every "link" in the chain usually executes its logic and then calls the next one. The goal is to build a complex object by stacking features (e.g., adding a border and a scrollbar to a window).
Chain of Responsibility is about handling a request. One object in the chain typically decides whether to process the request or pass it along. The goal is to find the right handler without the sender knowing who it is (e.g., an automated phone menu or event bubbling).
"""
class Text:
    def render(self):
        return "Hello"

class Bold:
    def __init__(self, component):
        self._component = component
    def render(self):
        return f"<b>{self._component.render()}</b>"

class Italic:
    def __init__(self, component):
        self._component = component
    def render(self):
        return f"<i>{self._component.render()}</i>"

# Result: Layers both bold AND italic
message = Bold(Italic(Text()))
print(message.render()) # <b><i>Hello</i></b>
class Handler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, request):
        if self.next_handler:
            return self.next_handler.handle(request)
        return "Not handled"

class AuthHandler(Handler):
    def handle(self, request):
        if request == "login":
            return "Handled by Auth"
        return super().handle(request)

class DataHandler(Handler):
    def handle(self, request):
        if request == "fetch":
            return "Handled by Data"
        return super().handle(request)

# Result: Only the correct handler acts
chain = AuthHandler(DataHandler())
print(chain.handle("fetch")) # Handled by Data
