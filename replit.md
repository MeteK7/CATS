# Overview

This project is a SAP Portal Modernization application that provides a web-based interface for interacting with SAP systems. The system consists of a FastAPI backend that handles SAP RFC connections and data operations, coupled with an Angular frontend that provides a modern user interface for managing SAP records. The application aims to modernize legacy SAP interfaces by providing RESTful APIs and a responsive web UI.

## Current Status

The project has successfully implemented a **simplified work order search interface** that replaces the complex legacy Java-based SAP Portal with a clean, modern web interface. The search functionality focuses on essential business criteria:

- **Search Fields**: VIN Number, Dealer Code, Work Order Number, Date Range (From/To)
- **Strategy Options**: Temsa Global, Temsa Global GW&TK, Germany, France, North America
- **Filtering**: Server-side filtering respects all search criteria with case-insensitive partial matching
- **Mock Data**: Structured mock data simulates real Zcatsv2_Wo_Get_List RFC responses for testing

## SAP Integration Challenge

**Important**: The PyRFC library (Python's primary SAP RFC connector) has been officially discontinued by SAP as of 2024. This affects the original plan to directly call SAP RFCs like `Zcatsv2_Wo_Get_List`. The current architecture is designed to easily transition to **SAP web services/OData** integration when ready for production SAP connectivity.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The frontend is built using Angular 20.3.0 with a component-based architecture. It follows Angular's standalone component pattern without traditional NgModules. The application uses:

- **Component Structure**: Simplified work order search component with clean, focused interface
- **Search Interface**: Essential fields only - VIN, Dealer Code, Work Order Number, Date Range, Strategy checkboxes
- **Routing**: Angular Router with navigation between work order search and results views
- **State Management**: Service-based state management using `WorkOrderService` for API communication
- **Styling**: Component-scoped CSS with a modern, responsive design using flexbox layouts
- **Development Proxy**: Angular dev server proxies API calls to the FastAPI backend running on port 8000
- **Validation**: Client-side form validation with proper TypeScript typing

## Backend Architecture
The backend uses FastAPI as the web framework with a modular design:

- **API Layer**: RESTful endpoints following OpenAPI standards with automatic documentation
- **Work Order Search**: Simplified endpoint `/api/sap/work-orders/search` with comprehensive server-side filtering
- **SAP Integration**: Prepared for SAP web services integration (PyRFC discontinued by SAP)
- **Data Models**: Simplified Pydantic models matching real business requirements
- **Mock Data System**: Structured mock data with realistic filtering for development and testing
- **CORS Configuration**: Configured for cross-origin requests from the Angular frontend
- **Error Handling**: Structured error responses with appropriate HTTP status codes

## Data Flow
The application follows a standard client-server pattern:
1. Angular frontend collects search criteria from simplified form
2. HTTP POST request sent to `/api/sap/work-orders/search` with search parameters
3. Backend applies server-side filtering (VIN, dealer code, work order number, date range, strategy)
4. Filtered work order data returned as JSON response
5. Frontend displays results in responsive table format
6. **Future**: Replace mock data filtering with SAP web services/OData calls

## Configuration Management
- Backend uses environment variables loaded via python-dotenv
- Frontend uses Angular's proxy configuration for development
- SAP connection parameters ready for web services integration
- Mock data system configured for development and testing

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
- **Current Approach**: Structured mock data simulating Zcatsv2_Wo_Get_List RFC responses
- **Future Integration**: SAP web services/OData (PyRFC library discontinued by SAP)
- **Architecture Ready**: Backend filtering logic prepared for easy SAP data source swap
- **Business Logic**: Real search criteria based on actual business requirements
- **Strategy Mapping**: Five strategy categories mapped to realistic dealer/country combinations