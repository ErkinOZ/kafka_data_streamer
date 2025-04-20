# kafka_data_streamer
## Project Overview
Real-Time Telecom is a system designed to process, store, and visualize telecom user activity in real time. It leverages Kafka for data streaming, PostgreSQL for data storage, and Streamlit for interactive dashboards. The project also includes a FastAPI backend for API-based data access.
## Architecture
The project consists of the following components:
- **Kafka Consumer**: Processes user activity data from Kafka topics and stores it in PostgreSQL.
- **PostgreSQL Database**: Stores user activity logs with conflict resolution for updates.
- **FastAPI Backend**: Provides RESTful APIs for accessing user activity data.
- **Streamlit Dashboard**: Visualizes real-time data with interactive maps and metrics.

## Installation and Setup

### Prerequisites
- Docker and Docker-Compose
- Python 3.8+
- Kafka and Zookeeper

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/real-time-telecom.git
   cd real-time-telecom
