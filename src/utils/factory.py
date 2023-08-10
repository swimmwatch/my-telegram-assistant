"""
Utilities for creating factories.
"""
import typing

T = typing.TypeVar("T")
FactoryType = typing.Union["FactoryMaker", "FactoryGroupMaker"]


class FactoryGroupMaker:
    def __init__(self, *args):
        self.args = args

    def __and__(self, other: FactoryType) -> "FactoryGroupMaker":
        if isinstance(other, FactoryMaker):
            return self.__class__(other, *self.args)
        elif isinstance(other, FactoryGroupMaker):
            return self.__class__(*other.args, *self.args)

    def make(self) -> typing.Iterable:
        return (factory_maker.make() for factory_maker in self.args)


class FactoryMaker(typing.Generic[T]):
    def __init__(self, factory: typing.Callable[..., T], **kwargs) -> None:
        self.factory = factory
        self.kwargs = kwargs

    def __and__(self, other: "FactoryMaker") -> "FactoryGroupMaker":
        return FactoryGroupMaker(self, other)

    def __call__(self, *args, **kwargs) -> "FactoryMaker":
        """
        Merge factory maker arguments.
        """
        return self.__class__(self.factory, **(self.kwargs | kwargs))

    def make(self) -> T:
        return self.factory(**self.kwargs)
