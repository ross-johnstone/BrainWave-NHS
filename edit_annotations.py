from annotations import Annotation, save_json

annotation1 = Annotation("A1", "text", "start_time", "end_time")
self.annotations = [annotation1]
annotation_id = 1

for annotation in self.annotations:
    if annotation.id == annotation_id:
        title = annotation.title
        content = annotation.content

        # display the annotation title and content in a pop up box so they can edit it
        # maybe reuse the functionality when creating the annotations annotations

        annotation.title = title_entry.get()
        annotation.content = description_entry.get()
        # update the json file

        save_json(self.annotations, 'data/pat1/annotations.json')
        break
