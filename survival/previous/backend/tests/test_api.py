import unittest
import json
from backend import app  # Import your Flask app here

class TaskManagerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a test client for the Flask app"""
        cls.client = app.test_client()
        cls.client.testing = True

    def test_get_tasks_empty(self):
        """Test the GET /api/tasks endpoint when there are no tasks"""
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_add_task_without_task(self):
        """Test the POST /api/tasks endpoint with missing task data"""
        response = self.client.post('/api/tasks',
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No task provided', response.json.get('error'))

    def test_create_delete_task(self):
        """Test the DELETE /api/tasks endpoint"""
        # First, add a task
        task_data = {"task": "Test Task 1"}
        self.client.post('/api/tasks',
                         data=json.dumps(task_data),
                         content_type='application/json')

        # Check if the task was added
        response = self.client.get('/api/tasks')
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['task'], 'Test Task 1')

        # Delete the task
        response = self.client.delete('/api/tasks',
                                      data=json.dumps({"task": "Test Task 1"}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task deleted successfully!', response.json.get('message'))

        # Verify that the task is deleted
        response = self.client.get('/api/tasks')
        self.assertEqual(len(response.json), 0)

    def test_delete_non_existing_task(self):
        """Test DELETE /api/tasks with a non-existing task"""
        response = self.client.delete('/api/tasks',
                                      data=json.dumps({"task": "Non-existent Task"}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Task deleted successfully!', response.json.get('message'))

if __name__ == '__main__':
    unittest.main()
