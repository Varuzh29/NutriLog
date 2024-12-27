# NutriLog
#### Video Demo: https://youtu.be/o7nescUFyH8
#### Description:
NutriLog is a food diary application designed to assist users in monitoring their dietary habits and achieving their nutritional goals. The application is built to provide a comprehensive platform for logging daily food intake, tracking calorie consumption, and managing hydration and weight. With features that calculate and display BMI (Body Mass Index), NutriLog aims to offer users a detailed insight into their health metrics and dietary habits.

The core functionality of NutriLog includes maintaining a food diary where users can record their meals and drinks. The application also allows users to set and monitor calorie and hydration goals, record weight and height measurements, and adjust various settings. The user-friendly interface leverages modern web technologies and frameworks to ensure a seamless and efficient experience.

## Technology Stack:

NutriLog utilizes a diverse technology stack to deliver a robust and efficient application:

### Backend:

#### Python: 
Chosen for its simplicity and extensive support for web development. Python's flexibility and ease of integration with other technologies make it a suitable choice for the backend of NutriLog.
Flask: A lightweight web framework for Python, Flask is used due to its modular design and ease of use. It provides the necessary tools to build and maintain the backend services of the application efficiently.
Database:

#### SQLite: 
Selected for its simplicity and ease of use, SQLite is an embedded database that requires minimal setup. It is ideal for small to medium-sized applications and supports efficient data management for NutriLog.

### Frontend:

#### HTML/CSS/JavaScript: 
The foundational technologies for web development are employed to create a responsive and interactive user interface. HTML structures the content, CSS styles the elements, and JavaScript adds dynamic functionality.

#### Bootstrap: 
This CSS framework is used to expedite the styling process and ensure a visually appealing and responsive design. Bootstrap's pre-designed components and layout utilities simplify the development of a modern and user-friendly interface.

#### Image Processing:
##### Pillow: 
An image processing library for Python, Pillow is utilized to handle image optimization tasks. It ensures that images are resized and compressed before being uploaded to the server, thus improving performance and reducing load times.

## Structure:

### Python modules:

#### Image upload module:

##### Path: 
nutrilog\modules\img_upload.py

##### Description: 
This module contains code for validating, resizing and uploading images to the server. It uses Pillow for image processing.

#### BMI calculator module:

##### Path: 
nutrilog\modules\bmi_calculator.py

##### Description:
This module contains one function that takes in the user's weight and height and calculates the user's BMI. It returns an object containing the index and interpretation of the BMI.

#### Food item HTML module:

##### Path: 
nutrilog\modules\food_item_html.py

##### Description:
This module contains code for generating HTML for food items. It uses Jinja templates.

### Static files:
- nutrilog\static\style.css - Project stylesheet
- nutrilog\static\icons - Icons

### Jinja Templates:
- nutrilog\templates\base.html - Base for all templates

#### Login template:

##### Path:
nutrilog\templates\auth\login.html

##### Description:
This template is used to login. It includes a form for login and a link to register. The form is used to login. It also validates that both username and password are entered. If the login is successful, it redirects to the index page. If the login is unsuccessful, it displays an error message.

#### Register template:

##### Path:
nutrilog\templates\auth\register.html

##### Description:
This template is used to register new users. It includes a form with required fields for successful registration. 

#### Index (home) template:

##### Path:
nutrilog\templates\diary\index.html

##### Description:
This template is used to display the food diary. It includes a form for adding food items, water intake, goals, measurements, and settings. It also includes a table for displaying the food items.

#### Add food intake template:

##### Path:
nutrilog\templates\diary\add_food_intake.html

##### Description:
This template is used to add food intake. It includes a form for adding food items and a table for displaying the food items. The table is populated with food items from the database. The form is used to add new food items. It uses javascript to search for food items based on the user's input.

#### Goals template:

##### Path:
nutrilog\templates\diary\goals.html

##### Description:
This template is used to add goals. It includes a form for adding goals and a table for displaying the goals. The table is populated with goals from the database. The form is used to add new goals.

#### Settings template:

##### Path:
nutrilog\templates\diary\settings.html

##### Description:
This template is used to change password. It includes a form for changing password.

#### Measurements template:

##### Path:
nutrilog\templates\diary\measurements.html

##### Description:
This template is used to add measurements. It includes a form for adding weight and height and a button to save the measurements.

#### Add water intake template:

##### Path:
nutrilog\templates\diary\add_water_intake.html

##### Description:
This template is used to add water intake. It includes a form for adding water intake and a table for displaying the water intake history.

#### Add food item template:

##### Path:
nutrilog\templates\diary\add_food_item.html

##### Description:
This template is used to add food items. It includes a form for adding food items and a table for displaying the food items from the database.

#### Food search response template:

##### Path:
nutrilog\templates\diary\food_search_response.html

##### Description:
This template is used to display the food search response. It includes a table for displaying the search results.

### Root directory:

#### Init file:

##### Path: 
nutrilog\\_\_init\_\_.py

##### Description:
This file is used to initialize the project. It imports the necessary modules and sets up the database.

#### Database schema:

##### Path:
nutrilog\nutrilog.sql

##### Description:
This file contains the SQL schema for the database.

#### Auth.py:

##### Path:
nutrilog\auth.py

##### Description:
This file contains the authentication logic for the application. It includes user registration and login. It also checks if the user is logged in or not.

#### Diary.py:

##### Path:
nutrilog\diary.py

##### Description:
This file contains the logic for the food diary. It includes functions for adding food items, water intake, goals, measurements, and settings. It also includes functions for uploading images.

#### db.py:

##### Path:
nutrilog\db.py

##### Description:
This file contains the database logic. It initializes the database, creates tables, and closes the database connection.
