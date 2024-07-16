import unittest
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock
from main import initialize_simulation, Environment, Scout, Worker

class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        self.mock_slider = MagicMock()
        self.mock_slider.val = 5

    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.axes')
    @patch('matplotlib.widgets.Button')
    @patch('matplotlib.widgets.Slider')
    def test_initialize_simulation(self, mock_slider, mock_button, mock_axes, mock_subplots):
        mock_subplots.return_value = (MagicMock(), MagicMock())
        mock_axes.return_value = MagicMock()
        mock_button.return_value = MagicMock()
        mock_slider.return_value = self.mock_slider

        initialize_simulation()

        self.assertIsInstance(environment, Environment)
        self.assertEqual(len(ants), 30)
        self.assertTrue(any(isinstance(ant, Scout) for ant in ants))
        self.assertTrue(any(isinstance(ant, Worker) for ant in ants))

    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.axes')
    @patch('matplotlib.widgets.Button')
    @patch('matplotlib.widgets.Slider')
    def test_environment_creation(self, mock_slider, mock_button, mock_axes, mock_subplots):
        mock_subplots.return_value = (MagicMock(), MagicMock())
        mock_axes.return_value = MagicMock()
        mock_button.return_value = MagicMock()
        mock_slider.return_value = self.mock_slider

        initialize_simulation()

        self.assertEqual(environment.width, 100)
        self.assertEqual(environment.height, 100)
        self.assertEqual(environment.num_of_food, 20)
        self.assertEqual(environment.pheromone_decay_factor, 5)

    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.axes')
    @patch('matplotlib.widgets.Button')
    @patch('matplotlib.widgets.Slider')
    def test_ant_creation(self, mock_slider, mock_button, mock_axes, mock_subplots):
        mock_subplots.return_value = (MagicMock(), MagicMock())
        mock_axes.return_value = MagicMock()
        mock_button.return_value = MagicMock()
        mock_slider.return_value = self.mock_slider

        initialize_simulation()

        scout_count = sum(1 for ant in ants if isinstance(ant, Scout))
        worker_count = sum(1 for ant in ants if isinstance(ant, Worker))

        self.assertEqual(scout_count, 25)
        self.assertEqual(worker_count, 5)

    @patch('matplotlib.pyplot.subplots')
    @patch('matplotlib.pyplot.axes')
    @patch('matplotlib.widgets.Button')
    @patch('matplotlib.widgets.Slider')
    def test_plot_setup(self, mock_slider, mock_button, mock_axes, mock_subplots):
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        mock_axes.return_value = MagicMock()
        mock_button.return_value = MagicMock()
        mock_slider.return_value = self.mock_slider

        initialize_simulation()

        mock_ax.set_xlim.assert_called_with(0, 100)
        mock_ax.set_ylim.assert_called_with(0, 100)
        mock_ax.set_xlabel.assert_called_with("X")
        mock_ax.set_ylabel.assert_called_with("Y")
        mock_fig.canvas.manager.set_window_title.assert_called_with('Ant Simulator')

if __name__ == '__main__':
    unittest.main()
