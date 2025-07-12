import { chromium, type FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig): Promise<void> {
  console.log('🚀 Starting global setup...');
  
  // Launch browser for authentication setup
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    // Navigate to login page
    console.log('📍 Navigating to login page...');
    await page.goto('http://localhost:3000/auth/login', { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    // Check if login elements exist
    const emailInput = page.locator('[data-testid="email-input"]');
    const passwordInput = page.locator('[data-testid="password-input"]');
    const loginButton = page.locator('[data-testid="login-button"]');
    
    if (await emailInput.isVisible() && await passwordInput.isVisible()) {
      // Perform login to get authentication state
      console.log('🔐 Performing login...');
      await emailInput.fill('admin@phishguard.com');
      await passwordInput.fill('demo123');
      await loginButton.click();
      
      // Wait for navigation to dashboard
      await page.waitForURL('**/dashboard', { timeout: 15000 });
      
      // Save authentication state
      await page.context().storageState({ 
        path: './e2e/auth-state.json' 
      });
      
      console.log('✅ Authentication state saved');
    } else {
      console.log('⚠️ Login form not found, skipping authentication setup');
    }
    
  } catch (error) {
    console.warn('⚠️ Could not setup authentication state:', error);
    // Don't fail the entire test suite if auth setup fails
  } finally {
    await browser.close();
  }
  
  console.log('✅ Global setup completed');
}

export default globalSetup; 