from json import dump
from msilib import type_string
import os
import re
from tokenize import String
from unicodedata import category
from xml.dom.minidom import TypeInfo
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    """ @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, application/json')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response """
        
    """
    @TODO:
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
            
            return jsonify({
                'categories':formatted_category,
                'success':True
            })
        except:
            abort(404)
        
   
    """
    @TODO:
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
            #formatted_current_category = [ctgy.format() for ctgy in current_category]

            formatted_category ={}

            for category in categories:
                formatted_category.update({category.id:category.type})
            #formatted_category = [category.format() for category in categories]
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
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/v1/questions_delete/<int:id>', methods =['POST'])
   # @cross_origin()
    def questions_delete(id):
        
        try:
            if(request.type == 'DELETE'):
                #id = request.args.get('id', 1, type=int)
                oneQuests = Question.query.filter(id).delete()
                return jsonify({
                    'success': True,
                    'message':'question deleted successfully!',
                    })
            else:
                pass
        except:
             abort(404)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/api/v1/create_question', methods=['POST'])
    def create_question():
        try:
            content = request.get_json()
            question = content.get('question', None)
            answer = content.get('answer', None)
            difficulty = content.get('difficulty', None)
            category = content.get('category', None)
            add = Question(question=question, answer=answer,difficulty=difficulty,category=category)
            add.insert()
            return jsonify({
                    'success': True,
                    'message':'question created successfully!',
                    })
        except:
           abort(404)
           
           #return content
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/api/v1/create_search', methods=['POST'])
    #@cross_origin()
    def create_search():   
          #try:     
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
            #print( vars(currentCategory))
            
            formatted_questions = [quest.format() for quest in currentCategory]
            print(arr)
            return jsonify({
                    'success': True,
                    'message':'question created successfully!',
                    'questions':arr,
                    'total_questions':len(arr),
                    'current_category':formatted_questions
                    }) 
          #except:
            #abort(404)
            #return 
     
                
       
    """
    @TODO:
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
            return jsonify({
                'success': True,
                'questions':formatted_questions,
                'total_questions':len(formatted_questions),
                'current_category':current_category,
                })
       except:
        abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/api/v1/quizzes', methods=['POST'])
    #@cross_origin()
    def quizzes():
       ## try:
            content = request.get_json()
            previous_question = content.get('previous_questions', None)
            quiz_category = content.get('quiz_category', None)
            id = quiz_category
            print(type(quiz_category))
            print(quiz_category)
            categories =Question.query.filter(Question.category==quiz_category['id']).all()
            quest = []
            moris=[quest.format() for quest in categories]
            #return moris
            
            random.shuffle(categories)
            for question in categories:
                if (question.id in previous_question):
                    pass
                else:
                    #moris=[quest.format() for quest in question]
                    return jsonify({
                            'question':{"question":question.question,
                                        "id":question.id,
                                        "difficulty":question.difficulty,
                                        "category":question.category,
                                        "answer":question.answer,
                                        'quiz_category':quiz_category
                                        },
                            'success':True
                        }) 
            
             
        ##except:
            ##abort()
            ##return   
    """
    
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler
    def not_found():
        return jsonify({
            "success":False,
            "error":404,
            "message":"Not Found"},404)
        
    return app

