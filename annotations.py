import json

class Annotation:
	def __init__(self, title, content, start_time, end_time):
		self.title = title
		self.content = content
		self.start = start_time
		self.end = end_time
	def __str__(self):
		dct = vars(self)
		return str(dct)
		# return "{\"title\": \"{}\", \"content\": \"{}\", \"start\": \"{}\", \"end\": \"{}\"}".format(self.title, self.content, self.start, self.end)  
	def __repr__(self):
		return str(self)
def encode_annotation(annotation):
	if isinstance(annotation, Annotation):
		return {"__annotation__":True, "title":annotation.title, "content":annotation.content, "start_time":annotation.start, "end_time":annotation.end}
	else:
		type_name = annotation.__class__.__name__
		raise TypeError("Object of type '{}' is not JSON serializable".format(type_name))

def decode_annotation(dict):
	if "__annotation__" in dict:
		return Annotation(dict["title"], dict["content"], dict["start_time"], dict["end_time"])
	return dict

def generate_annotations():
	annotations = []
	annotations.append(Annotation("Test annotation 1", "This is the first test annotation.", 100, 250))
	annotations.append(Annotation("Test annotation 2", "This is the second test annotation, but it's a little bit longer just as an edge case.", 300, 350))
	annotations.append(Annotation("Test annotation 3", "This is the third test annotation.", 455, 500))
	annotations.append(Annotation("Test annotation 4", "This is in fact not the fourth test annotation, just kidding it actually is.", 600, 700))
	return annotations

def save_json(annotations):
	"""
	Saves an annotation object as json
	"""
	with open("test.txt","w+") as outfile:
		json.dump(annotations, outfile, sort_keys=True, default=encode_annotation)

def open_json(filename):
	"""
	Unpacks a json object into an annotation
	"""
	with open(filename) as infile:
		return json.load(infile, object_hook=decode_annotation)

def main ():
	#TODO make these testcases in the automated tests check against [{u'content': u'This is the first test annotation.', u'start': 100, u'end': 250, u'title': u'Test annotation 1'}, {u'content': u"This is the second test annotation, but it's a little bit longer just as an edge case.", u'start': 300, u'end': 350, u'title': u'Test annotation 2'}, {u'content': u'This is the third test annotation.', u'start': 455, u'end': 500, u'title': u'Test annotation 3'}, {u'content': u'This is in fact not the fourth test annotation, just kidding it actually is.', u'start': 600, u'end': 700, u'title': u'Test annotation 4'}]
	annotations = generate_annotations()
	save_json(annotations)
	loaded_annotations = open_json("test.txt")
	print(loaded_annotations)

if __name__ == "__main__":
	main()