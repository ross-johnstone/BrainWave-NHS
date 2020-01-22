from annotations import Annotation, save_json

annotation1 = Annotation("A1", "text", "start_time", "end_time")
self.annotations = [annotation1]
annotation_id = 1

for i in range(len(self.annotations)):
    annotation = self.annotations[i]
    if annotation.id == annotation_id:

        # just delete from the list
        self.annotations.remove(i)
        # update the json file
        save_json(self.annotations, 'data/pat1/annotations.json')
        break
