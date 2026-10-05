/**
 * Node.js build runner for CobolScope frontend assets.
 * Calls Python bundle_assets.py or executes node packaging.
 */
const { execSync } = require('child_process');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
console.log('[Frontend Build] Rebuilding CobolScope UI assets...');
try {
  const output = execSync('python scripts/bundle_assets.py', {
    cwd: repoRoot,
    stdio: 'inherit'
  });
  console.log('[Frontend Build] Assets successfully compiled to cobolscope/templates/assets/');
} catch (error) {
  console.error('[Frontend Build] Error compiling assets:', error);
  process.exit(1);
}
