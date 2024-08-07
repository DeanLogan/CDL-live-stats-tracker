# CDL Live Stat Tracker (Work In Progress)

This project is dedicated to providing real-time statistics for Call of Duty League (CDL) games. CDL is the esports platform for Call of Duty. 

During CDL games, a stat board occasionally appears, displaying the current stats for the players. However, most of the time, the screen only shows the players' faces. This project aims to fill that gap by tracking these stats live during the matches.

![Scoreboard](./imgs/scoreboard.png)
*Example of a stat board during a CDL game*

![Player Faces](./imgs/player-faces.png)
*Typical view during a CDL game*

## How It Will Work

The primary statistic this program tracks is the kills and deaths for each player (K/D). All kills players achieve are displayed in the killfeed during the match as the player scores the kills. 

![Killfeed](./imgs/killfeed.png)  
*Example of a killfeed during a CDL game*

The main component of the system is the [`game-stats-recorder`]("c:\Users\dloga\Documents\Code\Python\CDL-live-stats-tracker\backend\python\game-stats-recorder.py"). It starts by monitoring the official CDL YouTube channel to detect when a match goes live. Once a match is identified, the program uses Optical Character Recognition (OCR) to determine when the match begins. It then reads the players' names and the teams playing, using a database of player information that is regularly updated by scraping the CDL website. During the match, the program "watches" the killfeed to identify kills. When a kill occurs, it identifies the two players involved (the killer and the victim), updates a dictionary that stores each player's kills and deaths, and publishes this updated information to Kafka. A Node.js server, acting as a subscriber, collects the updated information and updates the main React app with the players' kills and deaths, calculating the K/D ratio in real-time.

## Project Structure

The project is organized into several directories:

- **backend/**: Contains the server-side code.
  - **node-server/**: Node.js server implementation.
    - [package.json](backend/node-server/package.json): Defines the Node.js server dependencies.
  - **python/**: Python scripts for capturing and processing game statistics.
    - [game-stats-recorder.py](backend/python/game-stats-recorder.py): Main script for recording game statistics using OCR and Selenium.

- **db/**: Database-related files.
  - [create-db.py](db/create-db.py): Script to create the database.
  - [populate-db.py](db/populate-db.py): Script to populate the database with initial data.
  - Dockerfile: Docker configuration for the database.

- **frontend/**: Contains the client-side code.
  - [index.html](frontend/index.html): Main HTML file for the frontend.
  - [src/](frontend/src/): Source code for the frontend application.
    - [App.tsx](frontend/src/App.tsx): Main React component.
    - [components/](frontend/src/components/): React components.
  - [package.json](frontend/package.json): Defines the frontend dependencies.
  - [vite.config.ts](frontend/vite.config.ts): Vite configuration file.

- **imgs/**: Contains images used in the README and the application.

- **POCs/**: Proof of Concept scripts.
  - [docker-test.py](POCs/docker-test.py): Script to test Docker integration.
  - [game-live-identification.py](POCs/game-live-identification.py): Script for live game identification.

- **README.md**: This file.
- **docker-compose.yml**: Docker Compose configuration file.
- **requirements.txt**: Python dependencies.
