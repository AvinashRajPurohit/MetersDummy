# Live System of Meters

dummy project on meters data

## Prerequisites

- Python 3.9

## Installation

1. Clone the repository:

2. Create a virtual environment:


3. Create and Activate the virtual environment:

- For macOS/Linux:

  ```
  source env/bin/activate
  ```

- For Windows:

  ```
  .\env\Scripts\activate
  ```

4. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

5. Database Setup:
- Update the database URI in the `app.config['SQLALCHEMY_DATABASE_URI']` configuration variable in `app.py` with your database URI or use the sqlite3.
- Populate the tables
  - ```shell
    $ flask db init
    $ flask db migrate 
    $ flask db upgrade 
    ```

## Usage

1. After setting up database run the application:
   ```shell
    $ python3 app.py
   ```
2. Open your browser and access the application at [http://localhost:5000](http://localhost:5000).
3. API Spec:
   * Get Meters 

     - Endpoint: /meters/
     - Method: GET
     - Description: Retrieves all available meters from the database.
     - Response: JSON array of meter labels and URLs.
     - Example: http://localhost:5000/meters/
     <hr>
   * Get Meter Data
   
     - Endpoint: /meters/<meter_id>/
     - Method: GET
     - Description: Retrieves the data associated with a specific meter.
     - Parameters:
       - meter_id: The ID of the meter.
     - Response: JSON array of meter data.
     - Example: http://localhost:5000/meters/1/
   <hr>
     
   * Generate Dummy Data
     
    - Endpoint: /generate_dummy_data/
     - Method: GET
     - Description: Generates fake data for the Meter and MeterData tables.
     - Response: JSON object containing generated meter labels and meter data.
     - Example: http://localhost:5000/generate_dummy_data/


