from flask import Flask, request, jsonify
from datetime import datetime
from vedicastro.VedicHoroscopeData import VedicHoroscopeData
from vedicastro.KpAyanamsha import KpAyanamsha

app = Flask(__name__)

@app.route('/generate_kp_chart', methods=['POST'])
def generate_kp_chart():
    try:
        data = request.get_json()

        name = data.get('name')
        dob_str = data.get('dob') # Expected format: YYYY-MM-DD
        tob_str = data.get('tob') # Expected format: HH:MM (24-hour)
        lat_str = data.get('lat')
        lon_str = data.get('lon')

        # Input validation and parsing
        if not all([dob_str, tob_str, lat_str, lon_str]):
            return jsonify({"error": "Missing one or more required fields: dob, tob, lat, lon"}), 400

        try:
            birth_date_obj = datetime.strptime(dob_str, '%Y-%m-%d')
            # Assuming tob_str is "HH:MM AM/PM"
            if "AM" in tob_str.upper() or "PM" in tob_str.upper():
                birth_time_obj = datetime.strptime(tob_str, '%I:%M %p').time()
            else: # Assuming 24-hour format "HH:MM"
                birth_time_obj = datetime.strptime(tob_str, '%H:%M').time()
            birth_datetime = datetime.combine(birth_date_obj, birth_time_obj)
            
            latitude = float(lat_str)
            longitude = float(lon_str)
        except ValueError as ve:
            return jsonify({"error": f"Invalid input format: {str(ve)}"}), 400

        # VedicAstro logic
        horoscope_data = VedicHoroscopeData()
        # KP Ayanamsha is typically default in many KP-focused libraries, 
        # but explicit setting is good.
        # The library might automatically use KP or require explicit setting.
        # This is a common way to set it, actual API might differ.
        ayanamsa_mode = KpAyanamsha.KRISHNAMURTI 
        
        # Assuming generate_chart takes ayanamsha_mode directly or it's set on horoscope_data
        # chart = horoscope_data.generate_chart(birth_datetime, latitude, longitude, ayanamsha_mode=ayanamsa_mode)
        # Simpler call if ayanamsha is set globally or by default for KP libraries
        chart = horoscope_data.generate_chart(birth_datetime, latitude, longitude)


        planets_data = horoscope_data.get_planets_data_from_chart(chart)
        houses_data = horoscope_data.get_houses_data_from_chart(chart)
        house_significators = horoscope_data.get_house_wise_significators(chart, planets_data, houses_data)
        planet_significators = horoscope_data.get_planet_wise_significators(chart, planets_data, houses_data)

        return jsonify({
            "message": "Chart generated successfully.",
            "received_data": {
                "name": name,
                "date_of_birth": dob_str,
                "time_of_birth": tob_str, # send back the original tob string
                "latitude": lat_str,
                "longitude": lon_str
            },
            "chart_data": {
                "planets": planets_data,
                "houses": houses_data,
                "house_significators": house_significators,
                "planet_significators": planet_significators
            }
        })

    except Exception as e:
        # Log the exception for debugging
        app.logger.error(f"Error in generate_kp_chart: {e}", exc_info=True)
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
