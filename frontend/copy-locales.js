const fs = require('fs');
const path = require('path');

// Source directory
const appDir = './src/app';

// Target locale directories
const locales = ['en', 'ur'];

// Items to copy (excluding the locale directories themselves, i18n.ts, and other locale dirs)
const itemsToCopy = ['page.tsx', 'layout.tsx', 'dashboard', 'login', 'profile', 'signup'];

// Get all items in the app directory
const allItems = fs.readdirSync(appDir);

// Filter to only include the items we want to copy
const itemsToProcess = allItems.filter(item => {
  return !['en', 'ur', 'i18n.ts'].includes(item) && itemsToCopy.includes(item);
});

locales.forEach(locale => {
  const localeDir = path.join(appDir, locale);

  // Create locale directory if it doesn't exist
  if (!fs.existsSync(localeDir)) {
    fs.mkdirSync(localeDir, { recursive: true });
    console.log(`Created directory: ${localeDir}`);
  }

  itemsToProcess.forEach(item => {
    const sourcePath = path.join(appDir, item);
    const destPath = path.join(localeDir, item);

    if (fs.existsSync(sourcePath)) {
      if (fs.lstatSync(sourcePath).isDirectory()) {
        // Copy directory recursively
        copyDirectory(sourcePath, destPath);
        console.log(`Copied directory: ${item} to ${locale}/`);
      } else {
        // Copy file
        fs.copyFileSync(sourcePath, destPath);
        console.log(`Copied file: ${item} to ${locale}/`);
      }
    }
  });
});

function copyDirectory(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const items = fs.readdirSync(src);
  items.forEach(item => {
    const srcPath = path.join(src, item);
    const destPath = path.join(dest, item);

    if (fs.lstatSync(srcPath).isDirectory()) {
      copyDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  });
}

console.log('Locale directories created and populated successfully!');