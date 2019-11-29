import json
import datetime as dt


class Annotation:
    def __init__(self, title, content, start_time, end_time):
        self.title = title
        self.content = content
        self.start = start_time
        self.end = end_time

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
	Function to help encode an annotation object to save in a json file
	"""
	if isinstance(annotation, Annotation):
		return {"__annotation__":True, "title":annotation.title, "content":annotation.content,
				"start_time":dt.datetime.isoformat(annotation.start), "end_time":dt.datetime.isoformat(annotation.end)}
	else:
		type_name = annotation.__class__.__name__
		raise TypeError("Object of type '{}' is not JSON serializable".format(type_name))

def decode_annotation(dict):
	"""
	Hook function to help decode an annotation object from a json file
	"""
	if "__annotation__" in dict:
		return Annotation(dict["title"], dict["content"], dt.datetime.strptime(dict["start_time"],"%Y-%m-%dT%H:%M:%S"), dt.datetime.strptime(dict["end_time"],"%Y-%m-%dT%H:%M:%S"))
	return dict

def save_json(annotations, filename):
    """
    Saves an annotation object as json
    """
    with open(filename, "w+") as outfile:
        json.dump(annotations, outfile, sort_keys=True, default=encode_annotation)


def open_json(filename):
    """
    Unpacks a json object into an annotation
    """
    with open(filename) as infile:
        return json.load(infile, object_hook=decode_annotation)
