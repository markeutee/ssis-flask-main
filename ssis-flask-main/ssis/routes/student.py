#routes/student.py
from flask import Blueprint
from flask import current_app as app
from flask import render_template, request, redirect, url_for, jsonify

from ..models.Course import Course
from ..models.College import College
from ..models.Student import Student

from cloudinary import uploader
from cloudinary.uploader import upload
from config import Config
import re

student_bp = Blueprint(
    "student_bp",
    __name__,
)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_public_id_from_url(url):
    match = re.search(r'/v\d+/(ssis/[^/]+)\.\w+', url)
    return match.group(1) if match else None

def check_file_size(picture):
    maxsize = 1 * 1024 * 1024  # 1MB
    picture.seek(0, 2)  
    size = picture.tell()  # Get size in bytes
    picture.seek(0)  
    print("📸 Uploaded picture size:", size, "bytes")
    return size <= maxsize

@student_bp.route("/")
@student_bp.route("/student")
def student():
    colleges = College.get_all()
    courses = Course.get_all()

    # 📄 Pagination logic
    page = request.args.get('page', default=1, type=int)
    per_page = 10  # Number of students per page
    offset = (page - 1) * per_page

    # Get paginated student list and total count
    students = Student.get_paginated(limit=per_page, offset=offset)
    total_count = Student.get_total_count()
    total_pages = (total_count + per_page - 1) // per_page  # ceiling division

    return render_template(
        'student_home.html',
        colleges=colleges,
        courses=courses,
        students=students,
        page=page,
        total_pages=total_pages
    )

@student_bp.route("/student/add", methods=['POST'])
def student_add():
    print("🧾 Form Data Received:")
    print("Student ID:", request.form.get("student_id"))
    print("First Name:", request.form.get("student_first_name"))
    print("Last Name:", request.form.get("student_last_name"))
    print("Course Code:", request.form.get("student_course_code"))
    print("Year:", request.form.get("student_year"))
    print("Gender:", request.form.get("student_gender"))
    print("✅ Student added successfully")

    id = request.form.get('student_id', '').strip()
    firstname = request.form.get('student_first_name')
    lastname = request.form.get('student_last_name')
    course_code = request.form.get('student_course_code')
    year = request.form.get('student_year')
    gender = request.form.get('student_gender')

    # Get file, but no error if not present
    picture = request.files.get('formFile')  # changed here from request.files['formFile']

    # Check if student ID is already taken
    exist_student = Student.check_existing_id(id)
    if exist_student:
        return jsonify({'error': f"Student ID: {id} is already taken"})

    picture_url = None  # default no picture

    # Only validate picture if user uploaded one
    if picture and picture.filename != '':
        if not allowed_file(picture.filename):
            return jsonify({'error': 'Image is required and must be PNG, JPG, or JPEG'})

        if not check_file_size(picture):
            return jsonify({'error': 'Max file size is 1MB'})

        try:
            # Upload image to Cloudinary
            result = upload(picture, folder=Config.CLOUDINARY_FOLDER)
            picture_url = result['secure_url']
        except Exception as e:
            return jsonify({'error': str(e)})

    # If no picture uploaded, picture_url stays None (or you can assign default here if you want)
    student = Student(
        id=id,
        firstname=firstname,
        lastname=lastname,
        course_code=course_code,
        year=year,
        gender=gender,
        picture=picture_url  # None or uploaded URL
    )
    student.add()

    return jsonify({'redirect': url_for("student_bp.student")})


@student_bp.route("/student/delete", methods=['POST'])
def student_delete():
    try:
        id = request.form.get('student_id')
        if not id:
            return jsonify({'error': 'Missing student ID'}), 400

        student = Student.get_one(id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404

        if student.picture:
            public_id = get_public_id_from_url(student.picture)
            if public_id:
                uploader.destroy(public_id)

        student.delete()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': f"Error: {str(e)}"}), 500

@student_bp.route("/student/edit", methods=['POST'])
def student_edit():
    pastid = request.form.get('pastid')
    id = request.form.get('edit_student_id')
    firstname = request.form.get('edit_student_first_name')
    lastname = request.form.get('edit_student_last_name')
    course_code = request.form.get('edit_student_course_code')
    year = request.form.get('edit_student_year')
    gender = request.form.get('edit_student_gender')
    picture = request.files.get('editFormFile')  # ✅ safe get

    student = Student.get_one(pastid)

    # Check ID conflicts
    if id != pastid:
        exist_student = Student.get_one(id)
        if exist_student:
            return jsonify({'error': f"Student ID: {id} is already taken"})

    try:
        # Update basic info
        student.id = id
        student.firstname = firstname
        student.lastname = lastname
        student.course_code = course_code
        student.year = year
        student.gender = gender

        # ✅ Only update picture if a new one is uploaded
        if picture and picture.filename.strip():
            if not allowed_file(picture.filename):
                return jsonify({'error': 'Image must be PNG, JPG, or JPEG'})
            if not check_file_size(picture):
                return jsonify({'error': 'Max Size Limit is: 1MB'})

            # Delete old picture from Cloudinary
            if student.picture:
                public_id = get_public_id_from_url(student.picture)
                if public_id:
                    uploader.destroy(public_id)

            # Upload new picture
            result1 = upload(picture, folder=Config.CLOUDINARY_FOLDER)
            student.picture = result1['secure_url']

        # ✅ If no new picture uploaded → keep existing one

        student.update(pastid if id != pastid else id)
        return redirect(url_for("student_bp.student"))

    except Exception as e:
        return jsonify({'error': str(e)})
        

@student_bp.route("/student/search", methods=['GET','POST'])
def student_search():
    input = request.args.get('querystudent')
    filter = request.args.get('filter_student')

    if input:
        students = Student.search(input,filter)
        if not students:
            filter_message = ""
            if filter == "0":
                filter_message = "Student ID or NAME or COURSE or YEAR or GENDER"
            elif filter == "1":
                filter_message = "Student ID"
            elif filter == "2":
                filter_message = "Student FirstName"
            elif filter == "3":
                filter_message = "Student Last Name"
            elif filter == "4":
                filter_message= "Student Course"
            elif filter == "5":
                filter_message= "Student Year"
            elif filter == "6":
                filter_message = "Student Gender"
            elif filter == "7":
                filter_message = "Student College"
            return render_template('student_home.html', studentInput = input, search = True, hideAdd = True , filter_message=filter_message)
        else:
            return render_template('student_home.html', students=students, hideAdd = True, search = True, studentInput=input)
    return redirect(url_for("student_bp.student"))
