from roughrider.traversing.meta import ModelLookup, ViewLookup
from roughrider.traversing.parsing import parse_path
from urllib.parse import unquote


class PublicationError(Exception):
    """Exception raised when the publisher is unable to resolve the
    path into a publishable object.
    """


class Publisher:
    """A publisher using model and view lookup components.
    """
    model_lookup: ModelLookup
    view_lookup: ViewLookup

    def publish(self, root, environ):
        path = unquote(
            environ['PATH_INFO'].encode('latin-1').decode('utf-8'))
        stack = parse_path(path)
        model, crumbs = self.model_lookup(root, stack)
        component = self.view_lookup(model, crumbs, environ)

        # The model needs an renderer
        if component is None:
            raise PublicationError('%r can not be rendered.' % model)

        return component
