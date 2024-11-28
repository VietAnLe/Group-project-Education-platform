from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import bcrypt  # For secure password hashing
import os
import datetime #For check time req
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'duc22bi13085'  # Replace with your MySQL root password
app.config['MYSQL_DB'] = 'english_learning'
app.secret_key = 'your_secret_key'  # For session management

mysql = MySQL(app)


# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'  # Folder where uploaded files will be stored
ALLOWED_EXTENSIONS = {'pdf', 'mp4', 'png', 'jpg', 'jpeg', 'gif', 'avi', 'mov'}  # Allowed file types (you can add more types if needed)
# Define the path for saving images
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SECRET_KEY'] = 'your_secret_key'  # For session and flashing messages

# Function to check if file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Home route
@app.route('/')
def home():
    if 'user_id' not in session:
        flash('Please log in to access the home page.', 'warning')
        return redirect(url_for('login'))

    # Redirect based on user role
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    elif role == 'student':
        return redirect(url_for('student_dashboard'))

    flash('Invalid role detected.', 'danger')
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Hash the password securely
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email is already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        cursor.execute(
            "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
            (username, email, hashed_password, role)
        )
        mysql.connection.commit()
        cursor.close()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate user credentials
        user = validate_user(email, password)

        if user:
            session['user_id'] = user[0]  # User ID
            session['username'] = user[1]  # Username
            session['role'] = user[4]  # User role

            # Redirect based on role
            if user[4] == 'student':
                return redirect(url_for('student_dashboard'))
            elif user[4] == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif user[4] == 'admin':
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

# Validate user function
def validate_user(email, password):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # Check if password matches
        stored_password = user[3]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return user
    return None

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Admin dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))
    cursor = mysql.connection.cursor()

    # Count teachers by filtering users with role='teacher'
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'teacher'")
    total_teachers = cursor.fetchone()[0]

    # Count courses
    cursor.execute("SELECT COUNT(*) FROM courses")
    total_courses = cursor.fetchone()[0]

    # Count lessons
    cursor.execute("SELECT COUNT(*) FROM lessons")
    total_lessons = cursor.fetchone()[0]

    # Count enrollments
    cursor.execute("SELECT COUNT(*) FROM enrollments")
    total_enrollments = cursor.fetchone()[0]

    cursor.close() 

    return render_template('admin_dashboard.html', total_teachers=total_teachers,
                           total_courses=total_courses, total_lessons=total_lessons,
                           total_enrollments=total_enrollments)
    
    
# Admin manage teachers
@app.route('/admin/manage_teachers', methods=['GET', 'POST'])
def admin_manage_teachers():
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        # Handle adding a new teacher
        if 'add_teacher' in request.form:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            # Hash the password securely
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            try:
                cursor.execute("""
                    INSERT INTO users (username, email, password, role) 
                    VALUES (%s, %s, %s, 'teacher')
                """, (username, email, hashed_password))
                mysql.connection.commit()
                flash('Teacher added successfully!', 'success')
            except Exception as e:
                flash(f'Error adding teacher: {e}', 'danger')

        # Handle removing a teacher
        elif 'remove_teacher' in request.form:
            teacher_id = request.form['teacher_id']
            try:
                cursor.execute("DELETE FROM users WHERE id = %s AND role = 'teacher'", (teacher_id,))
                mysql.connection.commit()
                flash('Teacher removed successfully!', 'success')
            except Exception as e:
                flash(f'Error removing teacher: {e}', 'danger')

    # Fetch all teachers
    cursor.execute("SELECT id, username, email FROM users WHERE role = 'teacher'")
    teachers = cursor.fetchall()
    cursor.close()

    return render_template('admin_manage_teachers.html', teachers=teachers)

# Admin view student enrollments 
@app.route('/admin/manage_enrollments', methods=['GET', 'POST'])
def admin_manage_enrollments():
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        # Remove Enrollment
        if 'remove_enrollment' in request.form:
            enrollment_id = request.form['enrollment_id']
            try:
                cursor.execute("DELETE FROM enrollments WHERE id = %s", (enrollment_id,))
                mysql.connection.commit()
                flash('Enrollment removed successfully!', 'success')
            except Exception as e:
                flash(f'Error removing enrollment: {e}', 'danger')

    # Fetch enrollments
    cursor.execute("""
        SELECT enrollments.id, users.username AS student, courses.name AS course
        FROM enrollments 
        JOIN users ON enrollments.user_id = users.id
        JOIN courses ON enrollments.course_id = courses.id
    """)
    enrollments = cursor.fetchall()
    cursor.close()

    return render_template('admin_manage_enrollments.html', enrollments=enrollments)

#Admin manage lessons
@app.route('/admin/manage_lessons', methods=['GET', 'POST'])
def admin_manage_lessons():
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    # Fetch all courses
    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()

    # Handle form submission
    if request.method == 'POST':
        # Add Lesson
        if 'add_lesson' in request.form:
            course_id = request.form['course_id']
            title = request.form['title']
            content = request.form['content']
            video_url = request.form.get('video_url', None)
            video_path = None
            file_path = None

            # Handle Video Upload
            if 'video_file' in request.files:
                video_file = request.files['video_file']
                if video_file and allowed_file(video_file.filename):
                    video_filename = secure_filename(video_file.filename)
                    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename).replace('\\', '/')
                    video_file.save(video_path)

            # Handle PDF Upload
            if 'pdf_file' in request.files:
                pdf_file = request.files['pdf_file']
                if pdf_file and allowed_file(pdf_file.filename):
                    pdf_filename = secure_filename(pdf_file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename).replace('\\', '/')
                    pdf_file.save(file_path)

            try:
                cursor.execute("""
                    INSERT INTO lessons (course_id, title, content, video_url, file_path, video_path)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (course_id, title, content, video_url, file_path, video_path))
                mysql.connection.commit()
                flash('Lesson added successfully!', 'success')
            except Exception as e:
                flash(f'Error adding lesson: {e}', 'danger')
                
                
        # Update Lesson
        elif 'update_lesson' in request.form:
            lesson_id = request.form['lesson_id']
            title = request.form['title']
            content = request.form['content']
            video_url = request.form.get('video_url', None)
            video_path = None
            file_path = None

            # Handle video upload
            if 'video_file' in request.files:
                video_file = request.files['video_file']
                if video_file and allowed_file(video_file.filename):
                    video_filename = secure_filename(video_file.filename)
                    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename).replace('\\', '/')
                    video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))

            # Handle PDF upload
            if 'pdf_file' in request.files:
                pdf_file = request.files['pdf_file']
                if pdf_file and allowed_file(pdf_file.filename):
                    pdf_filename = secure_filename(pdf_file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename).replace('\\', '/')
                    pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))
            try:
                cursor.execute("""
                    UPDATE lessons
                    SET title = %s, content = %s, video_url = %s, file_path = %s, video_path = %s
                    WHERE id = %s
                """, (title, content, video_url, file_path, video_path, lesson_id))
                mysql.connection.commit()
                flash('Lesson updated successfully!', 'success')
            except Exception as e:
                flash(f'Error updating lesson: {e}', 'danger')

        # Remove Lesson
        elif 'remove_lesson' in request.form:
            lesson_id = request.form['lesson_id']

            try:
                cursor.execute("DELETE FROM lessons WHERE id = %s", (lesson_id,))
                mysql.connection.commit()
                flash('Lesson removed successfully!', 'success')
            except Exception as e:
                flash(f'Error removing lesson: {e}', 'danger')

    # Fetch all lessons with course names
    cursor.execute("""
        SELECT lessons.id, lessons.title, lessons.content, lessons.video_url, lessons.file_path, lessons.video_path, courses.name
        FROM lessons
        JOIN courses ON lessons.course_id = courses.id
    """)
    lessons = cursor.fetchall()

    cursor.close()
    return render_template('admin_manage_lessons.html', lessons=lessons, courses=courses)

# Admin Manage course
@app.route('/admin/manage_courses', methods=['GET', 'POST'])
def admin_manage_courses():
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        # Add New Course
        if 'add_course' in request.form:
            name = request.form['name']
            description = request.form['description']
            try:
                cursor.execute("""
                    INSERT INTO courses (name, description)
                    VALUES (%s, %s)
                """, (name, description))
                mysql.connection.commit()
                flash('Course added successfully!', 'success')
            except Exception as e:
                flash(f'Error adding course: {e}', 'danger')

        # Update Assigned Teacher
        elif 'update_teacher' in request.form:
            course_id = request.form['course_id']
            teacher_id = request.form['teacher_id']
            try:
                cursor.execute("""
                    DELETE FROM teacher_course WHERE course_id = %s
                """, (course_id,))
                cursor.execute("""
                    INSERT INTO teacher_course (teacher_id, course_id)
                    VALUES (%s, %s)
                """, (teacher_id, course_id))
                mysql.connection.commit()
                flash('Teacher updated successfully!', 'success')
            except Exception as e:
                flash(f'Error updating teacher: {e}', 'danger')

        # Remove Course
        elif 'remove_course' in request.form:
            course_id = request.form['course_id']
            try:
                cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
                cursor.execute("DELETE FROM teacher_course WHERE course_id = %s", (course_id,))
                mysql.connection.commit()
                flash('Course removed successfully!', 'success')
            except Exception as e:
                flash(f'Error removing course: {e}', 'danger')

    # Fetch all courses with assigned teachers
    cursor.execute("""
        SELECT courses.id, courses.name, courses.description, 
               users.id AS teacher_id, users.username AS teacher_name
        FROM courses
        LEFT JOIN teacher_course ON courses.id = teacher_course.course_id
        LEFT JOIN users ON teacher_course.teacher_id = users.id
    """)
    courses = cursor.fetchall()

    # Fetch all teachers for the dropdown
    cursor.execute("""
        SELECT id, username FROM users WHERE role = 'teacher'
    """)
    teachers = cursor.fetchall()

    cursor.close()
    return render_template('admin_manage_courses.html', courses=courses, teachers=teachers)


# Assign teacher to course
@app.route('/admin/assign_teacher', methods=['GET', 'POST'])
def admin_assign_teacher():
    if session.get('role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Get the teacher and course IDs from the form
        teacher_id = request.form.get('teacher_id')
        course_id = request.form.get('course_id')

        if teacher_id and course_id:
            try:
                cursor = mysql.connection.cursor()
                # Insert into teacher_course table
                cursor.execute(
                    "INSERT INTO teacher_course (teacher_id, course_id) VALUES (%s, %s)",
                    (teacher_id, course_id)
                )
                mysql.connection.commit()
                flash("Teacher assigned to course successfully!", "success")
            except Exception as e:
                # Check if it's a duplicate entry error
                if "Duplicate entry" in str(e):
                    flash("This teacher is already assigned to this course.", "error")
                else:
                    flash(f"Error assigning teacher: {str(e)}", "error")
            finally:
                cursor.close()
        else:
            flash("Please select both a teacher and a course.", "warning")

        return redirect(url_for('admin_dashboard'))

    # Fetch teachers and courses to display in the form
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username FROM users WHERE role = 'teacher'")
    teachers = cursor.fetchall()

    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()
    cursor.close()

    return render_template('admin_assign_teacher.html', teachers=teachers, courses=courses)



#Teacher dashboard
@app.route('/teacher/dashboard')
def teacher_dashboard():
    if session.get('role') != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    teacher_id = session.get('user_id')  # Get the teacher's user ID from the session
    print(f"Teacher ID from session: {teacher_id}")  # Debugging log

    try:
        cursor = mysql.connection.cursor()
        
        # Fetch courses assigned to the teacher
        cursor.execute("""
            SELECT courses.id, courses.name 
            FROM teacher_course 
            JOIN courses ON teacher_course.course_id = courses.id 
            WHERE teacher_course.teacher_id = %s
        """, (teacher_id,))
        assigned_courses = cursor.fetchall()

        # Debugging log for assigned courses
        print(f"Assigned courses: {assigned_courses}")

        # Format the result for the template as a list of dictionaries for easier handling
        assigned_courses = [{'id': course[0], 'name': course[1], 'assignments': []} for course in assigned_courses]

        # Fetch assignments for each course
        for course in assigned_courses:
            course_id = course['id']
            cursor.execute("""
                SELECT id, title 
                FROM assignments 
                WHERE course_id = %s
            """, (course_id,))
            course['assignments'] = cursor.fetchall()

        cursor.close()

    except Exception as e:
        flash(f'Error loading courses: {str(e)}', 'danger')
        assigned_courses = []

    return render_template('teacher_dashboard.html', assigned_courses=assigned_courses)

#CRUD operations for teacher
@app.route('/teacher/manage_lessons/<int:course_id>', methods=['GET', 'POST'])
def teacher_manage_lessons(course_id):
    if session.get('role') != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    # Fetch all courses
    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()

    # Handle form submission
    if request.method == 'POST':
        # Add Lesson
        if 'add_lesson' in request.form:
            course_id = request.form['course_id']
            title = request.form['title']
            content = request.form['content']
            video_url = request.form.get('video_url', None)
            video_path = None
            file_path = None

            # Handle Video Upload
            if 'video_file' in request.files:
                video_file = request.files['video_file']
                if video_file and allowed_file(video_file.filename):
                    video_filename = secure_filename(video_file.filename)
                    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename).replace('\\', '/')
                    video_file.save(video_path)

            # Handle PDF Upload
            if 'pdf_file' in request.files:
                pdf_file = request.files['pdf_file']
                if pdf_file and allowed_file(pdf_file.filename):
                    pdf_filename = secure_filename(pdf_file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename).replace('\\', '/')
                    pdf_file.save(file_path)

            try:
                cursor.execute("""
                    INSERT INTO lessons (course_id, title, content, video_url, file_path, video_path)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (course_id, title, content, video_url, file_path, video_path))
                mysql.connection.commit()
                flash('Lesson added successfully!', 'success')
            except Exception as e:
                flash(f'Error adding lesson: {e}', 'danger')
                
                
        # Update Lesson
        elif 'update_lesson' in request.form:
            lesson_id = request.form['lesson_id']
            title = request.form['title']
            content = request.form['content']
            video_url = request.form.get('video_url', None)
            video_path = None
            file_path = None

            # Handle video upload
            if 'video_file' in request.files:
                video_file = request.files['video_file']
                if video_file and allowed_file(video_file.filename):
                    video_filename = secure_filename(video_file.filename)
                    video_path = os.path.join('uploads', video_filename).replace('\\', '/')
                    video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))

            # Handle PDF upload
            if 'pdf_file' in request.files:
                pdf_file = request.files['pdf_file']
                if pdf_file and allowed_file(pdf_file.filename):
                    pdf_filename = secure_filename(pdf_file.filename)
                    file_path = os.path.join('uploads', pdf_filename).replace('\\', '/')
                    pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))
            try:
                cursor.execute("""
                    UPDATE lessons
                    SET title = %s, content = %s, video_url = %s, file_path = %s, video_path = %s
                    WHERE id = %s
                """, (title, content, video_url, file_path, video_path, lesson_id))
                mysql.connection.commit()
                flash('Lesson updated successfully!', 'success')
            except Exception as e:
                flash(f'Error updating lesson: {e}', 'danger')

        # Remove Lesson
        elif 'remove_lesson' in request.form:
            lesson_id = request.form['lesson_id']

            try:
                cursor.execute("DELETE FROM lessons WHERE id = %s", (lesson_id,))
                mysql.connection.commit()
                flash('Lesson removed successfully!', 'success')
            except Exception as e:
                flash(f'Error removing lesson: {e}', 'danger')

    # Fetch all lessons with course names
    cursor.execute("""
        SELECT lessons.id, lessons.title, lessons.content, lessons.video_url, lessons.file_path, lessons.video_path, courses.name
        FROM lessons
        JOIN courses ON lessons.course_id = courses.id
    """)
    lessons = cursor.fetchall()

    cursor.close()

    return render_template('teacher_manage_lessons.html', lessons=lessons,  course_id=course_id)

#Teacher create assignment
@app.route('/teacher/create_assignment/<int:course_id>', methods=['GET', 'POST'])
def create_assignment(course_id):
    if session.get('role') != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    assignment = {'title': '', 'description': ''}  # Default empty values
    question_count = 0

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        created_by = session['user_id']

        # Handle image uploads (if any)
        image_paths = []
        if 'assignment_images' in request.files:
            images = request.files.getlist('assignment_images')
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(image_path)
                    image_paths.append(image_path)

        try:
            cursor = mysql.connection.cursor()

            # Insert assignment into the database
            cursor.execute("""
                INSERT INTO assignments (title, description, course_id, created_by)
                VALUES (%s, %s, %s, %s)
            """, (title, description, course_id, created_by))
            mysql.connection.commit()
            assignment_id = cursor.lastrowid

            print(f"Assignment ID: {assignment_id}")  # Debug log

            # Insert image paths into the assignment_images table
            for image_path in image_paths:
                cursor.execute("""
                    INSERT INTO assignment_images (assignment_id, image_path)
                    VALUES (%s, %s)
                """, (assignment_id, image_path))

            # Insert questions for this assignment
            question_count = int(request.form['question_count'])
            for question_num in range(1, question_count + 1):
                question_type = request.form[f'question_type_{question_num}']
                question_text = request.form[f'question_text_{question_num}']
                correct_answer = request.form[f'correct_answer_{question_num}']
                option_a = request.form.get(f'option_a_{question_num}')
                option_b = request.form.get(f'option_b_{question_num}')
                option_c = request.form.get(f'option_c_{question_num}')
                option_d = request.form.get(f'option_d_{question_num}')

                print(f"Question Data: {question_type}, {question_text}, {correct_answer}, {option_a}, {option_b}, {option_c}, {option_d}")  # Debug log

                # Insert the question into the questions table
                cursor.execute("""
                    INSERT INTO questions (assignment_id, question_type, question_text, correct_answer, option_a, option_b, option_c, option_d)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (assignment_id, question_type, question_text, correct_answer, option_a, option_b, option_c, option_d))

            mysql.connection.commit()
            flash('Assignment created successfully!', 'success')

        except Exception as e:
            mysql.connection.rollback()  # Rollback changes in case of error
            flash(f'Error creating assignment: {str(e)}', 'danger')
        finally:
            cursor.close()

        return redirect(url_for('teacher_dashboard'))

    return render_template('create_assignment.html', course_id=course_id, assignment=assignment, question_count=question_count)

#Teacher manage assignment
# Manage Assignments
@app.route('/teacher/manage_assignments/<int:course_id>')
def manage_assignments(course_id):
    if session.get('role') != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT id, title, description FROM assignments WHERE course_id = %s""", (course_id,))
    assignments = cursor.fetchall()
    cursor.close()

    return render_template('manage_assignments.html', course_id=course_id, assignments=assignments)



# For editing an assignment
@app.route('/teacher/edit_assignment/<int:course_id>/<int:assignment_id>', methods=['GET', 'POST'])
def edit_assignment(course_id, assignment_id):
    if session.get('role') != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    questions = []

    try:
        if request.method == 'POST':
            # Handle updating or adding new questions
            question_count = int(request.form['question_count'])
            for i in range(1, question_count + 1):
                question_id = request.form.get(f'question_id_{i}')
                question_text = request.form.get(f'question_text_{i}')
                question_type = request.form.get(f'question_type_{i}')
                correct_answer = request.form.get(f'correct_answer_{i}')
                option_a = request.form.get(f'option_a_{i}')
                option_b = request.form.get(f'option_b_{i}')
                option_c = request.form.get(f'option_c_{i}')
                option_d = request.form.get(f'option_d_{i}')

                if question_id:
                    # Update existing question
                    cursor.execute("""
                        UPDATE questions
                        SET question_text = %s, question_type = %s, correct_answer = %s,
                            option_a = %s, option_b = %s, option_c = %s, option_d = %s
                        WHERE id = %s
                    """, (question_text, question_type, correct_answer, option_a, option_b, option_c, option_d, question_id))
                else:
                    # Insert new question
                    cursor.execute("""
                        INSERT INTO questions (assignment_id, question_text, question_type, correct_answer, option_a, option_b, option_c, option_d)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (assignment_id, question_text, question_type, correct_answer, option_a, option_b, option_c, option_d))

            mysql.connection.commit()

        # Fetch all questions for this assignment
        cursor.execute("SELECT * FROM questions WHERE assignment_id = %s", [assignment_id])
        questions = cursor.fetchall()

    finally:
        cursor.close()

    return render_template('edit_assignment.html', course_id=course_id, assignment_id=assignment_id, questions=questions)






# For deleting an assignment
@app.route('/teacher/remove_assignment/<int:assignment_id>', methods=['POST'])
def remove_assignment(assignment_id):
    if session.get('role') != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    try:
        # Delete assignment images
        cursor.execute("DELETE FROM assignment_images WHERE assignment_id = %s", (assignment_id,))
        # Delete assignment questions
        cursor.execute("DELETE FROM questions WHERE assignment_id = %s", (assignment_id,))
        # Delete the assignment
        cursor.execute("DELETE FROM assignments WHERE id = %s", (assignment_id,))
        mysql.connection.commit()
        flash('Assignment removed successfully!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f'Error removing assignment: {str(e)}', 'danger')
    finally:
        cursor.close()

    return redirect(url_for('manage_assignments', course_id=session.get('course_id')))




#Teacher view assignment submission
# Route to view submissions
@app.route('/teacher/view_student_submissions/<int:assignment_id>/<int:course_id>', methods=['GET'])
def view_student_submissions(assignment_id, course_id):
    if session.get('role') != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    
    try:
        # Fetch submissions for the specific assignment and course
        cursor.execute("""
            SELECT grades.student_id, grades.grade, grades.feedback, grades.created_at
            FROM grades
            WHERE grades.assignment_id = %s
        """, [assignment_id])
        submissions = cursor.fetchall()

        # Render the view with submissions and course details
        return render_template('view_student_submissions.html', submissions=submissions, course_id=course_id)

    finally:
        cursor.close()





# Manage Student Answers
# Route to update submission
@app.route('/teacher/update_student_submission/<int:course_id>/<int:assignment_id>/<int:student_id>', methods=['GET', 'POST'])
def update_student_submission(assignment_id, student_id):
    if session.get('role') != 'teacher':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    submission = {}
    questions = []

    try:
        if request.method == 'POST':
            # Update the grade and feedback
            grade = request.form.get('grade')
            feedback = request.form.get('feedback')

            # Update grade and feedback in the grades table
            cursor.execute("""
                UPDATE grades
                SET grade = %s, feedback = %s
                WHERE assignment_id = %s AND student_id = %s
            """, (grade, feedback, assignment_id, student_id))

            # Update answers for each question
            question_count = int(request.form['question_count'])
            for i in range(1, question_count + 1):
                answer_id = request.form.get(f'answer_id_{i}')
                answer_text = request.form.get(f'answer_{i}')
                
                if answer_id:
                    # Update existing answer
                    cursor.execute("""
                        UPDATE student_answers
                        SET answer = %s
                        WHERE id = %s
                    """, (answer_text, answer_id))
                else:
                    # Insert new answer
                    question_id = request.form.get(f'question_id_{i}')
                    cursor.execute("""
                        INSERT INTO student_answers (student_id, assignment_id, question_id, answer)
                        VALUES (%s, %s, %s, %s)
                    """, (student_id, assignment_id, question_id, answer_text))

            mysql.connection.commit()

        # Fetch current student submission and answers for the assignment
        cursor.execute("""
            SELECT sa.id AS answer_id, sa.question_id, sa.answer
            FROM student_answers sa
            WHERE sa.student_id = %s AND sa.assignment_id = %s
        """, (student_id, assignment_id))
        
        submission['answers'] = cursor.fetchall()

        # Fetch all questions for this assignment
        cursor.execute("SELECT * FROM questions WHERE assignment_id = %s", [assignment_id])
        questions = cursor.fetchall()

        # Fetch the grade and feedback for the student
        cursor.execute("""
            SELECT grade, feedback
            FROM grades
            WHERE student_id = %s AND assignment_id = %s
        """, (student_id, assignment_id))
        
        grade_data = cursor.fetchone()
        submission['grade'] = grade_data['grade'] if grade_data else None
        submission['feedback'] = grade_data['feedback'] if grade_data else None

    finally:
        cursor.close()

    return render_template('update_student_submission.html', submission=submission, questions=questions, assignment_id=assignment_id, student_id=student_id)





# Student dashboard
@app.route('/student/dashboard')
def student_dashboard():
    if session.get('role') != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    student_id = session['user_id']

    # Fetch enrolled courses for the student
    cursor.execute("""
        SELECT courses.id 
        FROM enrollments 
        JOIN courses ON enrollments.course_id = courses.id
        WHERE enrollments.user_id = %s
    """, (student_id,))
    enrolled_course_ids = [course[0] for course in cursor.fetchall()]

    # Fetch all available courses excluding enrolled ones
    if enrolled_course_ids:
        cursor.execute("""
            SELECT courses.id, courses.name, users.username AS teacher
            FROM courses
            JOIN teacher_course ON courses.id = teacher_course.course_id
            JOIN users ON teacher_course.teacher_id = users.id
            WHERE courses.id NOT IN %s
        """, (tuple(enrolled_course_ids),))
    else:
        cursor.execute("""
            SELECT courses.id, courses.name, users.username AS teacher
            FROM courses
            JOIN teacher_course ON courses.id = teacher_course.course_id
            JOIN users ON teacher_course.teacher_id = users.id
        """)
    courses = cursor.fetchall()

    # Fetch enrolled courses with teacher details
    cursor.execute("""
        SELECT courses.id, courses.name, users.username AS teacher
        FROM enrollments
        JOIN courses ON enrollments.course_id = courses.id
        JOIN teacher_course ON courses.id = teacher_course.course_id
        JOIN users ON teacher_course.teacher_id = users.id
        WHERE enrollments.user_id = %s
    """, (student_id,))
    enrolled_courses = cursor.fetchall()

    # Fetch assignments for each enrolled course
    assignments_by_course = {}
    for course in enrolled_courses:
        cursor.execute("""
            SELECT id, title 
            FROM assignments 
            WHERE course_id = %s
        """, (course[0],))
        assignments_by_course[course[0]] = cursor.fetchall()

    cursor.close()

    return render_template(
        'student_dashboard.html',
        courses=courses,
        enrolled_courses=enrolled_courses,
        assignments_by_course=assignments_by_course
    )





# Common function for handling enrollment
def handle_enrollment(course_id, student_id):
    cursor = mysql.connection.cursor()

    # Check if the student is already enrolled in this course
    cursor.execute("SELECT * FROM enrollments WHERE user_id = %s AND course_id = %s", (student_id, course_id))
    enrollment = cursor.fetchone()

    if enrollment:
        flash('You are already enrolled in this course!', 'warning')
    else:
        # Enroll the student in the course
        cursor.execute("INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)", (student_id, course_id))
        mysql.connection.commit()
        flash('Enrollment successful!', 'success')

    cursor.close()

# Student join course
@app.route('/student/join_course', methods=['POST'])
def student_join_course():
    if session.get('role') != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    course_id = request.form['course_id']
    student_id = session['user_id']

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO enrollments (course_id, user_id)
            VALUES (%s, %s)
        """, (course_id, student_id))
        mysql.connection.commit()
        flash('Course joined successfully!', 'success')
    except Exception as e:
        flash(f'Error joining course: {str(e)}', 'danger')
    finally:
        cursor.close()

    return redirect(url_for('student_dashboard'))

# Enroll route for enrolling in a course
@app.route('/enroll/<int:course_id>', methods=['POST'])
def enroll(course_id):
    if session.get('role') != 'student':
        flash('Access denied. Only students can enroll in courses.', 'danger')
        return redirect(url_for('login'))

    student_id = session.get('user_id')  # using consistent 'user_id'

    try:
        handle_enrollment(course_id, student_id)
    except Exception as e:
        flash(f'Error enrolling in course: {str(e)}', 'danger')

    return redirect(url_for('student_dashboard'))




# Student view lesson 
@app.route('/student/lessons/<int:course_id>')
def student_lessons(course_id):
    if session.get('role') != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    # Check if the student is enrolled in the course
    student_id = session['user_id']
    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT 1 
        FROM enrollments 
        WHERE user_id = %s AND course_id = %s
    """, (student_id, course_id))
    enrollment = cursor.fetchone()

    if not enrollment:
        flash('You are not enrolled in this course.', 'danger')
        return redirect(url_for('student_dashboard'))

    # Fetch lessons for the course
    cursor.execute("""
        SELECT id, title, content, video_url, file_path, video_path
        FROM lessons
        WHERE course_id = %s
    """, (course_id,))
    lessons = cursor.fetchall()

    # Manually convert the tuple into a dictionary
    lessons_dict = []
    for lesson in lessons:
        lesson_dict = {
            'id': lesson[0],
            'title': lesson[1],
            'content': lesson[2],
            'video_url': lesson[3],
            'file_path': lesson[4],
            'video_path': lesson[5]
        }
        lessons_dict.append(lesson_dict)

    cursor.close()

    return render_template('student_lessons.html', lessons=lessons_dict, course_id=course_id)

#student submit assignment
@app.route('/student/assignment/<int:assignment_id>', methods=['POST', 'GET'])
def submit_assignment(assignment_id):
    if session.get('role') != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()

    # Fetch the assignment details
    cursor.execute("""
        SELECT id, title, description FROM assignments WHERE id = %s
    """, (assignment_id,))
    assignment = cursor.fetchone()

    # Fetch assignment images (if any)
    cursor.execute("""
        SELECT image_path FROM assignment_images WHERE assignment_id = %s
    """, (assignment_id,))
    images = cursor.fetchall()

    # Ensure image paths are formatted correctly with forward slashes
    images = [image[0].replace("\\", "/") for image in images]

    # Fetch the questions for this assignment
    cursor.execute("""
        SELECT id, question_type, question_text, correct_answer, option_a, option_b, option_c, option_d
        FROM questions WHERE assignment_id = %s
    """, (assignment_id,))
    questions = cursor.fetchall()

    if request.method == 'POST':
        # Fetch the total number of questions for the assignment
        cursor.execute("""
            SELECT COUNT(*) FROM questions WHERE assignment_id = %s
        """, (assignment_id,))
        total_questions = cursor.fetchone()[0]

        # Points per question
        points_per_question = 20.00 / total_questions

        correct_answers_count = 0
        for question in questions:
            question_id = question[0]
            question_type = question[1]
            correct_answer = question[3].strip().lower()  # Correct answer from DB
            answer = request.form.get(f'answer_{question_id}')

            # Handle answer based on question type (MCQ or FIB)
            if question_type == 'MCQ':
                # For MCQ, check the selected option
                if answer and answer.strip().lower() == correct_answer.lower():
                    correct_answers_count += 1
            elif question_type == 'FIB':
                # For FIB, compare the text answer
                if answer and answer.strip().lower() == correct_answer.lower():
                    correct_answers_count += 1

            # Store the student's answer (whether correct or not)
            cursor.execute("""
                INSERT INTO student_answers (student_id, assignment_id, question_id, answer)
                VALUES (%s, %s, %s, %s)
            """, (session['user_id'], assignment_id, question_id, answer))

        # Calculate grade
        grade = correct_answers_count * points_per_question

        # Ensure the grade does not exceed 20
        if grade > 20.00:
            grade = 20.00

        feedback = "Well done!" if grade == 20.00 else "Keep trying! Check your answers."

        # Insert grade into the grades table
        cursor.execute("""
            INSERT INTO grades (student_id, assignment_id, grade, feedback, graded_by)
            VALUES (%s, %s, %s, %s, %s)
        """, (session['user_id'], assignment_id, grade, feedback, None))

        # Commit the transaction
        mysql.connection.commit()

        flash('Your assignment has been graded and submitted!', 'success')
        cursor.close()
        return redirect(url_for('student_dashboard'))  # Redirect to the student's dashboard after submission

    # If GET request, just render the template with assignment and question data
    cursor.close()
    return render_template('submit_assignment.html', assignment=assignment, questions=questions, assignment_images=images)




#student view grade
@app.route('/student/grades', methods=['GET'])
def student_grades():
    if session.get('role') != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('login'))

    student_id = session['user_id']

    cursor = mysql.connection.cursor()

    # Fetch all assignments and grades for the logged-in student
    cursor.execute("""
        SELECT a.title, g.grade, g.feedback, a.id 
        FROM assignments a
        JOIN grades g ON a.id = g.assignment_id
        WHERE g.student_id = %s
    """, (student_id,))

    grades = cursor.fetchall()
    cursor.close()

    return render_template('student_grades.html', grades=grades)



if __name__ == '__main__':
    app.run(debug=True)
