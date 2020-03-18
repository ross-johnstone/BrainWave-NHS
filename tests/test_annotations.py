import unittest
import sys
import os
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
sys.path.append(os.path.join(dirname(dirname(__file__)),'res/'))
from annotations import Annotation
from annotations import save_json
from annotations import open_json
from annotations import encode_annotation
from annotations import decode_annotation
import os
from datetime import datetime


class TestAnnotations(unittest.TestCase):

    def setUp(self):
        annotations = []
        annotations.append(
            Annotation("Test annotation 1", "This is the first test annotation.", datetime.fromtimestamp(100.5),
                       datetime.fromtimestamp(250.5), (256, 0, 0)))
        annotations.append(Annotation("Test annotation 2",
                                      "This is the second test annotation, but it's a little bit longer just as an edge case.",
                                      datetime.fromtimestamp(300.5), datetime.fromtimestamp(350.5), (256, 0, 0)))
        annotations.append(
            Annotation("Test annotation 3", "This is the third test annotation.", datetime.fromtimestamp(455.5),
                       datetime.fromtimestamp(500.5), (256, 0, 0)))
        annotations.append(Annotation("Test annotation 4",
                                      "This is in fact not the fourth test annotation, just kidding it actually is.",
                                      datetime.fromtimestamp(600.5), datetime.fromtimestamp(700.5), (256, 0, 0)))
        self.annotations = annotations

    def test_generate_annotations(self):
        annotation = self.annotations[0]
        self.assertEqual(annotation.title, "Test annotation 1",
                         "Should be Annotation 1")
        self.assertEqual(annotation.content, "This is the first test annotation.",
                         "Should be: This is the first test annotation.")
        self.assertEqual(annotation.start,
                         datetime.fromtimestamp(100.5), "Should be 100")
        self.assertEqual(annotation.end, datetime.fromtimestamp(
            250.5), "Should be 250")

    def test_encode_decode_annotation(self):
        annotation = self.annotations[0]
        encoded_annotation = encode_annotation(annotation)

        self.assertEqual(isinstance(encoded_annotation, dict),
                         True, "This should be a dictionary")
        self.assertEqual(
            encoded_annotation["title"], annotation.title, "The titles should be the same")
        self.assertEqual(
            encoded_annotation["content"], annotation.content, "The content should be the same")
        self.assertEqual(encoded_annotation["start_time"], datetime.isoformat(annotation.start),
                         "The start should be the same")
        self.assertEqual(encoded_annotation["end_time"], datetime.isoformat(annotation.end),
                         "The end should be the same")

        decoded_annotation = decode_annotation(encoded_annotation)
        self.assertEqual(isinstance(decoded_annotation, Annotation),
                         True, "This should be an annotation object")
        self.assertEqual(annotation, decoded_annotation)

    def test_encode_exception(self):
        with self.assertRaises(TypeError):
            encode_annotation("Not an annotation")

    def test_save_open_annotations(self):
        annotations = self.annotations
        save_json(annotations, "test.json")
        loaded_annotations = open_json("test.json")
        self.assertEqual(len(loaded_annotations),
                         len(annotations), "Should be: 4")
        for i in range(len(annotations)):
            # check whether the annotation objects loaded have the correct information
            self.assertEqual(
                annotations[i], loaded_annotations[i], "Annotations should be equal")
        os.remove("test.json")

    def test_open_json_excpetion(self):
        with self.assertRaises(Exception):
            open_json("./data/invalid_json/annotations.json")


if __name__ == '__main__':
    unittest.main()
