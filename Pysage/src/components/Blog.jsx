import React from 'react';
import blogData from './data'; // Import the blog data

const BlogPage = () => {
  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <h1 className="text-3xl font-bold text-center text-gray-900 mb-6">Welcome to the Pysage Blog</h1>
      
      {blogData.map((section, index) => (
        <div
          key={index}
          className={`bg-${index % 2 === 0 ? 'gray-100' : 'white'} p-6 rounded-lg shadow-lg mb-6 flex flex-col lg:flex-row lg:items-center`}
        >
          <div className={`lg:w-${section.image ? '1/2' : 'full'} mb-4 lg:mb-0`}>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">{section.title}</h2>
            <p className="text-gray-700 text-lg mb-4">{section.description}</p>
          </div>
          
          {section.image && (
            <img src={section.image} alt={section.title} className="w-full lg:w-1/2 rounded-lg lg:order-2 mb-4 lg:mb-0" />
          )}
        </div>
      ))}
    </div>
  );
};

export default BlogPage;
