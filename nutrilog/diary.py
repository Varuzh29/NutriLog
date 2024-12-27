from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app as app, send_from_directory, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from nutrilog.auth import login_required
from nutrilog.db import get_db
from nutrilog.modules.bmi_calculator import calculate_bmi
from nutrilog.modules.img_upload import upload_img
import os

bp = Blueprint('diary', __name__)


@bp.route('/')
@login_required
def index():

    bmi = calculate_bmi(g.user['weight'], g.user['height'])

    db = get_db()

    water_intake_in_last_24_hours = 0
    water_intake_in_last_24_hours = db.execute(
        "SELECT SUM(volume) FROM water_intake WHERE user_id = ? AND time >= datetime('now', '-24 hour')",
        (g.user['id'],)
    ).fetchall()[0]["SUM(volume)"]
    try:
        water_intake_in_last_24_hours = round(water_intake_in_last_24_hours, 2)
    except TypeError:
        water_intake_in_last_24_hours = 0
    water_intake_goal = g.user['water_intake_goal']

    calories_goal = g.user['kcal_goal']

    food_intake_in_last_24_hours = db.execute(
        "SELECT food_item_id, portion_weight, portions FROM food_intake WHERE user_id = ? AND time >= datetime('now', '-24 hour')",
        (g.user['id'],)
    ).fetchall()

    calories_in_last_24_hours = 0

    for food_intake in food_intake_in_last_24_hours:
        intake_weight = food_intake["portion_weight"] * food_intake["portions"]
        food_item = db.execute(
            "SELECT kcal FROM food_items WHERE id = ?",
            (food_intake["food_item_id"],)
        ).fetchall()[0]
        intake_calories = (food_item["kcal"] / 100) * intake_weight
        calories_in_last_24_hours += intake_calories

    print(calories_in_last_24_hours)

    return render_template('diary/index.html',
                           bmi=bmi["index"],
                           interpretation=bmi["interpretation"],
                           water_intake_in_last_24_hours=water_intake_in_last_24_hours,
                           water_intake_goal=water_intake_goal,
                           calories_goal=calories_goal,
                           calories_in_last_24_hours=calories_in_last_24_hours)


@bp.route('/measurements', methods=('GET', 'POST'))
@login_required
def measurements():
    user_weight = g.user['weight']
    user_height = g.user['height']
    error = None
    if request.method == 'POST':
        weight = request.form['weight']
        height = request.form['height']

        if not weight or not height:
            error = 'Weight and height are required'
        try:
            weight = float(weight)
            height = float(height)
        except ValueError:
            error = 'Weight and height must be numbers'
        if weight < 0 or height < 0:
            error = 'Please enter positive numbers'

        if error is None and (user_height != height or user_weight != weight):
            db = get_db()
            db.execute(
                'UPDATE user SET weight = ?, height = ? WHERE id = ?',
                (weight, height, g.user['id'])
            )
            db.commit()
        elif error is not None:
            flash(error)
            return redirect(url_for('diary.measurements'))

        return redirect(url_for('diary.index'))

    return render_template('diary/measurements.html', weight=user_weight, height=user_height)


@bp.route('/goals', methods=('GET', 'POST'))
@login_required
def goals():
    user_kcal_goal = g.user['kcal_goal']
    user_water_intake_goal = g.user['water_intake_goal']
    user_weigth_goal = g.user['weight_goal']
    error = None

    if request.method == 'POST':
        kcal_goal = request.form['kcal_goal']
        water_intake_goal = request.form['water_intake_goal']
        weight_goal = request.form['weight_goal']

        if not kcal_goal or not water_intake_goal or not weight_goal:
            error = 'Kcal, water intake and weight are required'
        try:
            kcal_goal = float(kcal_goal)
            water_intake_goal = float(water_intake_goal)
            weight_goal = float(weight_goal)
        except ValueError:
            error = 'Kcal, water intake and weight must be numbers'

        if kcal_goal < 0 or water_intake_goal < 0 or weight_goal < 0:
            error = 'Please enter positive numbers'

        if error is None:
            if user_kcal_goal != kcal_goal or user_water_intake_goal != water_intake_goal or user_weigth_goal != weight_goal:
                db = get_db()
                db.execute(
                    'UPDATE user SET kcal_goal = ?, water_intake_goal = ?, weight_goal = ? WHERE id = ?',
                    (kcal_goal, water_intake_goal, weight_goal, g.user['id'])
                )
                db.commit()
        elif error is not None:
            flash(error)
            return redirect(url_for('diary.goals'))

        return redirect(url_for('diary.index'))

    return render_template('diary/goals.html')


@bp.route('/food_items', methods=('GET', 'POST'))
@login_required
def food_items():
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        protein = request.form['protein']
        fat = request.form['fat']
        carbs = request.form['carbs']
        calories = request.form['calories']
        img_url = None
        error = None
        if 'image' in request.files:
            image = request.files['image']
            img_url, img_error = upload_img(image)
            if img_error is not None:
                error = img_error
        if not name or not protein or not fat or not carbs or not calories:
            error = 'All fields are required'
        try:
            protein = float(protein)
            fat = float(fat)
            carbs = float(carbs)
            calories = int(calories)
        except ValueError:
            error = 'Protein, fat, carbs and calories must be numbers'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'INSERT INTO food_items (name, kcal, protein, fat, carbohydrates, image_url) VALUES (?, ?, ?, ?, ?, ?)',
                (name.lower(), calories, protein, fat, carbs, img_url)
            )
            db.commit()
            return redirect(url_for('diary.food_items'))

    food_items = db.execute(
        'SELECT name, kcal, protein, fat, carbohydrates, image_url FROM food_items LIMIT 25').fetchall()

    return render_template('diary/food_items.html', food_items=food_items)


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirmation = request.form['confirmation']
        error = None
        if not old_password or not new_password or not confirmation:
            error = 'All fields are required'
        elif not check_password_hash(g.user['password'], old_password):
            error = 'Incorrect password'
        elif new_password != confirmation:
            error = 'Password does not match confirmation'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE user SET password = ? WHERE id = ?',
                (generate_password_hash(new_password), g.user['id'])
            )
            db.commit()
            return redirect(url_for('auth.login'))

    return render_template('diary/settings.html')


@bp.route('/add_water_intake', methods=('GET', 'POST'))
@login_required
def add_water_intake():
    db = get_db()
    if request.method == 'POST':
        volume = request.form['volume']
        error = None
        if not volume:
            error = 'Volume is required'
        else:
            try:
                volume = float(volume)
            except ValueError:
                error = 'Volume must be a number'
            if volume < 0:
                error = 'volume must be positive'

        if error is None:
            db.execute(
                'INSERT INTO water_intake (user_id, volume) VALUES (?, ?)',
                (g.user['id'], volume)
            )
            db.commit()
        else:
            flash(error)

        return redirect(url_for('diary.index'))

    water_records = db.execute(
        'SELECT time, volume FROM water_intake WHERE user_id = ? ORDER BY time DESC LIMIT 25',
        (g.user['id'],)
    ).fetchall()

    for record in water_records:
        print(record['time'])

    return render_template('diary/add_water_intake.html', water_records=water_records)


@bp.route('/add_food_intake', methods=('GET', 'POST'))
@login_required
def add_food_intake():
    if request.method == 'POST':
        food_item_id = request.form['food_item_id']
        portion_weight = request.form['portion_weight']
        portions = request.form['portions']
        error = None

        if not food_item_id or not portion_weight or not portions:
            error = 'All fields are required'
        else:
            try:
                portion_weight = int(portion_weight)
                portions = int(portions)
                if portion_weight < 0 or portions < 0:
                    error = 'Portion weight and portions must be positive'
            except ValueError:
                error = 'Portion weight and portions must be numbers'

        if error is None:
            db = get_db()
            db.execute(
                'INSERT INTO food_intake (user_id, food_item_id, portion_weight, portions) VALUES (?, ?, ?, ?)',
                (g.user['id'], food_item_id, portion_weight, portions)
            )
            db.commit()
        else:
            flash(error)

        return redirect(url_for('diary.index'))

    return render_template('diary/add_food_intake.html')


@bp.route('/upload/img/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.instance_path, app.config['IMG_UPLOAD_PATH']), filename)


@bp.route('/find_food_item')
@login_required
def find_food_item():
    query = request.args.get('q')
    if not query:
        return None

    db = get_db()
    food_items = db.execute(
        'SELECT id, name, kcal, protein, fat, carbohydrates, image_url FROM food_items WHERE name LIKE ? LIMIT 25',
        (f'%{query}%',)
    ).fetchall()

    result = []

    for food_item in food_items:
        result.append({
            'name': food_item['name'].title(),
            'kcal': food_item['kcal'],
            'protein': food_item['protein'],
            'fat': food_item['fat'],
            'carbohydrates': food_item['carbohydrates'],
            'image_url': food_item['image_url'] or url_for('static', filename='icons/no_food_img.svg'),
            'id': food_item['id']
        })

    return result
