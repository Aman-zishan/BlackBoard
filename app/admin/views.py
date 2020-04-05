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


# Department Views


@admin.route('/subjects', methods=['GET', 'POST'])
@login_required
def list_subjects():
    """
    List all departments
    """
    check_admin()

    subjects = Subject.query.all()

    return render_template('admin/departments/departments.html', subjects=subjects, title="Subjects")


@admin.route('/subjects/add', methods=['GET', 'POST'])
@login_required
def add_subject():
    """
    Add a department to the database
    """
    check_admin()

    add_subject = True

    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data,description=form.description.data)
        try:
            # add department to the database
            db.session.add(subject)
            db.session.commit()
            flash('You have successfully added a new subject.')
        except:
            # in case department name already exists
            flash('Error: subject name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_subjects'))

    # load department template
    return render_template('admin/departments/department.html', action="Add", add_subject=add_subject, form=form,title="Add Subject")


@admin.route('/subjects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
    """
    Edit a department
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

        # redirect to the departments page
        return redirect(url_for('admin.list_departments'))

    form.description.data = subject.description
    form.name.data = subject.name
    return render_template('admin/departments/department.html', action="Edit",add_department=add_department, form=form,department=department, title="Edit Department")


@admin.route('/subjects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_subject(id):
    """
    Delete a department from the database
    """
    check_admin()

    subject = Subject.query.get_or_404(id)
    db.session.delete(sunject)
    db.session.commit()
    flash('You have successfully deleted the subject.')

    # redirect to the departments page
    return redirect(url_for('admin.list_subjects'))

    return render_template(title="Delete Subject")

@admin.route('/tasks')
@login_required
def list_tasks():
    check_admin()
    """
    List all roles
    """
    tasks = Task.query.all()
    return render_template('admin/roles/roles.html',tasks=tasks, title='Tasks')


@admin.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    """
    Add a role to the database
    """
    check_admin()

    add_task = True

    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data,description=form.description.data)

        try:
            # add role to the database
            db.session.add(task)
            db.session.commit()
            flash('You have successfully added a new task.')
        except:
            # in case role name already exists
            flash('Error: task already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_tasks'))

    # load role template
    return render_template('admin/roles/role.html', add_task=add_task,form=form, title='Add Task')


@admin.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    """
    Edit a role
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

        # redirect to the roles page
        return redirect(url_for('admin.list_tasks'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_task=add_task,form=form, title="Edit Task")


@admin.route('/tasks/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    """
    Delete a role from the database
    """
    check_admin()

    task = Task.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the Task.')

    # redirect to the roles page
    return redirect(url_for('admin.list_tasks'))

    return render_template(title="Delete Task")

@admin.route('/students')
@login_required
def list_students():
    """
    List all employees
    """
    check_admin()

    students = Student.query.all()
    return render_template('admin/employees/employees.html',students=students, title='students')


@admin.route('/students/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_student(id):
    """
    Assign a department and a role to an employee
    """
    check_admin()

    student = Student.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if student.is_admin:
        abort(403)

    form = StudentAssignForm(obj=student)
    if form.validate_on_submit():
        student.subject = form.subject.data
        student.task = form.task.data
        db.session.add(student)
        db.session.commit()
        flash('You have successfully assigned a subject and task.')

        # redirect to the roles page
        return redirect(url_for('admin.list_students'))

    return render_template('admin/employees/employee.html',student=student, form=form,title='Assign Student')