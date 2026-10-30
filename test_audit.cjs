const http = require('http');
const fs = require('fs');

const raw = fs.readFileSync('/tmp/test_sitemap.py', 'utf8');
const match = raw.match(/paths = (\[[\s\S]*?\])/);
if (!match) {
  console.error("No paths found");
  process.exit(1);
}
const paths = JSON.parse(match[1].replace(/'/g, '"'));

async function run() {
  const statusMap = {};
  const errors = [];
  
  for (const p of paths) {
    await new Promise((resolve) => {
      const req = http.request({
        host: '127.0.0.1',
        port: 3000,
        path: encodeURI(p),
        method: 'HEAD',
        headers: { 'User-Agent': 'Mozilla/5.0' }
      }, (res) => {
        const code = String(res.statusCode);
        statusMap[code] = (statusMap[code] || 0) + 1;
        if (code !== '200' && code !== '301') {
          errors.push([p, code]);
        }
        resolve();
      });
      req.on('error', (e) => {
        statusMap['ERR'] = (statusMap['ERR'] || 0) + 1;
        errors.push([p, 'ERR']);
        resolve();
      });
      req.end();
    });
  }
  
  console.log('RESULTS:');
  for (const [k, v] of Object.entries(statusMap)) {
    console.log('  HTTP ' + k + ': ' + v);
  }
  console.log('Total non-200/301: ' + errors.length);
  const byPrefix = {};
  for (const [p] of errors) {
    const parts = p.split('/').filter(Boolean);
    const prefix = parts[0] || '/';
    byPrefix[prefix] = (byPrefix[prefix] || 0) + 1;
  }
  console.log('Breakdown by prefix:');
  for (const [k, v] of Object.entries(byPrefix).sort((a,b)=>b[1]-a[1])) {
    console.log('  /' + k + ': ' + v);
  }
  console.log('Sample errors:');
  for (const [p, c] of errors.slice(0, 15)) {
    console.log('  ' + c + ' -> ' + p);
  }
}
run();
