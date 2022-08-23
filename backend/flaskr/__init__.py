import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r'/*': {"origins": '*'}}, support_credentials=True)
    
    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
        return response
    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/v1/categories', methods=['GET'])
    def categories_index():
        try:
            categories = Category.query.all()
            formatted_category ={}

            for category in categories:
                formatted_category.update({category.id:category.type})
            
            return (jsonify({
                'categories':formatted_category,
                'success':True
            }))
        except:
            abort(404)
        
   
    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/v1/questions/', methods =['GET'])
    def questions():
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * 10
            end = start + 10
            quests = Question.query.all()
            formatted_questions = [quest.format() for quest in quests]
            
            categories = Category.query.all()
            current_category =  Category.query.first().type
           
            formatted_category ={}

            for category in categories:
                formatted_category.update({category.id:category.type})
            return jsonify({
                'success': True,
                'questions':formatted_questions[start:end],
                'categories':formatted_category,
                'total_questions':len(formatted_questions),
                'current_category':current_category
                })
        except:
            abort(404)

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/v1/questions_delete/<int:id>/', methods =['DELETE','OPTIONS'])
    def questions_delete(id):        
        try:
                        
                    oneQuests = Question.query.filter(Question.id==id).one_or_none()
                        
                    if(oneQuests is None): abort(404)
                    else: 
                        oneQuests.delete()
                        
                        return (jsonify({
                            'success': True,
                            'message':'question ({id}) deleted  successfully!',
                            }))
            
        except:
             abort(400)
    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/api/v1/create_question', methods=['POST', 'OPTIONS'])
    def create_question():
        try:
            content = request.get_json()
            question = content.get('question', None)
            answer = content.get('answer', None)
            difficulty = content.get('difficulty', None)
            category = content.get('category', None)
            add = Question(question=question, answer=answer,difficulty=difficulty,category=category)
            add.insert()
            return( jsonify({
                    'success': True,
                    'message':'question created successfully!',
                    }))
        except:
           abort(422)
           
    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/api/v1/create_search', methods=['POST','OPTIONS'])
    def create_search():   
          try:     
            content = request.get_json()
            strg = content.get('searchTerm', None)
            qst = Question.query.all()
            currentCategory = Question.query.join(Category, Question.category==Category.id)
            arr = []
                
            for question in qst:
                if question.question.find(strg) !=-1:
                    arr.append({ "question":question.question,
                                    "id":question.id,
                                    "difficulty":question.difficulty,
                                    "category":question.category,
                                    "answer":question.answer,
                                    })
            
            formatted_questions = [quest.format() for quest in currentCategory]
            print(arr)
            return (jsonify({
                    'success': True,
                    'message':'question created successfully!',
                    'questions':arr,
                    'total_questions':len(arr),
                    'current_category':formatted_questions
                    }) )
          except:
            abort(422)
     
                
       
    """
    @DONE:
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/v1/categories/<int:id>/questions', methods =['GET'])
    def categories(id):
       try:
            
            categories =Question.query.filter(id==Question.category).all()
            current_category =  Category.query.filter_by(id=Category.id).first().type

            formatted_questions = [quest.format() for quest in categories]
            print(formatted_questions)
            return (jsonify({
                'success': True,
                'questions':formatted_questions,
                'total_questions':len(formatted_questions),
                'current_category':current_category,
                }))
       except:
        abort(404)
    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/api/v1/quizzes/', methods=['POST'])
    def quizzes():
        try:
            content = request.get_json()
            previous_question = content.get('previous_questions', None)
            quiz_category = content.get('quiz_category', None)
            categories =Question.query.filter(Question.category==quiz_category['id']).all()
            categories_empty =Question.query.all()
            random.shuffle(categories)
            random.shuffle(categories_empty)
            if quiz_category['id'] == 0:
                for quest in categories_empty:
                
                   if (quest.id in previous_question):
                        pass
                   else:
                        return (jsonify({
                                    'question':{"question":quest.question,
                                                "id":quest.id,
                                                "difficulty":quest.difficulty,
                                                "category":quest.category,
                                                "answer":quest.answer,
                                                'quiz_category':None
                                                },
                                    'success':True
                                }) )
            else:  
                for question in categories:
                    if (question.id in previous_question):
                        pass
                    else:
                        return (jsonify({
                                'question':{"question":question.question,
                                            "id":question.id,
                                            "difficulty":question.difficulty,
                                            "category":question.category,
                                            "answer":question.answer,
                                            'quiz_category':quiz_category
                                            },
                                'success':True
                            }) )
        except:
            abort(404)  
    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )
     
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
    """
    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )
         """
    return app

