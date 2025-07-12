import { type FullConfig } from '@playwright/test';
import fs from 'fs';
import path from 'path';

async function globalTeardown(config: FullConfig): Promise<void> {
  console.log('🧹 Starting global teardown...');
  
  try {
    // Clean up authentication state file
    const authStatePath = path.join(__dirname, 'auth-state.json');
    if (fs.existsSync(authStatePath)) {
      fs.unlinkSync(authStatePath);
      console.log('🗑️ Cleaned up authentication state file');
    }
    
    // Clean up test artifacts directory if it exists
    const testResultsPath = path.join(__dirname, '..', 'test-results');
    if (fs.existsSync(testResultsPath)) {
      // Optional: Clean up old test results
      console.log('📁 Test results directory exists at:', testResultsPath);
    }
    
    // Additional cleanup can be added here
    // e.g., cleaning test data, stopping services, etc.
    
  } catch (error) {
    console.warn('⚠️ Error during global teardown:', error);
    // Don't fail if cleanup encounters issues
  }
  
  console.log('✅ Global teardown completed');
}

export default globalTeardown; 