import React, { lazy, Suspense } from 'react';
import Layout from './layout';
import LoadingSpinner from './components/LoadingSpinner';

// Lazy load pages
const Home = lazy(() => import('./components/Home'));
const Blog = lazy(() => import('./components/Blog'));
const ChatBox = lazy(() => import('./components/ChatBox'));
const NotFound = lazy(() => import('./components/NotFound')); // NotFound page

// Helper function to wrap components with Suspense
const withSuspense = (Component) => (
  <Suspense fallback={<LoadingSpinner />}>
    <Component />
  </Suspense>
);

export const routes = [
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: withSuspense(Home) },
      { path: 'blog', element: withSuspense(Blog) },
      { path: 'websocket', element: withSuspense(ChatBox) },
    ],
  },
  {
    path: '*',
    element: withSuspense(NotFound), // Fallback route for unmatched paths
  },
];
