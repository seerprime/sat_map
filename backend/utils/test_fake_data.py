**Step-by-step plan (pseudocode):**

1. Identify functions in `fake_data.py` that generate data and can be tested via API endpoints.
2. List typical API endpoints for these functions (e.g., `/api/map/trash-hotspots`, `/api/map/water-zones`, etc.).
3. For each function, describe a sample request body (if needed) and expected response structure.
4. Write Postman test instructions for each endpoint:
    - HTTP method (GET/POST)
    - URL path
    - Example query/body parameters
    - Expected response keys and types
    - Example Postman test scripts (in JavaScript) to validate response

---

**API Endpoint Test Instructions for Postman**

1. **Trash Hotspots**
    - **Method:** GET
    - **URL:** `/api/map/trash-hotspots?lat_min=28.6&lat_max=28.7&lng_min=77.2&lng_max=77.3&zoom_level=14`
    - **Tests:**
      ```javascript
      pm.test("Status code is 200", function () {
          pm.response.to.have.status(200);
      });
      pm.test("Response is array", function () {
          pm.expect(pm.response.json()).to.be.an('array');
      });
      pm.test("Hotspot object has required keys", function () {
          const item = pm.response.json()[0];
          pm.expect(item).to.have.property("id");
          pm.expect(item).to.have.property("location");
          pm.expect(item).to.have.property("intensity");
      });
      ```

2. **Water Contamination Zones**
    - **Method:** GET
    - **URL:** `/api/map/water-zones?lat_min=28.6&lat_max=28.7&lng_min=77.2&lng_max=77.3&zoom_level=14`
    - **Tests:**
      ```javascript
      pm.test("Status code is 200", function () {
          pm.response.to.have.status(200);
      });
      pm.test("Response is array", function () {
          pm.expect(pm.response.json()).to.be.an('array');
      });
      pm.test("Zone object has required keys", function () {
          const item = pm.response.json()[0];
          pm.expect(item).to.have.property("id");
          pm.expect(item).to.have.property("contamination_level");
          pm.expect(item).to.have.property("location");
      });
      ```

3. **Heatmap Data**
    - **Method:** GET
    - **URL:** `/api/map/heatmap?lat_min=28.6&lat_max=28.7&lng_min=77.2&lng_max=77.3&zoom_level=14`
    - **Tests:**
      ```javascript
      pm.test("Status code is 200", function () {
          pm.response.to.have.status(200);
      });
      pm.test("Response is array", function () {
          pm.expect(pm.response.json()).to.be.an('array');
      });
      pm.test("Heatmap point has required keys", function () {
          const item = pm.response.json()[0];
          pm.expect(item).to.have.property("latitude");
          pm.expect(item).to.have.property("intensity");
      });
      ```

4. **Satellite Imagery Metadata**
    - **Method:** GET
    - **URL:** `/api/map/satellite-metadata`
    - **Tests:**
      ```javascript
      pm.test("Status code is 200", function () {
          pm.response.to.have.status(200);
      });
      pm.test("Response is object", function () {
          pm.expect(pm.response.json()).to.be.an('object');
      });
      pm.test("Metadata has required keys", function () {
          const item = pm.response.json();
          pm.expect(item).to.have.property("satellite");
          pm.expect(item).to.have.property("acquisition_date");
      });
      ```

5. **Cleanup Cost Estimate**
    - **Method:** POST
    - **URL:** `/api/map/cleanup-cost`
    - **Body (JSON):**
      ```json
      {
        "item_count": 100,
        "weight_kg": 250,
        "location_difficulty": "hard"
      }
      ```
    - **Tests:**
      ```javascript
      pm.test("Status code is 200", function () {
          pm.response.to.have.status(200);
      });
      pm.test("Response is object", function () {
          pm.expect(pm.response.json()).to.be.an('object');
      });
      pm.test("Cost estimate has required keys", function () {
          const item = pm.response.json();
          pm.expect(item).to.have.property("total_cost_usd");
          pm.expect(item).to.have.property("cost_breakdown");
      });
      ```

6. **Weather Impact Data**
    - **Method:** GET
    - **URL:** `/api/map/weather-impact?lat=28.6139&lng=77.2090`
    - **Tests:**
      ```javascript
      pm.test("Status code is 200", function () {
          pm.response.to.have.status(200);
      });
      pm.test("Response is object", function () {
          pm.expect(pm.response.json()).to.be.an('object');
      });
      pm.test("Weather impact has required keys", function () {
          const item = pm.response.json();
          pm.expect(item).to.have.property("current_conditions");
          pm.expect(item).to.have.property("environmental_modifiers");
      });
      ```

---

**Summary:**  
- Use the above endpoints and test scripts in Postman.
- Adjust endpoint paths to match your FastAPI routes.
- For POST requests, use the provided sample JSON body.
- Each test checks for status code, response type, and key fields.

Let me know if you want Python unit tests for these functions instead!