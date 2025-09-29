import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('title is present', () => {
  render(<App />);
  const title = screen.getByText(/Probabilistic model configuration/i);
  expect(title).toBeInTheDocument();
});
