import json

def generate_annotations():
	annotations = []
	annotations.append({"title":"Test annotation 1", "content":"This is the first test annotation.", "start":100, "end":250})
	annotations.append({"title":"Test annotation 2", "content":"This is the second test annotation, but it's a little bit longer just as an edge case.", "start":300, "end":350})
	annotations.append({"title":"Test annotation 3", "content":"This is the third test annotation.", "start":455, "end":500})
	annotations.append({"title":"Test annotation 4", "content":"This is in fact not the fourth test annotation, just kidding it actually is.", "start":600, "end":700})
	return annotations

def save_json(annotations):
	"""
	Saves an annotation object as json
	"""
	with open("test.txt","w+") as outfile:
		json.dump(annotations, outfile)

def open_json(filename):
	"""
	Unpacks a json object into an annotation
	"""
	with open(filename) as infile:
		return json.load(infile)

def main ():
	#TODO make these testcases in the automated tests check against [{u'content': u'This is the first test annotation.', u'start': 100, u'end': 250, u'title': u'Test annotation 1'}, {u'content': u"This is the second test annotation, but it's a little bit longer just as an edge case.", u'start': 300, u'end': 350, u'title': u'Test annotation 2'}, {u'content': u'This is the third test annotation.', u'start': 455, u'end': 500, u'title': u'Test annotation 3'}, {u'content': u'This is in fact not the fourth test annotation, just kidding it actually is.', u'start': 600, u'end': 700, u'title': u'Test annotation 4'}]
	annotations = generate_annotations()
	save_json(annotations)
	loaded_annotations = open_json("test.txt")
	print(loaded_annotations)

if __name__ == "__main__":
    main()