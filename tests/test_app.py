import os
import unittest
import tempfile
import sqlite3
from app import app, init_db

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a temporary database and Flask test client."""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
        """Close the temporary database."""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_index(self):
        """Test the index page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Smart Notes Organizer', response.data)

    def test_add_note(self):
        """Test adding a new note."""
        response = self.app.post('/add_note', data=dict(
            title='Test Note',
            content='This is a test note.',
            category='Test',
            sentiment='Positive',
            summary='A brief summary.'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Note', response.data)

    def test_search_notes(self):
        """Test searching notes."""
        self.app.post('/add_note', data=dict(
            title='Meeting Notes',
            content='Notes from the meeting last Monday.',
            category='Work',
            sentiment='Neutral',
            summary='Meeting summary.'
        ), follow_redirects=True)
        response = self.app.post('/', data=dict(query='meeting'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Meeting Notes', response.data)

if __name__ == '__main__':
    unittest.main()
