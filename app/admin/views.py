from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from . import admin
from .forms import SubjectForm, StudentAssignForm, TaskForm
from .. import db
from ..models import Subject, Student, Task



def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Subject Views


@admin.route('/subjects', methods=['GET', 'POST'])
@login_required
def list_subjects():
    """
    List all subjects
    """
    check_admin()

    subjects = Subject.query.all()

    return render_template('admin/subjects/subjects.html', subjects=subjects, title="Subjects")


@admin.route('/subjects/add', methods=['GET', 'POST'])
@login_required
def add_subject():
    """
    Add a subject to the database
    """
    check_admin()

    add_subject = True

    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data,description=form.description.data)
        try:
            
            db.session.add(subject)
            db.session.commit()
            flash('You have successfully added a new subject.')
        except:
         
            flash('Error: subject name already exists.')

   
        return redirect(url_for('admin.list_subjects'))

    return render_template('admin/subjects/subject.html', action="Add", add_subject=add_subject, form=form,title="Add Subject")


@admin.route('/subjects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
    """
    Edit a subject
    """
    check_admin()

    add_subject = False

    subject = Subject.query.get_or_404(id)
    form = SubjectForm(obj=subject)
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the subject.')

        
        return redirect(url_for('admin.list_subjects'))

    form.description.data = subject.description
    form.name.data = subject.name
    return render_template('admin/subjects/subject.html', action="Edit",add_subject=add_subject, form=form,subject=subject, title="Edit Subject")


@admin.route('/subjects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_subject(id):
    """
    Delete a subject from the database
    """
    check_admin()

    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash('You have successfully deleted the subject.')

    
    return redirect(url_for('admin.list_subjects'))

    return render_template(title="Delete Subject")

@admin.route('/tasks')
@login_required
def list_tasks():
    check_admin()
    """
    List all tasks
    """
    tasks = Task.query.all()
    return render_template('admin/tasks/tasks.html',tasks=tasks, title='Tasks')


@admin.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    """
    Add a task to the database
    """
    check_admin()

    add_task = True

    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data,description=form.description.data)

        try:
           
            db.session.add(task)
            db.session.commit()
            flash('You have successfully added a new task.')
        except:
           
            flash('Error: task already exists.')

       
        return redirect(url_for('admin.list_tasks'))

    
    return render_template('admin/tasks/task.html', add_task=add_task,form=form, title='Add Task')


@admin.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    """
    Edit a task
    """
    check_admin()

    add_task = False

    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.name = form.name.data
        task.description = form.description.data
        db.session.add(task)
        db.session.commit()
        flash('You have successfully edited the Task.')

        # redirect to the tasks page
        return redirect(url_for('admin.list_tasks'))

    form.description.data = task.description
    form.name.data = task.name
    return render_template('admin/tasks/task.html', add_task=add_task,form=form, title="Edit Task")


@admin.route('/tasks/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    """
    Delete a role from the database
    """
    check_admin()

    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('You have successfully deleted the Task.')

    # redirect to the tasks page
    return redirect(url_for('admin.list_tasks'))

    return render_template(title="Delete Task")

@admin.route('/students')
@login_required
def list_students():
    """
    List all students
    """
    check_admin()

    students = Student.query.all()
    return render_template('admin/students/students.html',students=students, title='students')


@admin.route('/students/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_student(id):
    """
    Assign a subject and a task to a student
    """
    check_admin()

    student = Student.query.get_or_404(id)

    # prevent admin from being assigned a subject or task
    if student.is_admin:
        abort(403)

    form = StudentAssignForm(obj=student)
    if form.validate_on_submit():
        student.subject = form.subject.data
        student.task = form.task.data
        db.session.add(student)
        db.session.commit()
        flash('You have successfully assigned a subject and task.')

        # redirect to the tasks page
        return redirect(url_for('admin.list_students'))

    return render_template('admin/students/student.html',student=student, form=form,title='Assign Student')