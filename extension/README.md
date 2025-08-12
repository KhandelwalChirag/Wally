# Smart Cart Builder Extension

This is the frontend component of the Smart Cart Builder project, implemented as a Chrome extension using Vue 3, TypeScript, and Tailwind CSS.

## Features

- **Chatbot Interface**: Natural language interaction with the AI shopping assistant
- **Product Display**: Visual cards showing optimized product selections
- **Budget Tracking**: Real-time calculation of total cart cost
- **One-click Checkout**: Direct link to Walmart cart for seamless checkout
- **Responsive Design**: Works across different screen sizes
- **Animated UI**: Smooth transitions and loading states

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

### Extension Popup

The extension popup is configured in `popup.html` and uses the built files from the `dist` directory.

## Component Details

### Chatbot.vue

The main component that handles:

- User input processing
- API communication with the backend
- Message display
- Product card rendering
- Cart management

#### Key Features

1. **Message Handling**:
   - Displays user and AI messages in a chat interface
   - Handles loading states during API calls

2. **Product Display**:
   - Renders optimized products as cards
   - Shows product details including name, price, rating, brand, and description
   - Calculates and displays total cart price

3. **Cart Integration**:
   - Provides a button to proceed to Walmart cart
   - Opens cart URL in a new tab

4. **Animations**:
   - Smooth transitions for messages and product cards
   - Loading animations during API calls
   - Hover effects for interactive elements

## API Integration

The extension communicates with the backend API at `http://localhost:8000/chat` to process user requests and retrieve optimized product recommendations.

### Request Format

```json
{
  "message": "I want to make pasta for $20"
}
```

### Response Format

```json
{
  "optimized_products": [
    {
      "name": "Great Value Spaghetti Pasta",
      "price": 1.24,
      "rating": 4.7,
      "brand": "Great Value",
      "category": "Pasta & Noodles",
      "description": "16 oz, dried pasta"
    },
    ...
  ],
  "cart_url": "https://walmart.com/cart",
  "message": "Found 5 optimized products for $18.75"
}
```

## Styling

The extension uses Tailwind CSS for styling with custom animations defined in the `<style>` section of the Chatbot component.

## Notes

This is a demo implementation. In a production environment, you would need to:

1. Configure proper CORS settings
2. Add error handling for network issues
3. Implement user authentication
4. Add proper state management for larger applications
5. Configure the extension for distribution through the Chrome Web Store