# Smart Cart Builder Extension - Enhanced Version

This is the enhanced frontend component of the Smart Cart Builder project, implemented as a Chrome extension using Vue 3, TypeScript, and Tailwind CSS.

## New Features

### 1. Human-in-the-Loop Interaction
- **Category Review UI**: Review and modify AI-suggested categories
- **Product Review UI**: Examine product options found by the AI
- **Optimization Review UI**: Accept or reject the AI's budget optimization

### 2. User Authentication
- **Login/Register Forms**: User authentication interface
- **Token-based Authentication**: Secure API communication
- **User Profile Display**: Shows logged-in user information

### 3. Personalized Shopping Experience
- **Preference-based Recommendations**: Products tailored to user preferences
- **Purchase History Integration**: Learns from past purchases
- **Personalized Search**: Enhanced search queries based on user data

## Technical Stack

- **Vue 3**: Progressive JavaScript framework with Composition API
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Next-generation frontend tooling
- **Chrome Extension API**: Browser integration

## Project Structure

- `src/components/Chatbot.vue`: Main chatbot component with UI and logic
- `src/App.vue`: Root application component
- `src/main.ts`: Application entry point
- `manifest.json`: Chrome extension manifest
- `popup.html`: Extension popup HTML
- `vite.config.ts`: Vite configuration

## Setup Instructions

1. Install dependencies:
```bash
npm install
```

2. Build the extension:
```bash
npm run build
```

3. Load the extension in Chrome:
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `extension` folder

## Development

### Running Development Server

```bash
npm run dev
```

This will start a development server at `http://localhost:5173/` where you can preview the application.

### Building for Production

```bash
npm run build
```

This will generate production-ready files in the `dist` directory.

## Component Details

### Chatbot.vue

The main component that handles:

- User authentication and profile management
- Message display and interaction
- Human-in-the-loop review interfaces
- Product card rendering
- Cart management

### Key Features

1. **Authentication**:
   - Login and registration forms
   - Token-based API communication
   - User profile display

2. **Human-in-the-Loop Interfaces**:
   - Category review interface
   - Product options review interface
   - Optimization review interface

3. **Message Handling**:
   - Displays user and AI messages in a chat interface
   - Handles loading states during API calls

4. **Product Display**:
   - Renders optimized products as cards
   - Shows product details including name, price, rating, brand, and description
   - Calculates and displays total cart price

5. **Cart Integration**:
   - Provides a button to proceed to Walmart cart
   - Opens cart URL in a new tab

## API Integration

The extension communicates with the backend API at `http://localhost:8000` for authentication, chat processing, and human-in-the-loop interactions.

### Authentication Flow

1. User registers or logs in
2. Backend returns an access token
3. Token is stored and used for subsequent API calls

### Chat Flow

1. User sends a message
2. Backend processes the message and may return an interrupt
3. User reviews and responds to the interrupt
4. Backend continues processing and returns optimized products

## Styling

The extension uses Tailwind CSS for styling with custom animations defined in the `<style>` section of the Chatbot component.