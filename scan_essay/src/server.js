const express = require('express');
const multer = require('multer');
const path = require('path');
const runReadScan = require('./readScan');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 8080;
const OpenAIEndpoint = process.env.OPENAI_ENDPOINT;

app.use(express.static(path.join(__dirname, '../public')));
const upload = multer({ dest: 'uploads/' });

app.get('/scan', async (req, res) => {
    try {
        res.sendFile(path.join(__dirname, '../public/index.html'));
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
});

app.post('/upload', upload.single('file'), async (req, res) => {
    const filePath = req.file.path;
    try {
        const result = await runReadScan(filePath);
        res.json(result);
    } catch (error) {
        res.status(500).send('Error analyzing document');
    }
});

app.use('/api', (req, res, next) => {
    console.log('Received request for /api');
    next();
});

app.use('/api', createProxyMiddleware({
    target: OpenAIEndpoint,
    changeOrigin: true,
    pathRewrite: {
        '^/api': '/score'
    },
    onProxyReq: (proxyReq, req, res) => {
        console.log('Proxying request:', req.method, req.url);
        console.log('Full URL:', proxyReq.getHeader('host') + proxyReq.path);
    },
    onProxyRes: (proxyRes, req, res) => {
        console.log('Received response from target:', proxyRes.statusCode);
    },
    logLevel: 'debug'
}));

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});