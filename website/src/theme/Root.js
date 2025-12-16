/**
 * Docusaurus Root Theme Wrapper
 * =============================
 * This component wraps all pages in the Docusaurus site.
 * We use it to inject the Chatbot widget on every page.
 *
 * @see https://docusaurus.io/docs/swizzling#wrapper-your-site-with-root
 */

import React from 'react';
import Chatbot from '@site/src/components/Chatbot';

// Default implementation, that you can customize
export default function Root({ children }) {
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}
