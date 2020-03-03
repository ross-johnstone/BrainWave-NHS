import json
import datetime as dt
import itertools


class AnnotationException(Exception):
    """
    Exception for when the .json file contains annotations in an incorrect format, this annotation is ignored and execution continues,
    just without annotations.
    """
    pass


class Annotation:
    """
    Basic annotation class to represent annotations within the application, implements eq, str and repr for debugging purposes.
    """
    id_generator = itertools.count(1)

    def __init__(self, title, content, start_time, end_time, color):
        self.title = title
        self.content = content
        self.start = start_time
        self.end = end_time
        self.id = next(self.id_generator)
        self.color = color

    def __str__(self):
        return str(vars(self))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        # only compare against other annotations
        if not isinstance(other, Annotation):
            return NotImplemented
        return self.title == other.title and self.content == other.content and self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash((self.title, self.content, self.start, self.end))


def encode_annotation(annotation):
    """
    Helper function to encode an annotation object to save in a json file
    """
    if isinstance(annotation, Annotation):
        return {"__annotation__": True, "title": annotation.title, "content": annotation.content,
                "start_time": dt.datetime.isoformat(annotation.start), "end_time": dt.datetime.isoformat(annotation.end), "color": annotation.color}
    else:
        type_name = annotation.__class__.__name__
        raise TypeError(
            "Object of type '{}' is not JSON serializable".format(type_name))


def decode_annotation(dict):
    """
    Hook function to help decode an annotation object from a json file
    """
    if "__annotation__" in dict:
        return Annotation(dict["title"], dict["content"], dt.datetime.strptime(dict["start_time"], "%Y-%m-%dT%H:%M:%S.%f"), dt.datetime.strptime(dict["end_time"], "%Y-%m-%dT%H:%M:%S.%f"), dict["color"])
    return dict


def save_json(annotations, filename):
    """
    Saves an a list of annotations as a json, takes the list and filename as arguments and saves it as filename in the project directory.
    """
    with open(filename, "w+") as outfile:
        json.dump(annotations, outfile, sort_keys=True,
                  default=encode_annotation)


def open_json(filename):
    """
    Given a filename unpacks a json object into an annotation list
    """
    with open(filename) as infile:
        try:
            return json.load(infile, object_hook=decode_annotation)
        except Exception:
            raise AnnotationException(
                "Wrong format of annotation in .json file, annotations could not be loaded.")
