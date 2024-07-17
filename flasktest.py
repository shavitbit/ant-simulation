from flask import Flask, jsonify, request, render_template
import logging, sys

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# In-memory storage for simulation results
sim_results = {}
sim_counters = {}

# Function to handle incoming simulation results
def send_sim_result(sim_result):
    sim_id = sim_result['sim_id']
    food_collected = sim_result['food_collected']
    
    if sim_id in sim_results:
        sim_results[sim_id].append(food_collected)
    else:
        sim_results[sim_id] = [food_collected]

    if sim_id in sim_counters:
        sim_counters[sim_id] += 1
    else:
        sim_counters[sim_id] = 1

    return {"status": "success", "message": "Simulation result received"}

# Function to get the summary of all simulation results
def get_all_sim_results():
    summary = {}
    for sim_id, results in sim_results.items():
        summary[sim_id] = {
            "total_runs": len(results),
            "average_food_collected": sum(results) / len(results) if results else 0
        }
    return {"status": "success", "summary": summary}

# Function to get the summary of a specific simulation result by ID
def get_sim_result_by_id(sim_id):
    if sim_id in sim_results:
        results = sim_results[sim_id]
        summary = {
            "total_runs": len(results),
            "average_food_collected": sum(results) / len(results) if results else 0
        }
        return {"status": "success", "summary": summary}
    else:
        return {"status": "error", "message": f"No simulation found for ID {sim_id}"}

# Function to get the counter for a specific simulation by ID
def get_sim_counter_by_id(sim_id):
    if sim_id in sim_counters:
        return {"status": "success", "counter": sim_counters[sim_id]}
    else:
        return {"status": "error", "message": f"No simulation counter found for ID {sim_id}"}

# Function to get the total counter of all simulations
def get_total_sim_counter():
    total_counter = sum(sim_counters.values())
    return {"status": "success", "total_counter": total_counter}

@app.route('/')
def index():
    return render_template('index.html')

# POST simulation result
@app.route('/api/v1/send_sim_result', methods=['POST'])
def send_sim_result_api():
    sim_result = request.get_json()
    return jsonify(send_sim_result(sim_result))

# GET average summary of all simulations
@app.route('/api/v1/get_sim_summary', methods=['GET'])
def get_sim_summary_api():
    return jsonify(get_all_sim_results())

# GET average summary of a specific simulation ID
@app.route('/api/v1/get_sim_summary/<int:sim_id>', methods=['GET'])
def get_sim_summary_by_id_api(sim_id):
    return jsonify(get_sim_result_by_id(sim_id))

# GET simulation counter for a specific simulation ID
@app.route('/api/v1/sim_counter/<int:sim_id>', methods=['GET'])
def get_sim_counter_by_id_api(sim_id):
    return jsonify(get_sim_counter_by_id(sim_id))

# GET simulation counter for all simulations
@app.route('/api/v1/sim_counter', methods=['GET'])
def get_total_sim_counter_api():
    return jsonify(get_total_sim_counter())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)