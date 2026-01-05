// Configuration for different environments
const config = {
  development: {
    API_URL: 'http://localhost:8000/api/oracle'
  },
  production: {
    API_URL: import.meta.env.VITE_API_URL || 'https://your-lambda-url.amazonaws.com/api/oracle'
  }
};

// Determine environment
const isProduction = import.meta.env.PROD;
const environment = isProduction ? 'production' : 'development';

export const API_URL = config[environment].API_URL;
export const isDev = !isProduction;
