# Overview

This project is a SAP Portal Modernization application that provides a web-based interface for interacting with SAP systems. The system consists of a FastAPI backend that handles SAP RFC connections and data operations, coupled with an Angular frontend that provides a modern user interface for managing SAP records. The application aims to modernize legacy SAP interfaces by providing RESTful APIs and a responsive web UI.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The frontend is built using Angular 20.3.0 with a component-based architecture. It follows Angular's standalone component pattern without traditional NgModules. The application uses:

- **Component Structure**: Two main components - `SapRecordList` for displaying records and `SapRecordForm` for creating/editing records
- **Routing**: Angular Router with lazy loading for navigation between record list and form views
- **State Management**: Service-based state management using `SapDataService` for API communication
- **Styling**: Component-scoped CSS with a modern, responsive design using flexbox layouts
- **Development Proxy**: Angular dev server proxies API calls to the FastAPI backend running on port 8000

## Backend Architecture
The backend uses FastAPI as the web framework with a modular design:

- **API Layer**: RESTful endpoints following OpenAPI standards with automatic documentation
- **SAP Integration**: Dedicated `SAPConnector` class for managing SAP RFC connections (currently stubbed, awaiting pyrfc library integration)
- **Data Models**: Pydantic models for request/response validation and serialization
- **CORS Configuration**: Configured for cross-origin requests from the Angular frontend
- **Error Handling**: Structured error responses with appropriate HTTP status codes

## Data Flow
The application follows a standard client-server pattern:
1. Angular frontend makes HTTP requests to FastAPI backend
2. Backend processes requests and communicates with SAP systems via RFC calls
3. Data is transformed and returned as JSON responses
4. Frontend updates the UI based on API responses

## Configuration Management
- Backend uses environment variables loaded via python-dotenv
- Frontend uses Angular's proxy configuration for development
- SAP connection parameters are configured through the SAPConfig dataclass

# External Dependencies

## Frontend Dependencies
- **Angular Framework**: Core framework (v20.3.0) with Router, Forms, and HTTP client modules
- **RxJS**: For reactive programming and HTTP request handling
- **TypeScript**: For type-safe development and Angular compatibility
- **Zone.js**: For Angular's change detection mechanism

## Backend Dependencies
- **FastAPI**: Web framework for building RESTful APIs with automatic OpenAPI documentation
- **Pydantic**: Data validation and serialization using Python type annotations
- **python-dotenv**: Environment variable management for configuration
- **pyrfc** (planned): SAP RFC library for connecting to SAP systems (not yet installed)

## Development Tools
- **Angular CLI**: For project scaffolding, building, and development server
- **Karma/Jasmine**: Testing framework for Angular components
- **Prettier**: Code formatting for consistent style
- **VSCode Extensions**: Angular language service for enhanced development experience

## SAP Integration
- **SAP RFC Protocol**: Direct connection to SAP systems using Remote Function Calls
- **SAP Application Server**: Target SAP system for data retrieval and manipulation
- The SAP connector supports standard SAP connection parameters (host, system number, client, credentials)