import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { routes } from './routes';

const router = createBrowserRouter(routes, {
  future: {
    v7_partialHydration: true, // Enable advanced hydration (optional)
  },
});

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
