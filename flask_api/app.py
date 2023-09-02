import oci
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/compartments', methods=['GET'])
def get_compartments():
    # Initialize OCI SDK with your credentials
    config = oci.config.from_file()  # Make sure your OCI config file is set up

    # Create an OCI identity client
    identity_client = oci.identity.IdentityClient(config)

    try:
        # List all compartments in the tenancy
        compartments = identity_client.list_compartments(compartment_id=config['tenancy'])

        # Extract relevant information and return as JSON
        compartment_data = [
            {
                'name': compartment.name,
                'id': compartment.id,
                'description': compartment.description,
                # Add more attributes as needed
            }
            for compartment in compartments.data
        ]

        return jsonify({'compartments': compartment_data})

    except oci.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
