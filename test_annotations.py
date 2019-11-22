import unittest
from annotations import Annotation
from annotations import save_json
from annotations import open_json
from annotations import encode_annotation
from annotations import decode_annotation
import os

class TestAnnotations(unittest.TestCase):

    def setUp(self):
        annotations = []
        annotations.append(Annotation("Test annotation 1", "This is the first test annotation.", 100, 250))
        annotations.append(Annotation("Test annotation 2",
                                      "This is the second test annotation, but it's a little bit longer just as an edge case.",
                                      300, 350))
        annotations.append(Annotation("Test annotation 3", "This is the third test annotation.", 455, 500))
        annotations.append(Annotation("Test annotation 4",
                                      "This is in fact not the fourth test annotation, just kidding it actually is.",
                                      600, 700))
        self.annotations = annotations

    def test_generate_annotations(self):
        annotation = self.annotations[0]
        self.assertEqual(annotation.title, "Test annotation 1", "Should be Annotation 1")
        self.assertEqual(annotation.content, "This is the first test annotation.", "Should be: This is the first test annotation." )
        self.assertEqual(annotation.start, 100, "Should be 100")
        self.assertEqual(annotation.end, 250, "Should be 250")

    def test_encode_decode_annotation(self):
        annotation = self.annotations[0]
        encoded_annotation = encode_annotation(annotation)

        self.assertEqual(isinstance(encoded_annotation, dict), True, "This should be a dictionary")
        self.assertEqual(encoded_annotation["title"], annotation.title, "The titles should be the same")
        self.assertEqual(encoded_annotation["content"], annotation.content, "The content should be the same")
        self.assertEqual(encoded_annotation["start_time"], annotation.start, "The start should be the same")
        self.assertEqual(encoded_annotation["end_time"], annotation.end,  "The end should be the same")

        decoded_annotation = decode_annotation(encoded_annotation)
        self.assertEqual(isinstance(decoded_annotation, Annotation), True, "This should be an annotation object")
        self.assertEqual(annotation, decoded_annotation)


    def test_save_open_annotations(self):
        annotations = self.annotations
        save_json(annotations, "test.txt")
        loaded_annotations = open_json("test.txt")
        self.assertEqual(len(loaded_annotations), len(annotations), "Should be: 4")
        for i in range(len(annotations)):
            # check whether the annotation objects loaded have the correct information
            self.assertEqual(annotations[i], loaded_annotations[i], "Annotations should be equal")
        os.remove("test.txt")

if __name__ == '__main__':
    unittest.main()
