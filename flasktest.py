from flask import Flask, jsonify, request, render_template
import logging, sys
import mysql.connector
from flask_restx import Api, Resource,Namespace

app = Flask(__name__)
api = Api(app, doc='/swagger')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'oren'
app.config['MYSQL_PASSWORD'] = 'oren'
app.config['MYSQL_DB'] = 'ant_db'

ns = Namespace("api/v1")
api.add_namespace(ns)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def get_db_connection():
    connection = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    return connection

# Function to handle incoming simulation results
def send_sim_result(id, sim_result, runs):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Execute a SQL query
    query = "SELECT * FROM ant_table WHERE sim_name =%s"
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    if result is None:
        insert_query = "INSERT INTO ant_table (sim_name, run_count, total_food_collected) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (id, runs, sim_result * runs))
        connection.commit()  # Commit the transaction
        print(f"Row with sim_name = {sim_result} created.")      
    else:
         new_run_count = result['run_count'] + runs
         new_total_food_collected = result['total_food_collected'] + (sim_result * runs)
        # Update the row with the new values
         update_query = """
         UPDATE ant_table 
         SET run_count = %s, total_food_collected = %s
         WHERE sim_name = %s
         """
         cursor.execute(update_query, (new_run_count, new_total_food_collected, id))
         connection.commit()  # Commit the transaction
         print(f"Row with sim_name = {sim_result} updated.")
    # Close the connection
    cursor.close()
    connection.close()
    return {"status": "success", "message": "Simulation result received. result =" + str(result)}

# Function to get the summary of all simulation results including average food collected
def get_all_sim_results():
    # Get the database connection
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Execute the SQL query to fetch all rows from the ant_table
        query = "SELECT * FROM ant_table"
        cursor.execute(query)

        results = cursor.fetchall()

        # Check if results exist and calculate the average for each row
        if results:
            for row in results:
                # Calculate the average if run_count is not zero
                if row["run_count"] > 0:
                    row["average_food_collected"] = row["total_food_collected"] / row["run_count"]
                else:
                    row["average_food_collected"] = None  # Or 0, depending on your preference

            return {
                "status": "success",
                "message": "Results retrieved successfully.",
                "data": results
            }
        else:
            return {
                "status": "success",
                "message": "No results found.",
                "data": []
            }

    except Exception as e:
        # Handle any exceptions that occur during database operations
        print(f"Error: {str(e)}")
        return {"status": "error", "message": f"Error occurred: {str(e)}"}

    finally:
        cursor.close()
        connection.close()

def get_sim_result_by_id(sim_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Execute the SQL query to fetch a specific row by sim_id
        query = "SELECT * FROM ant_table WHERE sim_name = %s"
        cursor.execute(query, (sim_id,))  # Use (sim_id,) to pass as a tuple

        # Fetch the single result
        result = cursor.fetchone()

        # Check if the result exists
        if result:
            return {"status": "success", "message": "Result retrieved successfully.", "data": result}
        else:
            return {"status": "success", "message": f"No result found for sim_id = {sim_id}", "data": None}

    except Exception as e:
        # Handle any exceptions that occur during database operations
        print(f"Error: {str(e)}")
        return {"status": "error", "message": f"Error occurred: {str(e)}"}

    finally:
        cursor.close()
        connection.close()




my_resource_parser = api.parser()
my_resource_parser.add_argument('id', required=True,location='json')
my_resource_parser.add_argument('sim_result', required=True,location='json',type = float)
my_resource_parser.add_argument('runs', required=True,location='json',type = int)

@ns.route("/send_sim_result", endpoint='with-parser')
class send_sim_results(Resource):
    @ns.expect(my_resource_parser)
    def post(self):
      if request.is_json:
          # Get the data from the request
          data = request.get_json()

          # Extract the values from the request data
          id = data.get('id')
          sim_result = data.get('sim_result')
          runs = data.get('runs')
          # Ensure all necessary parameters are present
          if not all([id, sim_result, runs]):
              return ({"error": "Missing required fields"}), 400

          # Call the send_sim_result function
          send_sim_result(id, sim_result, runs)

          # Return a success response
          return ({"message": "Simulation result processed successfully"}), 200
      else:
          return ({"error": "Invalid input, JSON expected"}), 400
     


@ns.route("/get_sim_summary")
class get_sim_summary(Resource):
  def get(self):
    result = get_all_sim_results()
    return jsonify(result)


@ns.route('/get_sim_result/<string:sim_id>', endpoint='my-resource')
class get_sim_result(Resource):
    def get(self,sim_id):       
        return(get_sim_result_by_id(sim_id))

@app.route('/home')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)