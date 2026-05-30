const fs = require('fs');
const path = require('path');
const https = require('https');

const TOKEN = process.env.GITHUB_TOKEN || 'YOUR_GITHUB_TOKEN_HERE';
const OWNER = 'freefluxkr';
const REPO = 'DMDG_UT';
const BRANCH = 'main';

async function getFileSha(repoPath) {
  const options = {
    hostname: 'api.github.com',
    path: `/repos/${OWNER}/${REPO}/contents/${repoPath}?ref=${BRANCH}`,
    method: 'GET',
    headers: {
      'Authorization': `token ${TOKEN}`,
      'User-Agent': 'NodeJS'
    }
  };

  return new Promise((resolve) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const data = JSON.parse(body);
            resolve(data.sha);
          } catch (e) {
            resolve(null);
          }
        } else {
          resolve(null);
        }
      });
    });
    req.on('error', () => resolve(null));
    req.end();
  });
}

async function uploadFile(filePath, repoPath) {
  const content = fs.readFileSync(filePath, 'base64');
  const sha = await getFileSha(repoPath);
  
  const payload = {
    message: `Deploying ${repoPath}`,
    content: content,
    branch: BRANCH
  };
  
  if (sha) {
    payload.sha = sha;
  }

  const data = JSON.stringify(payload);

  const options = {
    hostname: 'api.github.com',
    path: `/repos/${OWNER}/${REPO}/contents/${repoPath}`,
    method: 'PUT',
    headers: {
      'Authorization': `token ${TOKEN}`,
      'User-Agent': 'NodeJS',
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(data)
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 201 || res.statusCode === 200) {
          console.log(`Success: ${repoPath}`);
          resolve();
        } else {
          console.error(`Error: ${repoPath}`, res.statusCode, body);
          resolve();
        }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  const distDir = path.join(__dirname, 'dist');
  const files = [
    { local: path.join(distDir, 'index.html'), remote: 'index.html' }
  ];
  
  const assetsDir = path.join(distDir, 'assets');
  if (fs.existsSync(assetsDir)) {
    const assetFiles = fs.readdirSync(assetsDir);
    for (const f of assetFiles) {
      files.push({
        local: path.join(assetsDir, f),
        remote: `assets/${f}`
      });
    }
  }

  for (const file of files) {
    await uploadFile(file.local, file.remote);
  }
  console.log("All files uploaded successfully!");
}

main();
