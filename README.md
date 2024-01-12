## API Routes Documentation

This section describes the available API routes in the application, including their functionality, request format, and response structure.

### 1. Upload GeoData (`POST /upload/`)

#### Description
Uploads GeoJSON data and stores it in the database.

#### Request
- **URL**: `/upload/`
- **Method**: `POST`
- **Body**: 
  - `file`: A GeoJSON file.

#### Response
- **Success**: Returns the ID and filename of the uploaded data.
- **Failure**: Returns an error message if no valid features are found or if an internal error occurs.

### 2. Delete All GeoData (`DELETE /delete-all/`)

#### Description
Deletes all GeoData records from the database.

#### Request
- **URL**: `/delete-all/`
- **Method**: `DELETE`

#### Response
- **Success**: A confirmation message indicating that all data has been successfully deleted.
- **Failure**: An error message if an internal error occurs.

### 3. Get All GeoData (`GET /get-all/`)

#### Description
Retrieves all GeoData records from the database.

#### Request
- **URL**: `/get-all/`
- **Method**: `GET`

#### Response
- **Success**: A list of all GeoData records, each including ID, filename, and geographic data (in WKT or GeoJSON format).
- **Failure**: An error message if an internal error occurs.

### 4. Update GeoData Name (`PUT /update-name/{item_id}`)

#### Description
Updates the name of a specific GeoData record.

#### Request
- **URL**: `/update-name/{item_id}`
- **Method**: `PUT`
- **URL Parameters**: 
  - `item_id`: The ID of the GeoData record to be updated.
- **Body**: 
  - `new_name`: The new name for the GeoData record.

#### Response
- **Success**: A confirmation message indicating that the name has been successfully updated.
- **Failure**: An error message if the item is not found or if an internal error occurs.
