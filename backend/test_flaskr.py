import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


from dotenv import load_dotenv
load_dotenv()

DATABASE_USERNAME= os.environ.get("DATABASE_USERNAME")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_PORT=os.environ.get("DATABASE_PORT")
DATABASE_NAME=os.environ.get("DATABASE_NAME")
DATABASE_TEST_NAME=os.environ.get("DATABASE_TEST_NAME")

class TriviaTestCase(unittest.TestCase):
        """This class represents the trivia test case"""
        def setUp(self):
            """Define test variables and initialize app."""
            self.app = create_app()
            self.client = self.app.test_client
            self.database_name = "trivia_test"
            self.database_path =  'postgresql://{}:{}@localhost:{}/{}'.format(DATABASE_USERNAME,DATABASE_PASSWORD,DATABASE_PORT,DATABASE_TEST_NAME)
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
       
        def test_get_categories(self):
            res = self.client().get('/api/v1/categories')
            data = json.loads(res.data)
            self.assertEqual(data['success'], True)
           
        def test_404_get_categories_response(self):
            res = self.client().get('/api/v1/categories')
            data = json.loads(res.data)
            self.assertEqual(data['error'],404)
            self.assertEqual(data['success'],False)
            self.assertEqual(data['message'],"Not Found")
        
        """ '/api/v1/questions/' "...args.." """
        def test_get_questions_args(self):
            res = self.client().get('/api/v1/questions/?page=1')
            data = json.loads(res.data)

            self.assertEqual(data['success'],True)
            self.assertTrue(data['questions'])
            self.assertTrue(data['categories'])
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['current_category'])
        
        def test_404__get_questions__response(self):
            res = self.client().get('/api/v1/questions/?page=1')
            data = json.loads(res.data)
            
            self.assertEqual(data['error'],404)
            self.assertEqual(data['success'],False)
            self.assertEqual(data['message'],"Not Found")
       
        """ '/api/v1/questions_delete/<int:id>' """
        def test_delete_question(self):
            res = self.client().delete('/api/v1/questions_delete/6')
            data = json.loads(res.data)
            self.assertEqual(data['success'],True)

        
        def test_404_delete_questions_response(self):
            res = self.client().delete('/api/v1/questions_delete/1/')
            data = json.loads(res.data)
            
            self.assertEqual(data.status_code,404)
            self.assertEqual(data['success'],False)
            self.assertEqual(data['message'],"Not Found")
            
       
        """ '/api/v1/create_question' """
        def test_post_questions_response(self):
            res = self.client().post('/api/v1/questions', json={'question':'Who is the founder of Udacity?',"answer":"Sebastian Thrun","difficulty":"2","category":1,})
            data = json.loads(res.data)
            self.assertEqual(data['success'],True)
        
        def test_404_post_questions_response(self):
            res = self.client().post('/api/v1/questions')
            data = json.loads(res.data)
            
            self.assertEqual(data['error'],404)
            self.assertEqual(data['success'],False)
            self.assertEqual(data['message'],"Not Found")
       
        """ '/api/v1/create_search' """
        def test_post_search(self):
            res = self.client().post('/api/v1/create_search', json={'searchTerm':"Africa"})
            data = json.loads(res.data)
            self.assertEqual(data['success'],True)
           
        def test_404_create_search_response(self):
            res = self.client().post('/api/v1/create_search/')
            data = json.loads(res.data)
            
            self.assertEqual(data['error'],404)
            self.assertEqual(data['success'],False)
            self.assertEqual(data['message'],"Not Found")
        
        """ '/api/v1/categories/<int:id>/questions' """
        def test_get_questions_based_on_id(self):
            res = self.client().get('/api/v1/categories/2/questions')
            data = json.loads(res.data)
            self.assertEqual(data['success'],True)
            self.assertTrue(data['questions'])
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['current_category'])
         
        def test_404_get_questions_based_on_id_response(self):
            res = self.client().get('/api/v1/categories/2/questions')
            data = json.loads(res.data)
            
            self.assertEqual(data['error'],404)
            self.assertEqual(data['success'],False)
            self.assertEqual(data['message'],"Not Found") 
        
        """ '/api/v1/quizzes' """
        def test_api_v1_quizzes(self):
            res = self.client().post('/api/v1/quizzes/', json={'previous_questions':[],'quiz_category':{'id':1}})
            data = json.loads(res.data)
            print(data)
            self.assertEqual(data['success'],True)
            self.assertTrue(data['question'])
   
        def test_api_v1_quizzes_404_error_test(self):
            res = self.client().post('/api/v1/quizzes/')
            data = json.loads(res.data)
            
            self.assertEqual(data['error'],404)
            self.assertEqual(data['success'],False)
            self.assertEqual(data['message'],"Not Found") 
      
        
        """
        @DONE
        Write at least one test for each test for successful operation and for expected errors.
        """
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()