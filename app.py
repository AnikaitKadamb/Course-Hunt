import operations
from flask import Flask, request, render_template, jsonify, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/coursesearch", methods = ["POST"])
def search():
    course_code = request.form.get("course_code")
    if not course_code:
        return jsonify({"error": "Course Code is required"}), 400
    posts = operations.get_course_posts(course_code,"all",15)
    commentlist = operations.get_posts_comments(posts)

    checkdict = {
        "midterm": 0,
        "final": 0,
        "research" : 0,
        "assignment": 0,
        "essay": 0,
        "quiz": 0,
        "test": 0,
        "lab": 0,
        "project":0,
        "group":0,
        "presentation":0
    }

    categorydict = {
        "Exams": {},
        "Assignments":{},
        "Projects":{}
    }


    end = operations.check_var(commentlist, checkdict)
    benchmark = round((max(checkdict.values()) - (min(checkdict.values())+1))/2)
    course_work = {}
    course_work = operations.course_work_list(checkdict,benchmark)
    if end == 0:
        return render_template("coursework.html",coursework = course_work, course_code = course_code)
    operations.set_null_dict(checkdict,0)
    operations.set_null_dict(checkdict,{})
    return render_template("coursework.html", coursework = course_work, course_code = course_code)

if __name__ == '__main__':
    app.run(debug = True)




