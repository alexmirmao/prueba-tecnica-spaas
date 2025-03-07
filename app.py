from flask import Flask, request, jsonify
import copy

app = Flask(__name__)

def load_algorithm_recursively(result, result_inicialized, remaining_load, first_load, powerplants, i, j):
    #checking if we have not exceded the length of powerplants
    print("i---->" + str(i))
    print("j---->" + str(j))
    print(result)
    if i < len(powerplants):
        if j < len(powerplants):
            allocated_power = min(powerplants[j]["pmax"], max(powerplants[j]["pmin"], remaining_load))
            if remaining_load - allocated_power >= 0 and allocated_power > 0 and result[j]["p"] == 0:
                
                result[j]["p"] = round(allocated_power, 1)
                remaining_load -= allocated_power
                #checking if we get the most optimized result
                if remaining_load == 0:
                    return result
                else:
                    return load_algorithm_recursively(result, result_inicialized, remaining_load,first_load, powerplants, i, 0)
            else:
                return load_algorithm_recursively(result, result_inicialized, remaining_load,first_load, powerplants, i, j+1)
            
        else:
            result = copy.deepcopy(result_inicialized)
            remaining_load = first_load
            #Here we do the first load to the reinizialiced list
            allocated_power = min(powerplants[i+1]["pmax"], max(powerplants[i+1]["pmin"], remaining_load))
            result[i+1]["p"] = round(allocated_power, 1)
            remaining_load -= allocated_power

            if remaining_load == 0:
                return result
            
            return load_algorithm_recursively(result, result_inicialized, remaining_load,first_load, powerplants, i+1, 0)

def load_algorithm_linear(load, result_inicialized, powerplants):
    is_remaining_load = True
    i = 0
    while i < len(powerplants) and is_remaining_load:
        result = copy.deepcopy(result_inicialized)
        remaining_load = load
        #Here we do the first load to the reinizialiced list
        allocated_power = min(powerplants[i]["pmax"], max(powerplants[i]["pmin"], remaining_load))
        result[i]["p"] = round(allocated_power, 1)
        remaining_load -= allocated_power
        j = 0
        #Looping all elements since the beggining
        while j < len(powerplants) and is_remaining_load:
            if result[j]["p"] == 0:
                #Calculate the allocated_power
                allocated_power = min(powerplants[j]["pmax"], max(powerplants[j]["pmin"], remaining_load))

                #Checking if its enough load 
                if remaining_load - allocated_power >= 0 and allocated_power > 0:
                    result[j]["p"] = round(allocated_power, 1)
                    remaining_load -= allocated_power
                    j = 0
                    #checking if we get the most optimized result
                    if remaining_load == 0:
                        return result
                    
                
            j += 1
            print(result)        
        if remaining_load == 0:
            return result
        i +=1
            
def inicialize_results(powerplants):
    result = []
    for plant in powerplants:
        result.append({"name": plant["name"], "p": 0.0})
    
    return result

def calculate_production_plan(load, fuels, powerplants):
    # 1. Calculating production costs
    co2_price = fuels["co2(euro/ton)"]  # Price C02 per ton
    co2_emission_per_mwh = 0.3  # Tons of CO2 per Mwh

    for plant in powerplants:
        if plant["type"] == "windturbine":
            plant["cost"] = 0  # Free wind
            plant["pmax"] *= fuels["wind(%)"] / 100  
        elif plant["type"] == "gasfired":
            fuel_price = fuels["gas(euro/MWh)"]  
            plant["cost"] = (fuel_price / plant["efficiency"]) + (co2_price * co2_emission_per_mwh)
        else:
            fuel_price = fuels["kerosine(euro/MWh)"]
            plant["cost"] = fuel_price / plant["efficiency"]
    
    # 2. (Merit Order) by costs
    powerplants.sort(key=lambda x: x["cost"])

    # 3. Loads
    result_inicialized = inicialize_results(powerplants)
    
    
    i = 0
    j = 0
    result = copy.deepcopy(result_inicialized)
    remaining_load = load
    #First load
    allocated_power = min(powerplants[i]["pmax"], max(powerplants[i]["pmin"], remaining_load))
    result[i]["p"] = round(allocated_power, 1)
    remaining_load -= allocated_power

    result = load_algorithm_recursively(result, result_inicialized, remaining_load, load, powerplants, i, j)

    #result = load_algorithm_linear(load,result_inicialized,powerplants)

    return result

@app.route("/productionplan", methods=["POST"])
def production_plan():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400
        
        response = calculate_production_plan(data["load"], data["fuels"], data["powerplants"])
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
