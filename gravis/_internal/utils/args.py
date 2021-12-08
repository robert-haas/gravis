"""Centralized value and type checking for user-provided arguments."""

from collections.abc import Iterable as _Iterable


def check_arg(value, name, allowed_types=None, allowed_values=None, allow_none=False):
    """Check if a user-provided argument has a valid type and value.

    Parameters
    ----------
    value : any type
        Value that a user provided for an argument.
    name : str
        Name of the argument, used for proper Exception messages.
    allowed_types : type or list of types, optional
    allowed_values : list of values of any type, optional
    allow_none : bool, optional
        If True, ``value`` can be ``None`` and then no type or value checks
        are performed on it.

    Raises
    ------
    TypeError
        If the type of the given value is not contained in ``allowed_types``.
    ValueError
        If the given value is not contained in ``allowed_values``.

    """
    if not (allow_none and value is None):
        # Check type
        if allowed_types is not None and not isinstance(value, allowed_types):
            type_name = value.__class__.__name__
            if not isinstance(allowed_types, _Iterable):
                allowed_types = [allowed_types]
            allowed_type_names = ', '.join(t.__name__ for t in allowed_types)
            message = 'Argument "{}" has a wrong type: {}\n\nAllowed types: {}'.format(
                name, type_name, allowed_type_names)
            raise TypeError(message)

        # Check value
        if allowed_values is not None and value not in allowed_values:
            allowed_value_names = ', '.join(str(v) for v in allowed_values)
            message = 'Argument "{}" has a wrong value: {}\n\nAllowed values: {}'.format(
                name, value, allowed_value_names)
            raise ValueError(message)
