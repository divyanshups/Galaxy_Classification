from flask import Flask, render_template, request, redirect, url_for
import joblib

app = Flask(__name__, template_folder='C:/Users/HP/Downloads/templates')
loaded_model = joblib.load('RFmodel.sav')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            r = float(request.form['r'])
            i = float(request.form['i'])
            z = float(request.form['z'])
            petroRad_g = float(request.form['petroRad_g'])
            petroRad_r = float(request.form['petroRad_r'])
            petroR50_u = float(request.form['petroR50_u'])
            petroR50_g = float(request.form['petroR50_g'])
            petroR50_i = float(request.form['petroR50_i'])
            petroR50_r = float(request.form['petroR50_r'])
            petroR50_z = float(request.form['petroR50_z'])

            # Build query string and redirect to /output
            return redirect(url_for('output',
                r=r, i=i, z=z,
                petroRad_g=petroRad_g, petroRad_r=petroRad_r,
                petroR50_u=petroR50_u, petroR50_g=petroR50_g,
                petroR50_i=petroR50_i, petroR50_r=petroR50_r, petroR50_z=petroR50_z))
        except ValueError:
            return "Invalid input. Please enter numeric values only."

    return render_template('index.html')

@app.route('/output')
def output():
    # Extract values from URL query parameters
    try:
        test = [[
            float(request.args.get('r')),
            float(request.args.get('i')),
            float(request.args.get('z')),
            float(request.args.get('petroRad_g')),
            float(request.args.get('petroRad_r')),
            float(request.args.get('petroR50_u')),
            float(request.args.get('petroR50_g')),
            float(request.args.get('petroR50_i')),
            float(request.args.get('petroR50_r')),
            float(request.args.get('petroR50_z'))
        ]]
    except (TypeError, ValueError):
        return "Missing or invalid query parameters."
    out = loaded_model.predict(test)
    if out == 0:
        output_ml = "STARFORMING"
    else:
        output_ml = "STARBURST"


    return render_template('output.html', output=output_ml)

try: 
    if  __name__ == '__main__':
        app.run(debug=True,port=8000)
except:
    print("Exception occured!")
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)
