from typing import Any, Optional
from abc import ABC, abstractmethod
from roughrider.traversing import DEFAULT, VIEW


class ResolveError(Exception):
    """Exception raised when a path resolution fails.
    """


class Lookup(ABC):

    @abstractmethod
    def register(self, cls, component):
        """Registers the component for the given class.
        """


class ModelLookup(Lookup):

    @abstractmethod
    def lookup(self, obj):
        """Iterator over all relevant consumers
        """

    def __call__(self, obj, stack):
        """Traverses following stack components and starting from obj.
        """
        unconsumed = stack.copy()
        while unconsumed:
            for consumer in self.lookup(obj):
                any_consumed, obj, unconsumed = consumer(obj, unconsumed)
                if any_consumed:
                    # Something was consumed, we exit.
                    break
            else:
                # nothing could be consumed
                return obj, unconsumed
        return obj, unconsumed


class ViewLookup(Lookup):
    """Looks up a view using a given method.
    """

    @abstractmethod
    def lookup(self, obj, name, environ):
        """Resolves a view given an object and a name
        """

    def __call__(self, obj, stack, environ, default='index'):
        """Resolves a view.
        """
        default_fallback = False
        unconsumed_amount = len(stack)
        if unconsumed_amount == 0:
            default_fallback = True
            ns, name = VIEW, default
        elif unconsumed_amount == 1:
            ns, name = stack[0]
        else:
            raise ResolveError(
                "Can't resolve view: stack is not fully consumed.")

        if ns not in (DEFAULT, VIEW):
            raise ResolveError(
                "Can't resolve view: namespace %r is not supported." % ns)

        view = self.lookup(obj, name, environ)
        if view is None:
            if default_fallback:
                raise ResolveError(
                    "Can't resolve view: no default view on %r." % obj)
            else:
                if ns == VIEW:
                    raise ResolveError(
                        "Can't resolve view: no view `%s` on %r." % (
                            name, obj))
                raise ResolveError(
                    "%r is neither a view nor a model." % name)
        return view


class Traverser(ABC):
    """Prototyping of a traverser.
    By default, it consumes only one stack element.
    """

    def __init__(self, obj: Any):
        self.obj = obj

    @abstractmethod
    def consume(self, ns: str, name: str) -> Optional[Any]:
        """Returns the target object
        """

    def __call__(self, consume, stack):
        ns, name = stack.popleft()
        next_obj = self.consume(ns, name)
        if next_obj is None:
            # Nothing was found, we restore the stack.
            stack.appendleft((ns, name))
            return False, self.obj, stack
        return True, next_obj, stack
