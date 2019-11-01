import boto3
import redis


def _check_type(struct, data):
    """Check if value stored in data is of the struct type.

    Arguments:
        data {any} -- Object holding data to be checked.
        struct {any} -- Types to be checked againt.
    Returns:
        {bool} -- Asserts check passed or failed.
    """
    if isinstance(struct, dict) and isinstance(data, dict):
        # struct is a dict of types or other dicts
        return all(
            k in data and _check_type(struct[k], data[k]) for k in struct
        )
    elif isinstance(struct, type):
        # struct is the type of data
        return isinstance(data, struct)
    else:
        # struct is not a standard type
        raise TypeError(f"argument {struct} not a supported type")


def _property_range_validate(data, properties):
    """Validate properties of dict by echecking that their min values are not greater than max values
        and values are not less tha 1..

    Arguments:
        data {dict} -- Mapping of minimum and maximum property to value.
        properties {list} -- List of dict properties/keys to validate against.
    Raises:
        TypeError, ValueError.
    Returns:
        N/A.
    """
    for property_ in properties:
        max_property = f"max_{property_}"
        min_property = f"min_{property_}"
        if (
            data.get(min_property) > data.get(max_property)
            or data.get(min_property) < 1
        ):
            raise ValueError("argument value invalid")


def connect_redis(host, port, password):
    # makes connection to a redis server
    r = redis.Redis(host=host, port=port, password=password)
    return r


def connect_s3(access_key_id, secret_access_key, region):
    # makes a connection to aws s3
    s3 = boto3.client(
        "s3",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name=region,
    )
    return s3


def validate_config(schema, data, properties):
    """Validate config properties by checking types and range.

    Arguments:
        schema {dict} -- Mapping of properties to type.
        data {dict} -- Mapping of minimum and maximum properties to value.
        properties {list} -- List of dict properties/keys to validate against.
    Raises:
        TypeError.
    Returns:
        N/A.
    """
    if not _check_type(schema, data):
        raise TypeError("argument type not supported")

    _property_range_validate(data, properties)
