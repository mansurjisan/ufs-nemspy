import unittest

from nemspy.model import ModelMediation, ModelVerbosity
from nemspy.model.atmospheric import AtmosphericMesh
from nemspy.model.ocean import ADCIRC
from nemspy.model.wave import WaveMesh


class TestModel(unittest.TestCase):
    def test_model(self):
        model = AtmosphericMesh(1, verbosity=ModelVerbosity.MINIMUM,
                                test='test2')

        self.assertEqual(str(model),
                         'ATM_model:                      atmesh\n' \
                         'ATM_petlist_bounds:             0 0\n' \
                         'ATM_attributes::\n' \
                         '  Verbosity = min\n' \
                         '  test = test2\n' \
                         '::')

    def test_connection(self):
        model_1 = AtmosphericMesh(1)
        model_2 = WaveMesh(1)

        model_1.connect(model_2, ModelMediation.REDISTRIBUTE)

        self.assertEqual(str(model_1.connections[0]),
                         'ATM -> WAV   :remapMethod=redist')

    def test_processors(self):
        model_1 = AtmosphericMesh(1)
        model_2 = WaveMesh(1)
        model_3 = ADCIRC(11)

        self.assertEqual(model_1.start_processor, 0)
        self.assertEqual(model_1.end_processor, 0)
        self.assertEqual(model_2.start_processor, 0)
        self.assertEqual(model_2.end_processor, 0)
        self.assertEqual(model_3.start_processor, 0)
        self.assertEqual(model_3.end_processor, 10)

        model_1.next = model_2
        model_2.next = model_3

        self.assertEqual(model_1.start_processor, 0)
        self.assertEqual(model_1.end_processor, 0)
        self.assertEqual(model_2.start_processor, 1)
        self.assertEqual(model_2.end_processor, 1)
        self.assertEqual(model_3.start_processor, 2)
        self.assertEqual(model_3.end_processor, 12)

        model_2.processors = 3
        model_1.processors = 4

        self.assertEqual(model_1.start_processor, 0)
        self.assertEqual(model_1.end_processor, 3)
        self.assertEqual(model_2.start_processor, 4)
        self.assertEqual(model_2.end_processor, 6)
        self.assertEqual(model_3.start_processor, 7)
        self.assertEqual(model_3.end_processor, 17)


if __name__ == '__main__':
    unittest.main()