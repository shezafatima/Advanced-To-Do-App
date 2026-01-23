const fs = require('fs');
const path = require('path');

// Directories to fix
const localeDirs = ['en', 'ur'];
const appDir = './src/app';

localeDirs.forEach(locale => {
  const localeDir = path.join(appDir, locale);

  // Find all .tsx and .jsx files in the locale directory
  const walk = function(dir) {
    let results = [];
    const list = fs.readdirSync(dir);

    list.forEach(file => {
      file = path.resolve(dir, file);

      const stat = fs.statSync(file);

      if (stat && stat.isDirectory()) {
        results = [...results, ...walk(file)];
      } else if (file.endsWith('.tsx') || file.endsWith('.jsx') || file.endsWith('.ts') || file.endsWith('.js')) {
        results.push(file);
      }
    });

    return results;
  };

  const files = walk(localeDir);

  files.forEach(filePath => {
    let content = fs.readFileSync(filePath, 'utf8');

    // Replace relative imports that go up one level to go up two levels instead
    // This handles imports like '../context/auth-context' -> '../../context/auth-context'
    content = content.replace(/'\.\.\/context\//g, "'../../context/");
    content = content.replace(/"\.\.\/context\//g, '"../../context/');

    // Also fix other common relative paths that would be affected
    content = content.replace(/'\.\.\/components\//g, "'../../components/");
    content = content.replace(/"\.\.\/components\//g, '"../../components/');

    content = content.replace(/'\.\.\/lib\//g, "'../../lib/");
    content = content.replace(/"\.\.\/lib\//g, '"../../lib/');

    content = content.replace(/'\.\.\/utils\//g, "'../../utils/");
    content = content.replace(/"\.\.\/utils\//g, '"../../utils/');

    // Fix other relative paths that go up one level
    content = content.replace(/'\.\.\/styles\//g, "'../../styles/");
    content = content.replace(/"\.\.\/styles\//g, '"../../styles/');

    content = content.replace(/'\.\.\/hooks\//g, "'../../hooks/");
    content = content.replace(/"\.\.\/hooks\//g, '"../../hooks/');

    content = content.replace(/'\.\.\/types\//g, "'../../types/");
    content = content.replace(/"\.\.\/types\//g, '"../../types/');

    content = content.replace(/'\.\.\/api\//g, "'../../api/");
    content = content.replace(/"\.\.\/api\//g, '"../../api/');

    // Write the updated content back to the file
    fs.writeFileSync(filePath, content);
    console.log(`Fixed imports in: ${filePath}`);
  });
});

console.log('All import paths have been fixed for locale directories!');