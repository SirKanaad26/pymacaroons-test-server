import requests
from pymacaroons import Macaroon

# 1. Get the original token from Port 5000
print("Step 1: Getting original Macaroon...")
resp = requests.get('http://127.0.0.1:5000/macaroon')
m_serialized = resp.json()['macaroon']
m = Macaroon.deserialize(m_serialized)

# 2. Get the discharge (the stamp) from Port 5001
print("Step 2: Getting discharge from Third Party...")
resp_tp = requests.post('http://127.0.0.1:5001/discharge', json={'key_id': 'third-party-key-id'})
dm_serialized = resp_tp.json()['discharge_macaroon']
dm = Macaroon.deserialize(dm_serialized)

# 3. IMPORTANT: Bind the discharge to the root macaroon
# This prevents the discharge token from being stolen and used by others
print("Step 3: Binding discharge to root...")
prepared_dm = m.prepare_for_request(dm)

# 4. Send both back to Port 5000 for verification
print("Step 4: Verifying...")
final_resp = requests.post('http://127.0.0.1:5000/verify', json={
    'macaroon': m.serialize(),
    'discharge': prepared_dm.serialize()
})

print(f"Final Result: {final_resp.status_code}")
print(final_resp.json())