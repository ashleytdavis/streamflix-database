<img src="StreamflixDatabase\assets\streamflix-logo.png" alt="Streamflix Logo" />

## Overview
The **Streamflix Database** is designed to act as a media streaming platform, structued to handle users, content (including movies and series), and basic associated interactions (leaving reviews, ratings, etc.). The database schema includes tables for managing user information, video content, and various relationships among them.


## Data Model
The Streamflix data model serves as a low-level representation for a large-scale streaming service, comparable to platforms like Netflix or Hulu.
<img src="StreamflixDatabase\assets\streamflix-database-diagram.png" alt="Relational Diagram" />


## Sample Data
Data for the Streamflix database can be generated by running the `data_generation.py` file. A testing file, `data_test.py` has also been provided, to ensure the data was successfully generated. 

1. **Prerequisites**: Ensure you have Python 3.x installed on your system. The data generation script also requires `Faker`, `MySQL-Connector`, `Pandas`, and `Python-dotenv`. They can be installed by running the command `pip install Faker mysql-connector-python pandas python-dotenv`.

2. **Clone the Repository**: Clone the database repository to your local machine using git:

  ```bash
  git clone https://github.com/ashleytdavis/streamflix-database
  ```

3. **Add Your Personal Information**: In the root directory, create a `.env` file and add values for the following attributes:
```
MYSQL_HOST=
MYSQL_PORT=
MYSQL_USER=
MYSQL_PASSWORD=
```