# TeleCar Backend 🚗💬🌐


TeleCar is a comprehensive automotive application that connects vehicle owners, facilitates communication, and provides a platform for buying, selling, and discussing all things related to cars. With TeleCar, users can engage in real-time chat with other car owners, participate in forum discussions, explore auction listings, manage tickets, and access various vehicle-related services.

This repository contains the backend code for the TeleCar application, built using FastAPI and Python. The backend provides a robust API for managing user authentication, real-time chat functionality, forum discussions, auction listings, ticket management, and integration with external services.

## Features ✨

- 🔒 User Registration and Authentication:
  - Secure user registration with password hashing
  - JWT-based authentication for protecting routes
  - User profile management

- 💬 Real-time Chat:
  - WebSocket-based real-time chat functionality
  - Support for one-to-one chat between users
  - Message persistence in MongoDB
  - Last chat retrieval for each user

- 🗨️ Forum Discussions:                                                                                ![TeleCar](https://github.com/user-attachments/assets/47260b9d-7a78-453e-8a81-0ac3f99a6129)
  - Create, read, and manage forum posts
  - Filter posts based on user choice
  - User commenting system for engaging discussions

- 🏷️ Auction Listings:
  - Create and manage vehicle auction listings
  - Detailed information including manufacturer, model, year, price, and description
  - Contact information for interested buyers

- 🎫 Ticket Management:
  - Create, retrieve, and delete tickets associated with users
  - Store ticket details such as fine amount and payment deadline

- 🌍 External Service Integration:
  - Integration with Google Maps API for locating parking and vehicle services
  - Fetch vehicle information from government APIs
  - Retrieve real-time stock data for automotive companies

## Technologies Used 🛠️

- 🚀 FastAPI: A modern, fast, web framework for building APIs with Python
- 🍃 MongoDB: A NoSQL database for storing user, chat, forum, auction, and ticket data
- 🔑 JWT (JSON Web Tokens): Used for authentication and securing routes
- 🌐 GoogleTrans: A library for translating text between languages
- 📦 Pydantic: For data validation and serialization
- 🖥️ Uvicorn: An ASGI server for running the FastAPI application


## Contributing 🤝

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


