import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
        """This class represents the trivia test case"""

        def setUp(self):
            """Define test variables and initialize app."""
            self.app = create_app()
            self.client = self.app.test_client
            self.database_name = "trivia_test"
            self.database_path = "postgresql://postgres:postgres@localhost:5432/trivia_test"
            
            setup_db(self.app, self.database_path)

            # binds the app to the current context
            with self.app.app_context():
                self.db = SQLAlchemy()
                self.db.init_app(self.app)
                # create all tables
                self.db.create_all()
    
        def tearDown(self):
            """Executed after reach test"""
            pass

        """ testing endpoint'/api/v1/categories' """
        def api_v1_categories(self):
            res = self.client().get('http://127.0.0.1:5000/api/v1/categories/')
            data = json.loads(res.data)
            self.assertEqual(data.success, True)
            self.assertTrue(data.categories)
        
        def api_v1_categories_404_error_test(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/categories/')
            data = json.loads(res.data)
            
            self.assertEqual(data.status_code,404)
            self.assertEqual(data.success,False)
            self.assertEqual(data.message,"Not Found")

        """ '/api/v1/questions/' "...args.." """
        def api_v1_questions_args(self):
            res = self.client().get('http://127.0.0.1:5000/api/v1/questions/')
            data = json.loads(res.data)
            self.assertEqual(data.success,True)
            self.assertTrue(data.question)
            self.assertTrue(data.categories)
            self.assertTrue(data.total_questions)
            self.assertTrue(data.current_category)
        
        def api_v1_questions_args_404_error_test(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/questions/')
            data = json.loads(res.data)
            
            self.assertEqual(data.status_code,404)
            self.assertEqual(data.success,False)
            self.assertEqual(data.message,"Not Found")

        """ '/api/v1/questions_delete/<int:id>' """
        def api_v1_questions_delete(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/questions/1')
            data = json.loads(res.data)
            self.assertEqual(data.success,True)

        def api_v1_questions_delete_id_404_error_test(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/questions/1')
            data = json.loads(res.data)
            
            self.assertEqual(data.status_code,404)
            self.assertEqual(data.success,False)
            self.assertEqual(data.message,"Not Found")

        """ '/api/v1/create_question' """
        def api_v1_create_questions(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/questions', json={'question':'Who is the founder of Udacity?',"answer":"Sebastian Thrun","difficulty":"2","category":1,})
            data = json.loads(res.data)
            self.assertEqual(data.success,True)
        
        def api_v1_create_questions_404_error_test(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/questions')
            data = json.loads(res.data)
            
            self.assertEqual(data.status_code,404)
            self.assertEqual(data.success,False)
            self.assertEqual(data.message,"Not Found")

        """ '/api/v1/create_search' """
        def api_v1_create_search(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/create_search', json={'searchTerm':"Africa"})
            data = json.loads(res.data)
            self.assertEqual(data.success,True)
            
        def api_v1_create_search_404_error_test(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/create_search')
            data = json.loads(res.data)
            
            self.assertEqual(data.status_code,404)
            self.assertEqual(data.success,False)
            self.assertEqual(data.message,"Not Found")

        """ '/api/v1/categories/<int:id>/questions' """
        def api_v1_categories_id_questions(self):
            res = self.client().get('http://127.0.0.1:5000/api/v1/categories/2/questions')
            data = json.loads(res.data)
            self.assertEqual(data.success,True)
            self.assertTrue(data.questions)
            self.assertTrue(data.total_questions)
            self.assertTrue(data.current_category)
        
        def api_v1_categories_id_questions_404_error_test(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/categories/2/questions')
            data = json.loads(res.data)
            
            self.assertEqual(data.status_code,404)
            self.assertEqual(data.success,False)
            self.assertEqual(data.message,"Not Found")

        """ '/api/v1/quizzes' """
        def api_v1_quizzes(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/quizzes')
            data = json.loads(res.data)
            self.assertEqual(data.success,True)
            self.assertTrue(data.question)
        
        def api_v1_quizzes_404_error_test(self):
            res = self.client().post('http://127.0.0.1:5000/api/v1/quizzes')
            data = json.loads(res.data)
            
            self.assertEqual(data.status_code,404)
            self.assertEqual(data.success,False)
            self.assertEqual(data.message,"Not Found")
        

            """
            TODO
            Write at least one test for each test for successful operation and for expected errors.
            """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()